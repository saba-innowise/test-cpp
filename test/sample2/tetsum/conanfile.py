from conan import ConanFile
from conan.tools.cmake import CMake, CMakeToolchain, CMakeDeps, cmake_layout


class TetsumConan(ConanFile):
    name = "tetsum"
    version = "1.0"
    description = "Simple static library example"
    license = "MIT"

    settings = "os", "compiler", "build_type", "arch"
    options = {
        "build_tests": [True, False],
        "run_tests": [True, False],
    }
    default_options = {
        "build_tests": False,
        "run_tests": False,
    }

    exports_sources = "CMakeLists.txt", "Config.cmake.in", "src/*", "include/*", "tests/*"

    def requirements(self):
        if self.options.build_tests:
            self.test_requires("gtest/1.15.0")

    def layout(self):
        cmake_layout(self)

    def generate(self):
        deps = CMakeDeps(self)
        deps.generate()

        tc = CMakeToolchain(self)
        tc.cache_variables["TETSUM_BUILD_TESTS"] = "ON" if self.options.build_tests else "OFF"
        tc.generate()

    def build(self):
        cmake = CMake(self)
        cmake.configure()
        cmake.build()
        if self.options.build_tests and self.options.run_tests:
            cmake.test()

    def package(self):
        cmake = CMake(self)
        cmake.install()

    def package_info(self):
        self.cpp_info.libs = ["tetsum"]
        self.cpp_info.set_property("cmake_file_name", "tetsum")
        self.cpp_info.set_property("cmake_target_name", "tetsum::tetsum")
