cmake_minimum_required(VERSION 3.15)

project(RTMAConsumer LANGUAGES CXX)

find_package(RTMA CONFIG REQUIRED)

add_executable(rtma_consumer main.cpp)
target_link_libraries(rtma_consumer PRIVATE RTMA::RTMA)
