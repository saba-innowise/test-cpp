cmake_minimum_required(VERSION 3.15)

project(tetsum_consumer LANGUAGES CXX)

find_package(tetsum CONFIG REQUIRED)

add_executable(tetsum_consumer main.cpp)
target_link_libraries(tetsum_consumer PRIVATE tetsum::tetsum)
