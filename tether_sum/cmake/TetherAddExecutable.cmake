function(tether_add_executable target)
    add_executable(${target} ${ARGN})
    if (MSVC)
        add_custom_command(
            TARGET ${target} POST_BUILD
            COMMAND ${CMAKE_COMMAND} -E copy -t $<TARGET_FILE_DIR:${target}> $<TARGET_RUNTIME_DLLS:${target}>
            COMMAND_EXPAND_LISTS
        )
    endif()
endfunction()