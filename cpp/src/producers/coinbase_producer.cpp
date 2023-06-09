
#include <boost/asio.hpp>
#include <boost/asio/ssl.hpp>
#include <boost/beast.hpp>
#include <boost/beast/ssl.hpp>
#include <cppkafka/cppkafka.h>

#include <fstream>
#include <iomanip>
#include <iostream>
#include <nlohmann/json.hpp>
#include <sys/types.h>
#include <unistd.h>
#include <system_error>
#include <unordered_map>
#include <pthread.h>
#include <sched.h>


namespace beast     = boost::beast;    
namespace http      = beast::http;     
namespace websocket = beast::websocket; 
namespace net       = boost::asio;      
namespace ssl       = net::ssl;
using beast::error_code;

using tcp           = net::ip::tcp; 
using json = nlohmann::json;

using TCPStream = beast::tcp_stream;
using SSLStream = beast::ssl_stream<TCPStream>;
using Stream    = websocket::stream<SSLStream>;

using namespace std::chrono_literals;
using namespace cppkafka;

void fail_ws(beast::error_code ec, char const* what)
{
    std::cerr << what << ": " << ec.message() << "\n";
}


std::map<std::string, int> load_symbols_partition_map() {
    // Open the JSON file
    std::ifstream i("coinbase_config.json");
    if (!i.is_open()) {
        throw std::runtime_error("Failed to open binance_config.json");
    }

    // Parse the JSON
    json j;
    i >> j;

    // Create a map of symbol to partition number
    std::map<std::string, int> symbol_dict;
    for (auto& [symbol, number] : j.items()) {
        symbol_dict[symbol] = number;
    }

    return symbol_dict;
}

#define COINBASE_HANDLER(c) beast::bind_front_handler(&coinbaseWS::c, this->shared_from_this())




class coinbaseWS : public std::enable_shared_from_this<coinbaseWS>
{
    tcp::resolver resolver_;
    Stream ws_;
    beast::flat_buffer buffer_;
    std::string message_text_;
    char const* host = "ws-feed.exchange.coinbase.com";
    std::string symb;
    std::string wsTarget_ = "/ws/";
    std::string host_;
    std::function<void()> message_handler;
    std::map<std::string, int> partition_map;
    Producer producer;


  public:

    coinbaseWS(net::any_io_executor ex, ssl::context& ctx)
        : resolver_(ex)
        , ws_(ex, ctx)
        , producer({
              { "metadata.broker.list", "localhost:9092" }
          })
        {
            partition_map = load_symbols_partition_map();
        }

    void run(json message) {
        if (!SSL_set_tlsext_host_name(ws_.next_layer().native_handle(), host)) {
            throw boost::system::system_error(
                error_code(::ERR_get_error(), net::error::get_ssl_category()));
        }
        host_ = host;
        message_text_ = message.dump();

        resolver_.async_resolve(host_, "443", COINBASE_HANDLER(on_resolve));
    }

    void on_resolve(beast::error_code ec, tcp::resolver::results_type results) {
        if (ec)
            return fail_ws(ec, "resolve");

        if (!SSL_set_tlsext_host_name(ws_.next_layer().native_handle(), host_.c_str())) {
            throw beast::system_error{
                error_code(::ERR_get_error(), net::error::get_ssl_category())};
        }

        get_lowest_layer(ws_).expires_after(30s);

        beast::get_lowest_layer(ws_).async_connect(results, COINBASE_HANDLER(on_connect));
    }

    void on_connect(beast::error_code                                           ec,
                    [[maybe_unused]] tcp::resolver::results_type::endpoint_type ep) {
        if (ec)
            return fail_ws(ec, "connect");

        // Perform the SSL handshake
        ws_.next_layer().async_handshake(ssl::stream_base::client, COINBASE_HANDLER(on_ssl_handshake));
    }

    void on_ssl_handshake(beast::error_code ec) {
        if (ec)
            return fail_ws(ec, "ssl_handshake");

        beast::get_lowest_layer(ws_).expires_never();

        ws_.set_option(websocket::stream_base::timeout::suggested(beast::role_type::client));

        ws_.set_option(websocket::stream_base::decorator([](websocket::request_type& req) {
            req.set(http::field::user_agent,
                    std::string(BOOST_BEAST_VERSION_STRING) + " websocket-client-async");
        }));

        std::cout << "using host_: " << host_ << std::endl;
        ws_.async_handshake(host_, wsTarget_, COINBASE_HANDLER(on_handshake));
    }

