set(TETHER_SUM_LIB_HEADERS
    include/tether_sum/tether_sum.hpp
    include/tether_sum/export.hpp
)

set(TETHER_SUM_LIB_SOURCES
    src/tether_sum.cpp
)

if(TETHER_SUM_BUILD_SHARED)
    set(TETHER_SUM_LIB_TYPE SHARED)
else()
    set(TETHER_SUM_LIB_TYPE STATIC)
endif()

configure_file(config.hpp.in include/tether_sum/config.hpp @ONLY)

add_library(tether_sum
    "${TETHER_SUM_LIB_TYPE}"
    "${TETHER_SUM_LIB_SOURCES}"
    "${TETHER_SUM_LIB_HEADERS}"
    "${CMAKE_CURRENT_BINARY_DIR}/include/tether_sum/config.hpp"
)

target_include_directories(tether_sum
    PUBLIC
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_SOURCE_DIR}/include>"
        "$<BUILD_INTERFACE:${CMAKE_CURRENT_BINARY_DIR}/include>"
        "$<INSTALL_INTERFACE:${CMAKE_INSTALL_INCLUDEDIR}>"
)

if(TETHER_SUM_BUILD_SHARED)
    target_compile_definitions(tether_sum PRIVATE TETHER_SUM_EXPORTS)
    target_compile_definitions(tether_sum PUBLIC TETHER_SUM_IMPORTS)
endif()


install(
    TARGETS tether_sum
    EXPORT tether_sumTargets
    LIBRARY DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    ARCHIVE DESTINATION "${CMAKE_INSTALL_LIBDIR}"
    RUNTIME DESTINATION "${CMAKE_INSTALL_BINDIR}"
)

install(
    EXPORT tether_sumTargets
    FILE tether_sumTargets.cmake
    NAMESPACE tether_sum::
    DESTINATION "${TETHER_SUM_INSTALL_CONFIGDIR}"
)

install(
    DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include/tether_sum
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)

install(
    DIRECTORY include/tether_sum
    DESTINATION "${CMAKE_INSTALL_INCLUDEDIR}"
)

configure_package_config_file(
    "${CMAKE_CURRENT_SOURCE_DIR}/Config.cmake.in" "${CMAKE_CURRENT_BINARY_DIR}/tether_sumConfig.cmake"
    INSTALL_DESTINATION "${TETHER_SUM_INSTALL_CONFIGDIR}"
    NO_SET_AND_CHECK_MACRO
)

write_basic_package_version_file(
    "${CMAKE_CURRENT_BINARY_DIR}/tether_sumConfigVersion.cmake"
    VERSION ${TETHER_SUM_VERSION}
    COMPATIBILITY SameMajorVersion
)

install(
    FILES
        "${CMAKE_CURRENT_BINARY_DIR}/tether_sumConfig.cmake"
        "${CMAKE_CURRENT_BINARY_DIR}/tether_sumConfigVersion.cmake"
    DESTINATION 
        "${TETHER_SUM_INSTALL_CONFIGDIR}"
)