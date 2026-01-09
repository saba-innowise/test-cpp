#include <tetsum/tetsum.hpp>
#include <iostream>

int main() {
    int result = tetsum::sum(2, 3);
    std::cout << "2 + 3 = " << result << std::endl;
    return result == 5 ? 0 : 1;
}
