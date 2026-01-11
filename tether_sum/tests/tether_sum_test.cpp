#include "tether_sum/tether_sum.hpp"

#include <gtest/gtest.h>

TEST(TetherTest, BasicAssertions) { EXPECT_EQ(tether::sum(2, 2), 4); }
