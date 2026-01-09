#include "tetsum/tetsum.hpp"
#include <gtest/gtest.h>

TEST(TetsumTest, BasicSum) {
    EXPECT_EQ(tetsum::sum(2, 2), 4);
    EXPECT_EQ(tetsum::sum(0, 0), 0);
    EXPECT_EQ(tetsum::sum(-1, 1), 0);
}
