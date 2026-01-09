cmake_minimum_required(VERSION 3.15)

option(TETSUM_BUILD_TESTS "Build tests" OFF)

project(tetsum VERSION 1.0 DESCRIPTION "Simple static library" LANGUAGES CXX)

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

# Library
add_library(tetsum STATIC
    src/tetsum.cpp
)

target_include_directories(tetsum
    PUBLIC
        $<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>
        $<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>
)

# Install
install(TARGETS tetsum
    EXPORT tetsumTargets
    ARCHIVE DESTINATION ${CMAKE_INSTALL_LIBDIR}
)

install(EXPORT tetsumTargets
    FILE tetsumTargets.cmake
    NAMESPACE tetsum::
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/tetsum
)

install(DIRECTORY include/tetsum
    DESTINATION ${CMAKE_INSTALL_INCLUDEDIR}
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/Config.cmake.in"
    "${CMAKE_CURRENT_BINARY_DIR}/tetsumConfig.cmake"
    INSTALL_DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/tetsum
    NO_SET_AND_CHECK_MACRO
)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/tetsumConfigVersion.cmake"
    VERSION ${PROJECT_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(FILES
    "${CMAKE_CURRENT_BINARY_DIR}/tetsumConfig.cmake"
    "${CMAKE_CURRENT_BINARY_DIR}/tetsumConfigVersion.cmake"
    DESTINATION ${CMAKE_INSTALL_LIBDIR}/cmake/tetsum
)

# Tests
if(TETSUM_BUILD_TESTS)
    enable_testing()
    find_package(GTest REQUIRED CONFIG)
    add_subdirectory(tests)
endif()
