cmake_minimum_required(VERSION 3.15...3.27)
cmake_policy(SET CMP0091 NEW)

project(PauliEngine LANGUAGES CXX)

# Standardkonfiguration
set(CMAKE_CXX_STANDARD 20)
set(CMAKE_POSITION_INDEPENDENT_CODE ON)

if (CMAKE_VERSION VERSION_LESS 3.18)
    set(DEV_MODULE Development)
else()
    set(DEV_MODULE Development.Module)
endif()

if (NOT CMAKE_BUILD_TYPE AND NOT CMAKE_CONFIGURATION_TYPES)
    set(CMAKE_BUILD_TYPE Release CACHE STRING "Choose the type of build." FORCE)
    set_property(CACHE CMAKE_BUILD_TYPE PROPERTY STRINGS "Debug" "Release" "MinSizeRel" "RelWithDebInfo")
endif()

# Conan Toolchain einbinden (nach: conan install .. --install-folder=build --build=missing)
include(${CMAKE_BINARY_DIR}/conan_toolchain.cmake OPTIONAL RESULT_VARIABLE _found)

# Python & SymEngine
find_package(Python REQUIRED COMPONENTS Interpreter Development.Module)
find_package(SymEngine REQUIRED CONFIG)

# Nanobind einbinden
add_subdirectory(nanobind)

# Header-only Bibliothek definieren
add_library(pauli_string INTERFACE)
target_include_directories(pauli_string INTERFACE ${CMAKE_CURRENT_SOURCE_DIR}/include)

if (SymEngine_FOUND)
    target_compile_definitions(pauli_string INTERFACE HAVE_SYMENGINE)
    target_link_libraries(pauli_string INTERFACE symengine)
endif()

# Python-Modul erstellen
nanobind_add_module(PauliEngine 
    QubitHamiltonian.cpp 
)

target_link_libraries(PauliEngine PRIVATE 
    pauli_string
)