    void on_handshake(beast::error_code ec) {
        if (ec) {
            return fail_ws(ec, "handshake");
        }

        std::cout << "Sending : " << message_text_ << std::endl;

        ws_.async_write(net::buffer(message_text_), COINBASE_HANDLER(on_write));
    }

    void on_write(beast::error_code ec, size_t bytes_transferred) {
        boost::ignore_unused(bytes_transferred);

        if (ec)
            return fail_ws(ec, "write");

        ws_.async_read(buffer_, COINBASE_HANDLER(on_message));
    }

    void on_message(beast::error_code ec, size_t bytes_transferred) {
        boost::ignore_unused(bytes_transferred);
        if (ec)
            return fail_ws(ec, "read");

        buffer_.clear();
        ws_.async_read(buffer_, [this](beast::error_code ec, size_t n) {
            if (ec)
                return fail_ws(ec, "read");
            message_handler();
            buffer_.clear();
            ws_.async_read(buffer_, COINBASE_HANDLER(on_message));
        });
    }

    void on_close(beast::error_code ec) {
        if (ec)
            return fail_ws(ec, "close");

        std::cout << beast::make_printable(buffer_.data()) << std::endl;
    }

  
  void subscribe_orderbook(const std::string& market)
  {
    symb = market;

    json payload = {{"type", "subscribe"},
                {"product_ids", {market}},
                {"channels", {"level2"}}};

    message_handler = [this]() {

        json payload = json::parse(beast::buffers_to_string(buffer_.cdata()));
        
        std::cout << "Coinbase Orderbook Response : " << payload << std::endl;
        int partition_id = partition_map[symb];
        std::string payload_str = payload.dump();
        producer.produce(MessageBuilder("coinbase-orderbook").partition(partition_id).payload(payload_str));
        producer.flush();

    };

    run(payload);            
  }


};

void run_event_loop(const std::vector<std::string>& symbols, ssl::context& ctx)
{
    std::vector<std::shared_ptr<coinbaseWS>> ws_objects; // to make scope outside of for loop
    net::io_context ioc; // one event loop per core 
    for (const auto& symbol : symbols) {
        std::cout << symbol << std::endl;
        auto coinbasews = std::make_shared<coinbaseWS>(ioc.get_executor(), ctx);  
        ws_objects.push_back(coinbasews);
        coinbasews->subscribe_orderbook(symbol);
    }

    ioc.run(); // this will block until all asynchronous operations have completed
}

void set_core_affinity(unsigned int core_id)
{
    cpu_set_t cpuset;
    CPU_ZERO(&cpuset);
    CPU_SET(core_id, &cpuset);

    pthread_t current_thread = pthread_self();
    pthread_setaffinity_np(current_thread, sizeof(cpu_set_t), &cpuset);
}


int main(){


    ssl::context ctx1{ssl::context::tlsv12_client};

    ctx1.set_verify_mode(ssl::verify_peer);
    ctx1.set_default_verify_paths();

   const std::size_t num_cores = std::thread::hardware_concurrency(); 

    std::vector<std::string> symbols;
    std::map<std::string, int> partition_map = load_symbols_partition_map();
    
    for (const auto& pair : partition_map) {
        symbols.push_back(pair.first);
    }
    
    std::vector<std::thread> threads;
    // partition symbols into groups based on the number of available cores
    std::vector<std::vector<std::string>> symbol_groups(num_cores);

    std::size_t i = 0;
    for (const auto& symbol : symbols) {
        symbol_groups[i++ % num_cores].push_back(symbol);
    }

    for (unsigned int coreid = 0; coreid < symbol_groups.size(); coreid++) {
        const auto& symbol_group = symbol_groups[coreid];
        if(symbol_group.empty()){ // if symbols is less than number of cores you dont need to start the thread
            continue;
        }
        threads.emplace_back([&symbol_group, &ctx1, coreid]() { 
            set_core_affinity(coreid);
            run_event_loop(symbol_group, ctx1); 
        
        });
    }

    std::for_each(threads.begin(), threads.end(), [](std::thread& t) { t.join(); });

}