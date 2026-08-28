#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#include <openssl/evp.h>
#include "common/benchmark.h"

#define CSV_FILE "../results/crypto/baseline.csv"

static double elapsed_us(struct timespec start, struct timespec end)
{
    return (end.tv_sec - start.tv_sec) * 1000000.0 +
           (end.tv_nsec - start.tv_nsec) / 1000.0;
}

static int generate_keypair(EVP_PKEY **key)
{
    EVP_PKEY_CTX *ctx =
        EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);

    if (!ctx)
        return 0;

    if (EVP_PKEY_keygen_init(ctx) <= 0)
    {
        EVP_PKEY_CTX_free(ctx);
        return 0;
    }

    if (EVP_PKEY_keygen(ctx, key) <= 0)
    {
        EVP_PKEY_CTX_free(ctx);
        return 0;
    }

    EVP_PKEY_CTX_free(ctx);
    return 1;
}

static int derive_secret(
    EVP_PKEY *private_key,
    EVP_PKEY *peer_public_key,
    uint8_t *secret,
    size_t *secret_len)
{
    EVP_PKEY_CTX *ctx =
        EVP_PKEY_CTX_new(private_key, NULL);

    if (!ctx)
        return 0;

    if (EVP_PKEY_derive_init(ctx) <= 0 ||
        EVP_PKEY_derive_set_peer(ctx, peer_public_key) <= 0)
    {
        EVP_PKEY_CTX_free(ctx);
        return 0;
    }

    if (EVP_PKEY_derive(ctx, NULL, secret_len) <= 0)
    {
        EVP_PKEY_CTX_free(ctx);
        return 0;
    }

    if (EVP_PKEY_derive(ctx, secret, secret_len) <= 0)
    {
        EVP_PKEY_CTX_free(ctx);
        return 0;
    }

    EVP_PKEY_CTX_free(ctx);
    return 1;
}

int main(void)
{
    double keygen_total = 0.0;
    double derive_total = 0.0;

    double keygen_min = 1e30;
    double keygen_max = 0.0;

    double derive_min = 1e30;
    double derive_max = 0.0;

    struct timespec start, end;

    printf("=============================================\n");
    printf("       PQC-Migrate X25519 Benchmark\n");
    printf("=============================================\n\n");

    printf("Iterations: %d\n\n", BENCHMARK_ITERATIONS);

    for (int i = 0; i < BENCHMARK_ITERATIONS; i++)
    {
        EVP_PKEY *alice = NULL;
        EVP_PKEY *bob = NULL;

        uint8_t alice_secret[32];
        uint8_t bob_secret[32];

        size_t alice_secret_len = sizeof(alice_secret);
        size_t bob_secret_len = sizeof(bob_secret);

        /* Key generation */

        clock_gettime(CLOCK_MONOTONIC, &start);

        if (!generate_keypair(&alice) ||
            !generate_keypair(&bob))
        {
            fprintf(stderr, "Key generation failed\n");
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        double elapsed = elapsed_us(start, end);

        keygen_total += elapsed;

        if (elapsed < keygen_min)
            keygen_min = elapsed;

        if (elapsed > keygen_max)
            keygen_max = elapsed;

        /* Shared-secret derivation */

        clock_gettime(CLOCK_MONOTONIC, &start);

        if (!derive_secret(
                alice,
                bob,
                alice_secret,
                &alice_secret_len))
        {
            fprintf(stderr, "Alice derivation failed\n");
            return 1;
        }

        if (!derive_secret(
                bob,
                alice,
                bob_secret,
                &bob_secret_len))
        {
            fprintf(stderr, "Bob derivation failed\n");
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        derive_total += elapsed;

        if (elapsed < derive_min)
            derive_min = elapsed;

        if (elapsed > derive_max)
            derive_max = elapsed;

        /* Correctness */

        if (alice_secret_len != bob_secret_len ||
            memcmp(
                alice_secret,
                bob_secret,
                alice_secret_len) != 0)
        {
            fprintf(stderr,
                    "Shared-secret mismatch at iteration %d\n",
                    i);

            return 1;
        }

        EVP_PKEY_free(alice);
        EVP_PKEY_free(bob);
    }

    BenchmarkResult keygen = {
        keygen_total / BENCHMARK_ITERATIONS,
        keygen_min,
        keygen_max
    };

    BenchmarkResult derive = {
        derive_total / BENCHMARK_ITERATIONS,
        derive_min,
        derive_max
    };

    printf("RESULTS\n");
    printf("---------------------------------------------\n");

    printf("Key Generation (Alice + Bob)\n");
    printf("  Average: %.3f us\n", keygen.average_us);
    printf("  Minimum: %.3f us\n", keygen.minimum_us);
    printf("  Maximum: %.3f us\n\n", keygen.maximum_us);

    printf("Shared Secret Derivation (Alice + Bob)\n");
    printf("  Average: %.3f us\n", derive.average_us);
    printf("  Minimum: %.3f us\n", derive.minimum_us);
    printf("  Maximum: %.3f us\n\n", derive.maximum_us);

    printf("All shared-secret checks: SUCCESS\n");

    benchmark_write_csv(
        CSV_FILE,
        "X25519",
        "KEM",
        "keygen",
        keygen);

    benchmark_write_csv(
        CSV_FILE,
        "X25519",
        "KEM",
        "derivation",
        derive);

    return 0;
}
