# J.A.R.V.I.S. Windows native bridge scaffold
cmake_minimum_required(VERSION 3.20)
project(jarvis_bridge LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_library(jarvis_bridge STATIC native_bridge/jarvis_bridge.cpp)
target_compile_definitions(jarvis_bridge PRIVATE UNICODE _UNICODE)
