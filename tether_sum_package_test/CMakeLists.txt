cmake_minimum_required(VERSION 3.15)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)

project(tether_sum_package_test DESCRIPTION "test tether_sum package installation" LANGUAGES C CXX)

find_package(tether_sum CONFIG REQUIRED)

# TetherAddExecutable is included via cmake_build_modules from tether_sum package
tether_add_executable(tether_sum_package_test tether_sum_package_test.cpp)
target_link_libraries(tether_sum_package_test PRIVATE tether_sum::tether_sum)