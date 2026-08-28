cmake_minimum_required(VERSION 3.20)

project(PQC_Migrate
    VERSION 0.1.0
    LANGUAGES C
)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# liboqs
find_path(OQS_INCLUDE_DIR
    NAMES oqs/oqs.h
    PATHS /usr/local/include
)

find_library(OQS_LIBRARY
    NAMES oqs
    PATHS /usr/local/lib
)

if(NOT OQS_INCLUDE_DIR OR NOT OQS_LIBRARY)
    message(FATAL_ERROR "liboqs not found")
endif()

message(STATUS "liboqs include: ${OQS_INCLUDE_DIR}")
message(STATUS "liboqs library: ${OQS_LIBRARY}")

# ML-KEM demonstration
add_executable(mlkem_demo
    src/crypto/mlkem_demo.c
)

target_include_directories(mlkem_demo PRIVATE
    ${OQS_INCLUDE_DIR}
)

target_link_libraries(mlkem_demo PRIVATE
    ${OQS_LIBRARY}
    crypto
    m
)
