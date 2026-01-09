import os

from conan import ConanFile
from conan.tools.cmake import CMake, CMakeDeps, CMakeToolchain, cmake_layout
from conan.tools.files import load


class TetherSumPackageTestConan(ConanFile):
    name = "tether_sum_package_test"
    settings = "os", "compiler", "build_type", "arch"

    def requirements(self):
        version_file = os.path.join(self.recipe_folder, "../tether_sum/VERSION")
        base_version = load(self, version_file).strip()
        self.requires(f"tether_sum/{base_version}")

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
