include(GoogleTest)

add_executable(tetsum_test tetsum_test.cpp)
target_link_libraries(tetsum_test
    PRIVATE tetsum
    PRIVATE GTest::gtest_main
)

gtest_discover_tests(tetsum_test)
