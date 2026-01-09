#include "tether_sum/tether_sum.hpp"

#include <gtest/gtest.h>

// Demonstrate some basic assertions.
TEST(TetherTest, BasicAssertions) { EXPECT_EQ(tether::sum(2, 2), 4); }

// #include <iostream>

// int main() {
//     std::cout << tether::sum(2, 2) << std::endl;
//     return 0;
// }