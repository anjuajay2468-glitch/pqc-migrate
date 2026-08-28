cmake_minimum_required(VERSION 3.20)

project(PQC_Migrate
    VERSION 0.1.0
    LANGUAGES C
)

set(CMAKE_C_STANDARD 11)
set(CMAKE_C_STANDARD_REQUIRED ON)

# ============================================================
# liboqs
# ============================================================

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


# ============================================================
# Shared Benchmark Library
# ============================================================

add_library(benchmark_common
    benchmarks/crypto/common/benchmark.c
)

target_include_directories(benchmark_common PUBLIC
    benchmarks/crypto/common
)


# ============================================================
# ML-KEM Demo
# ============================================================

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


# ============================================================
# ML-KEM Benchmark
# ============================================================

add_executable(mlkem_benchmark
    benchmarks/crypto/mlkem_benchmark.c
)

target_include_directories(mlkem_benchmark PRIVATE
    ${OQS_INCLUDE_DIR}
)

target_link_libraries(mlkem_benchmark PRIVATE
    ${OQS_LIBRARY}
    crypto
    m
    benchmark_common
)


# ============================================================
# X25519 Classical Benchmark
# ============================================================

add_executable(x25519_benchmark
    benchmarks/crypto/x25519_benchmark.c
)

target_link_libraries(x25519_benchmark PRIVATE
    crypto
    benchmark_common
)


# ============================================================
# ML-DSA Benchmark
# ============================================================

add_executable(mldsa_benchmark
    benchmarks/crypto/mldsa_benchmark.c
)

target_include_directories(mldsa_benchmark PRIVATE
    ${OQS_INCLUDE_DIR}
)

target_link_libraries(mldsa_benchmark PRIVATE
    ${OQS_LIBRARY}
    crypto
    m
    benchmark_common
)


# ============================================================
# ECDSA Classical Benchmark
# ============================================================

add_executable(ecdsa_benchmark
    benchmarks/crypto/ecdsa_benchmark.c
)

target_link_libraries(ecdsa_benchmark PRIVATE
    crypto
    benchmark_common
)


# ============================================================
# RSA-2048 Classical Benchmark
# ============================================================

add_executable(rsa_benchmark
    benchmarks/crypto/rsa_benchmark.c
)

target_link_libraries(rsa_benchmark PRIVATE
    crypto
    benchmark_common
)
