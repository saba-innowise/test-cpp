cmake_minimum_required(VERSION 3.15)

option(TETHER_SUM_BUILD_TESTS "build tests" ON)
option(TETHER_SUM_BUILD_SHARED "build as shared library" ON)

# Read version from VERSION file
file(READ "${CMAKE_CURRENT_SOURCE_DIR}/VERSION" TETHER_SUM_VERSION_RAW)
string(STRIP "${TETHER_SUM_VERSION_RAW}" TETHER_SUM_VERSION)

# Parse major.minor.patch components
string(REPLACE "." ";" VERSION_LIST "${TETHER_SUM_VERSION}")
list(GET VERSION_LIST 0 TETHER_SUM_VERSION_MAJOR)
list(GET VERSION_LIST 1 TETHER_SUM_VERSION_MINOR)
list(GET VERSION_LIST 2 TETHER_SUM_VERSION_PATCH)

set(CMAKE_C_VISIBILITY_PRESET hidden)
set(CMAKE_CXX_VISIBILITY_PRESET hidden)

set(CMAKE_EXPORT_COMPILE_COMMANDS ON)


project(tether_sum VERSION ${TETHER_SUM_VERSION} DESCRIPTION "dummy library" LANGUAGES C CXX)

include(CMakePackageConfigHelpers)
include(GNUInstallDirs)

set(TETHER_SUM_INSTALL_LIBDIR "${CMAKE_INSTALL_LIBDIR}/$<IF:$<CONFIG:Release>,,$<CONFIG>>")
set(TETHER_SUM_INSTALL_BINDIR "${CMAKE_INSTALL_BINDIR}/$<IF:$<CONFIG:Release>,,$<CONFIG>>")
set(TETHER_SUM_INSTALL_DOCDIR "${CMAKE_INSTALL_DOCDIR}")
set(TETHER_SUM_INSTALL_INCLUDEDIR "${CMAKE_INSTALL_INCLUDEDIR}")
set(TETHER_SUM_INSTALL_CONFIGDIR "${CMAKE_INSTALL_LIBDIR}/cmake/tether_sum")

if(TETHER_SUM_BUILD_TESTS)
    find_package(GTest REQUIRED CONFIG)
endif()
    

list(PREPEND CMAKE_MODULE_PATH "${CMAKE_CURRENT_SOURCE_DIR}/cmake/")
include(TetherAddExecutable)
    
install(
    FILES cmake/TetherAddExecutable.cmake
    DESTINATION "${TETHER_SUM_INSTALL_CONFIGDIR}/modules"
)


add_subdirectory(tether_sum)
if(TETHER_SUM_BUILD_TESTS)
    enable_testing()
    add_subdirectory(tests)
endif()