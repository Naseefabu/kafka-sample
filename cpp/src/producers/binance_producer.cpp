

#include <boost/asio.hpp>
#include <boost/asio/ssl.hpp>
// #include <boost/url/src.hpp> 
#include <boost/beast.hpp>
#include <boost/beast/ssl.hpp>
//#include <boost/json/src.hpp>

#include <fstream>
#include <iomanip>
#include <string>
#include <iostream>
#include <nlohmann/json.hpp>
#include <sys/types.h>
#include <unistd.h>
#include <system_error>
#include <cppkafka/cppkafka.h>

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
    std::ifstream i("binance_config.json");
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

#define BINANCE_HANDLER(f) beast::bind_front_handler(&binanceWS::f, this->shared_from_this())


class binanceWS : public std::enable_shared_from_this<binanceWS> {

private:

    tcp::resolver resolver_;
    Stream ws_;
    beast::flat_buffer buffer_;
    std::string host_;
    std::string message_text_;

    std::string wsTarget_ = "/ws/";
    char const* host      = "stream.binance.com";
    char const* port      = "9443";
    std::function<void()> message_handler;
    std::string symb;
    Producer producer;

public:
    binanceWS(net::any_io_executor ex, ssl::context& ctx)
        : resolver_(ex)
        , ws_(ex, ctx)
        , producer({
              { "metadata.broker.list", "localhost:9092" }
          })
         {}

    void run(char const* host, char const* port, json message, const std::string& streamName) {
        if (!SSL_set_tlsext_host_name(ws_.next_layer().native_handle(), host)) {
            throw boost::system::system_error(
                error_code(::ERR_get_error(), net::error::get_ssl_category()));
        }

        host_         = host;
        message_text_ = message.dump();
        wsTarget_ += streamName;

        resolver_.async_resolve(host_, port, BINANCE_HANDLER(on_resolve));
    }

    void on_resolve(beast::error_code ec, tcp::resolver::results_type results) {
        if (ec)
            return fail_ws(ec, "resolve");

        if (!SSL_set_tlsext_host_name(ws_.next_layer().native_handle(), host_.c_str())) {
            throw beast::system_error{
                error_code(::ERR_get_error(), net::error::get_ssl_category())};
        }

        get_lowest_layer(ws_).expires_after(30s);

        beast::get_lowest_layer(ws_).async_connect(results, BINANCE_HANDLER(on_connect));
    }

    void on_connect(beast::error_code                                           ec,
                    [[maybe_unused]] tcp::resolver::results_type::endpoint_type ep) {
        if (ec)
            return fail_ws(ec, "connect");

        // Perform the SSL handshake
        ws_.next_layer().async_handshake(ssl::stream_base::client, BINANCE_HANDLER(on_ssl_handshake));
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
        ws_.async_handshake(host_, wsTarget_, BINANCE_HANDLER(on_handshake));
    }

    void on_handshake(beast::error_code ec) {
        if (ec) {
            return fail_ws(ec, "handshake");
        }

        std::cout << "Sending : " << message_text_ << std::endl;

        ws_.async_write(net::buffer(message_text_), BINANCE_HANDLER(on_write));
    }

    void on_write(beast::error_code ec, size_t bytes_transferred) {
        boost::ignore_unused(bytes_transferred);

        if (ec)
            return fail_ws(ec, "write");
        std::cout << "on_write : " << std::endl;

        ws_.async_read(buffer_, BINANCE_HANDLER(on_message));
    }

    void on_message(beast::error_code ec, size_t bytes_transferred) {

        boost::ignore_unused(bytes_transferred);
        if (ec)
            return fail_ws(ec, "read");

        //json payload = json::parse(beast::buffers_to_string(buffer_.cdata()));
        // std::cout << "on_message : " << payload << std::endl;

        buffer_.clear();
        ws_.async_read(buffer_, [this](beast::error_code ec, size_t n) {
            if (ec)
                return fail_ws(ec, "read");

            message_handler();
            buffer_.clear();
            ws_.async_read(buffer_, BINANCE_HANDLER(on_message));
        });

    }

    void on_close(beast::error_code ec) {
        if (ec)
            return fail_ws(ec, "close");

        std::cout << beast::make_printable(buffer_.data()) << std::endl;
    }
    
    void subscribe_orderbook(const std::string action,const std::string symbol, int levels)
    {
        symb = symbol;
        std::string stream = symbol+"@"+"depth"+std::to_string(levels);
        message_handler = [this]() {

            json payload = json::parse(beast::buffers_to_string(buffer_.cdata()));
            
            // std::cout << "Binance Orderbook Response : " << payload << std::endl;
            std::map<std::string, int> partition_map = load_symbols_partition_map();
            int partition_id = partition_map[symb];
            std::string payload_str = payload.dump();
            producer.produce(MessageBuilder("kraken-orderbook").partition(partition_id).payload(payload_str));
            producer.flush();

        };
        json jv = {
            { "method", action },
            { "params", {stream} },
            { "id", 1 }
        };
        run(host, port,jv, stream);
    }



};


int main(){
    net::io_context ioc; 
    ssl::context ctx{ssl::context::tlsv12_client};

    ctx.set_verify_mode(ssl::verify_peer);
    ctx.set_default_verify_paths();

    // Create the config
    Configuration config = {
        { "metadata.broker.list", "localhost:9092" }
    };

    std::map<std::string, int> dict = load_symbols_partition_map();
    std::cout << dict["BTC/USD"] << std::endl;


    // Create the producer
    Producer producer(config);

    // Produce a message!
    std::string message = "hey there!";
    producer.produce(MessageBuilder("binance-orderbook").partition(0).payload(message));
    producer.flush();

    
    // auto binancews = std::make_shared<binanceWS>(ioc.get_executor(),ctx); 
    // binancews->subscribe_orderbook("SUBSCRIBE","btcusdt",5);  

    // ioc.run();
}