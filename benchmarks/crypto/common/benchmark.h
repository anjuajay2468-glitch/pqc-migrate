#ifndef PQC_MIGRATE_BENCHMARK_H
#define PQC_MIGRATE_BENCHMARK_H

#include <stdio.h>
#include <time.h>

#define BENCHMARK_ITERATIONS 1000

typedef struct {
    double average_us;
    double minimum_us;
    double maximum_us;
} BenchmarkResult;

double benchmark_elapsed_us(
    struct timespec start,
    struct timespec end
);

void benchmark_print_result(
    const char *algorithm,
    const char *operation,
    BenchmarkResult result
);

void benchmark_write_csv(
    const char *filename,
    const char *algorithm,
    const char *category,
    const char *operation,
    BenchmarkResult result
);

#endif
