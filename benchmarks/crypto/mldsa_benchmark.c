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
    OQS_SIG *sig = OQS_SIG_new("ML-DSA-65");

    if (sig == NULL)
    {
        fprintf(stderr, "Failed to initialize ML-DSA-65\n");
        return 1;
    }

    uint8_t *public_key = malloc(sig->length_public_key);
    uint8_t *secret_key = malloc(sig->length_secret_key);
    uint8_t *signature = malloc(sig->length_signature);

    const uint8_t message[] =
        "PQC-Migrate research benchmark message";

    size_t message_len = sizeof(message) - 1;

    if (!public_key || !secret_key || !signature)
    {
        fprintf(stderr, "Memory allocation failed\n");
        OQS_SIG_free(sig);
        return 1;
    }

    double keygen_total = 0.0;
    double sign_total = 0.0;
    double verify_total = 0.0;

    double keygen_min = 1e30;
    double keygen_max = 0.0;

    double sign_min = 1e30;
    double sign_max = 0.0;

    double verify_min = 1e30;
    double verify_max = 0.0;

    struct timespec start, end;

    printf("=============================================\n");
    printf("       PQC-Migrate ML-DSA-65 Benchmark\n");
    printf("=============================================\n\n");

    printf("Iterations: %d\n\n", BENCHMARK_ITERATIONS);

    /* Warm-up */
    size_t warmup_signature_len = 0;

    OQS_SIG_keypair(sig, public_key, secret_key);
    OQS_SIG_sign(
        sig,
        signature,
        &warmup_signature_len,
        message,
        message_len,
        secret_key
    );
    OQS_SIG_verify(
        sig,
        message,
        message_len,
        signature,
        warmup_signature_len,
        public_key
    );

    for (int i = 0; i < BENCHMARK_ITERATIONS; i++)
    {
        double elapsed;
        size_t signature_len = sig->length_signature;

        /* Key generation */

        clock_gettime(CLOCK_MONOTONIC, &start);

        if (OQS_SIG_keypair(
                sig,
                public_key,
                secret_key) != OQS_SUCCESS)
        {
            fprintf(stderr, "Key generation failed\n");
            OQS_SIG_free(sig);
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        keygen_total += elapsed;

        if (elapsed < keygen_min)
            keygen_min = elapsed;

        if (elapsed > keygen_max)
            keygen_max = elapsed;

        /* Signing */

        clock_gettime(CLOCK_MONOTONIC, &start);

        if (OQS_SIG_sign(
                sig,
                signature,
                &signature_len,
                message,
                message_len,
                secret_key) != OQS_SUCCESS)
        {
            fprintf(stderr, "Signing failed\n");
            OQS_SIG_free(sig);
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        sign_total += elapsed;

        if (elapsed < sign_min)
            sign_min = elapsed;

        if (elapsed > sign_max)
            sign_max = elapsed;

        /* Verification */

        clock_gettime(CLOCK_MONOTONIC, &start);

        if (OQS_SIG_verify(
                sig,
                message,
                message_len,
                signature,
                signature_len,
                public_key) != OQS_SUCCESS)
        {
            fprintf(stderr, "Signature verification failed\n");
            OQS_SIG_free(sig);
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        verify_total += elapsed;

        if (elapsed < verify_min)
            verify_min = elapsed;

        if (elapsed > verify_max)
            verify_max = elapsed;
    }

    BenchmarkResult keygen = {
        keygen_total / BENCHMARK_ITERATIONS,
        keygen_min,
        keygen_max
    };

    BenchmarkResult signing = {
        sign_total / BENCHMARK_ITERATIONS,
        sign_min,
        sign_max
    };

    BenchmarkResult verification = {
        verify_total / BENCHMARK_ITERATIONS,
        verify_min,
        verify_max
    };

    printf("RESULTS\n");
    printf("---------------------------------------------\n");

    printf("Key Generation\n");
    printf("  Average: %.3f us\n", keygen.average_us);
    printf("  Minimum: %.3f us\n", keygen.minimum_us);
    printf("  Maximum: %.3f us\n\n", keygen.maximum_us);

    printf("Signing\n");
    printf("  Average: %.3f us\n", signing.average_us);
    printf("  Minimum: %.3f us\n", signing.minimum_us);
    printf("  Maximum: %.3f us\n\n", signing.maximum_us);

    printf("Verification\n");
    printf("  Average: %.3f us\n", verification.average_us);
    printf("  Minimum: %.3f us\n", verification.minimum_us);
    printf("  Maximum: %.3f us\n\n", verification.maximum_us);

    printf("All signature checks: SUCCESS\n");

    benchmark_write_csv(
        CSV_FILE,
        "ML-DSA-65",
        "SIGNATURE",
        "keygen",
        keygen
    );

    benchmark_write_csv(
        CSV_FILE,
        "ML-DSA-65",
        "SIGNATURE",
        "signing",
        signing
    );

    benchmark_write_csv(
        CSV_FILE,
        "ML-DSA-65",
        "SIGNATURE",
        "verification",
        verification
    );

    free(public_key);
    free(secret_key);
    free(signature);

    OQS_SIG_free(sig);

    return 0;
}
