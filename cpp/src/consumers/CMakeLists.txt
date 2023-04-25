cmake_minimum_required(VERSION 3.16)
project(consumers)

#set(CMAKE_CXX_COMPILER /usr/bin/clang++)
set (CMAKE_CXX_FLAGS "-O3 -pthread -DNDEBUG -lssl -lcrypto")


include(FetchContent)

FetchContent_Declare(json URL https://github.com/nlohmann/json/releases/download/v3.10.5/json.tar.xz) # nlohmann json
FetchContent_MakeAvailable(json)



find_package(CppKafka REQUIRED)


add_executable(mm market_making.cpp)


target_link_libraries(mm PUBLIC ssl crypto)
target_link_libraries(mm PRIVATE nlohmann_json::nlohmann_json)
target_link_libraries(mm PRIVATE CppKafka::cppkafka)