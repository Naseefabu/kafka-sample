cmake_minimum_required(VERSION 3.16)
project(producers)

#set(CMAKE_CXX_COMPILER /usr/bin/clang++)
set (CMAKE_CXX_FLAGS "-O3 -pthread -DNDEBUG -lssl -lcrypto")


include(FetchContent)

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.10.5/json.tar.xz) # nlohmann json
FetchContent_MakeAvailable(json)

find_package(Boost 1.79.0 REQUIRED COMPONENTS system thread filesystem container)
find_package(Threads REQUIRED)
find_package(OpenSSL REQUIRED)
find_package(CppKafka REQUIRED)

set(URLIB_DIRECTORY "${CMAKE_CURRENT_SOURCE_DIR}/externel/url/include")
set(URLIB_HEADERS ${URLIB_DIRECTORY}/boost/url.hpp ${URLIB_DIRECTORY}/boost/url/src.hpp)

add_executable(binance binance_producer.cpp)
target_include_directories(binance SYSTEM PRIVATE ${Boost_INCLUDE_DIRS})
target_link_libraries(binance PUBLIC Boost::boost Threads::Threads)
target_link_libraries(binance PUBLIC ssl crypto)
target_link_libraries(binance PRIVATE nlohmann_json::nlohmann_json)
target_link_libraries(binance PRIVATE CppKafka::cppkafka)

add_executable(coinbase coinbase_producer.cpp)
target_include_directories(coinbase SYSTEM PRIVATE ${Boost_INCLUDE_DIRS})
target_link_libraries(coinbase PUBLIC Boost::boost Threads::Threads)
target_link_libraries(coinbase PUBLIC ssl crypto)
target_link_libraries(coinbase PRIVATE nlohmann_json::nlohmann_json)
target_link_libraries(coinbase PRIVATE CppKafka::cppkafka)