include(GoogleTest)

tether_add_executable(tether_sum_test tether_sum_test)
target_link_libraries(tether_sum_test
    PRIVATE tether_sum
    PRIVATE GTest::gtest_main
)

gtest_discover_tests(tether_sum_test)