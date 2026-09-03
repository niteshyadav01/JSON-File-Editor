cmake_minimum_required(VERSION 3.15)
project(TODO)

# Use Python from virtualenv or system
find_package(Python3 COMPONENTS Interpreter REQUIRED)

# Set source dir
add_subdirectory(src)

