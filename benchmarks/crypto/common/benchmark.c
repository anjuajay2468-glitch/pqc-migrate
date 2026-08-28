#include <stdio.h>
#include <time.h>

#include "benchmark.h"

double benchmark_elapsed_us(
    struct timespec start,
    struct timespec end)
{
    return (end.tv_sec - start.tv_sec) * 1000000.0 +
           (end.tv_nsec - start.tv_nsec) / 1000.0;
}

void benchmark_print_result(
    const char *algorithm,
    const char *operation,
    BenchmarkResult result)
{
    printf("%s,%s,%.3f,%.3f,%.3f\n",
           algorithm,
           operation,
           result.average_us,
           result.minimum_us,
           result.maximum_us);
}

void benchmark_write_csv(
    const char *filename,
    const char *algorithm,
    const char *category,
    const char *operation,
    BenchmarkResult result)
{
    FILE *file = fopen(filename, "a");

    if (!file)
    {
        perror("Failed to open CSV file");
        return;
    }

    fprintf(file,
            "%s,%s,%s,%.3f,%.3f,%.3f\n",
            algorithm,
            category,
            operation,
            result.average_us,
            result.minimum_us,
            result.maximum_us);

    fclose(file);
}
