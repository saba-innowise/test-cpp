from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout


class TetherSumPackageTestConan(ConanFile):
    name = "tether_sum_package_test"
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        self.requires("tether_sum/0.1")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
