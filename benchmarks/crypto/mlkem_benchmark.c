#include <stdio.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <oqs/oqs.h>
#include "common/benchmark.h"

#define CSV_FILE "../results/crypto/baseline.csv"

static double elapsed_us(struct timespec start, struct timespec end)
{
    return (end.tv_sec - start.tv_sec) * 1000000.0 +
           (end.tv_nsec - start.tv_nsec) / 1000.0;
}

int main(void)
{
    OQS_KEM *kem = OQS_KEM_new("ML-KEM-768");

    if (kem == NULL)
    {
        fprintf(stderr, "Failed to initialize ML-KEM-768\n");
        return 1;
    }

    uint8_t *public_key = malloc(kem->length_public_key);
    uint8_t *secret_key = malloc(kem->length_secret_key);
    uint8_t *ciphertext = malloc(kem->length_ciphertext);
    uint8_t *shared_secret = malloc(kem->length_shared_secret);
    uint8_t *shared_secret_check = malloc(kem->length_shared_secret);

    if (!public_key || !secret_key || !ciphertext ||
        !shared_secret || !shared_secret_check)
    {
        fprintf(stderr, "Memory allocation failed\n");
        OQS_KEM_free(kem);
        return 1;
    }

    double keygen_total = 0.0;
    double encaps_total = 0.0;
    double decaps_total = 0.0;

    double keygen_min = 1e30;
    double keygen_max = 0.0;

    double encaps_min = 1e30;
    double encaps_max = 0.0;

    double decaps_min = 1e30;
    double decaps_max = 0.0;

    struct timespec start, end;

    printf("=============================================\n");
    printf("       PQC-Migrate ML-KEM-768 Benchmark\n");
    printf("=============================================\n\n");

    printf("Iterations: %d\n\n", BENCHMARK_ITERATIONS);

    /* Warm-up */
    OQS_KEM_keypair(kem, public_key, secret_key);
    OQS_KEM_encaps(kem, ciphertext, shared_secret, public_key);
    OQS_KEM_decaps(kem, shared_secret_check, ciphertext, secret_key);

    for (int i = 0; i < BENCHMARK_ITERATIONS; i++)
    {
        double elapsed;

        /* Key generation */
        clock_gettime(CLOCK_MONOTONIC, &start);

        if (OQS_KEM_keypair(kem, public_key, secret_key) != OQS_SUCCESS)
        {
            fprintf(stderr, "Key generation failed\n");
            OQS_KEM_free(kem);
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        keygen_total += elapsed;

        if (elapsed < keygen_min)
            keygen_min = elapsed;

        if (elapsed > keygen_max)
            keygen_max = elapsed;

        /* Encapsulation */
        clock_gettime(CLOCK_MONOTONIC, &start);

        if (OQS_KEM_encaps(
                kem,
                ciphertext,
                shared_secret,
                public_key) != OQS_SUCCESS)
        {
            fprintf(stderr, "Encapsulation failed\n");
            OQS_KEM_free(kem);
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        encaps_total += elapsed;

        if (elapsed < encaps_min)
            encaps_min = elapsed;

        if (elapsed > encaps_max)
            encaps_max = elapsed;

        /* Decapsulation */
        clock_gettime(CLOCK_MONOTONIC, &start);

        if (OQS_KEM_decaps(
                kem,
                shared_secret_check,
                ciphertext,
                secret_key) != OQS_SUCCESS)
        {
            fprintf(stderr, "Decapsulation failed\n");
            OQS_KEM_free(kem);
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        decaps_total += elapsed;

        if (elapsed < decaps_min)
            decaps_min = elapsed;

        if (elapsed > decaps_max)
            decaps_max = elapsed;

        /* Correctness */
        if (memcmp(
                shared_secret,
                shared_secret_check,
                kem->length_shared_secret) != 0)
        {
            fprintf(stderr,
                    "Shared-secret mismatch at iteration %d\n",
                    i);

            OQS_KEM_free(kem);
            return 1;
        }
    }

    BenchmarkResult keygen = {
        keygen_total / BENCHMARK_ITERATIONS,
        keygen_min,
        keygen_max
    };

    BenchmarkResult encaps = {
        encaps_total / BENCHMARK_ITERATIONS,
        encaps_min,
        encaps_max
    };

    BenchmarkResult decaps = {
        decaps_total / BENCHMARK_ITERATIONS,
        decaps_min,
        decaps_max
    };

    printf("RESULTS\n");
    printf("---------------------------------------------\n");

    printf("Key Generation\n");
    printf("  Average: %.3f us\n", keygen.average_us);
    printf("  Minimum: %.3f us\n", keygen.minimum_us);
    printf("  Maximum: %.3f us\n\n", keygen.maximum_us);

    printf("Encapsulation\n");
    printf("  Average: %.3f us\n", encaps.average_us);
    printf("  Minimum: %.3f us\n", encaps.minimum_us);
    printf("  Maximum: %.3f us\n\n", encaps.maximum_us);

    printf("Decapsulation\n");
    printf("  Average: %.3f us\n", decaps.average_us);
    printf("  Minimum: %.3f us\n", decaps.minimum_us);
    printf("  Maximum: %.3f us\n\n", decaps.maximum_us);

    printf("All shared-secret checks: SUCCESS\n");

    benchmark_write_csv(
        CSV_FILE,
        "ML-KEM-768",
        "KEM",
        "keygen",
        keygen);

    benchmark_write_csv(
        CSV_FILE,
        "ML-KEM-768",
        "KEM",
        "encapsulation",
        encaps);

    benchmark_write_csv(
        CSV_FILE,
        "ML-KEM-768",
        "KEM",
        "decapsulation",
        decaps);

    free(public_key);
    free(secret_key);
    free(ciphertext);
    free(shared_secret);
    free(shared_secret_check);

    OQS_KEM_free(kem);

    return 0;
}
