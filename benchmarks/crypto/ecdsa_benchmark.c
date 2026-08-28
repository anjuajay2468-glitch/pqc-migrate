#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#include <openssl/evp.h>
#include <openssl/ec.h>

#include "common/benchmark.h"

#define CSV_FILE "../results/crypto/baseline.csv"

static double elapsed_us(struct timespec start, struct timespec end)
{
    return (end.tv_sec - start.tv_sec) * 1000000.0 +
           (end.tv_nsec - start.tv_nsec) / 1000.0;
}

static EVP_PKEY *generate_key(void)
{
    EVP_PKEY_CTX *ctx =
        EVP_PKEY_CTX_new_id(EVP_PKEY_EC, NULL);

    if (!ctx)
        return NULL;

    if (EVP_PKEY_keygen_init(ctx) <= 0)
        goto error;

    if (EVP_PKEY_CTX_set_ec_paramgen_curve_nid(
            ctx, NID_X9_62_prime256v1) <= 0)
        goto error;

    EVP_PKEY *key = NULL;

    if (EVP_PKEY_keygen(ctx, &key) <= 0)
        key = NULL;

    EVP_PKEY_CTX_free(ctx);

    return key;

error:
    EVP_PKEY_CTX_free(ctx);
    return NULL;
}

static int sign_message(
    EVP_PKEY *key,
    const uint8_t *message,
    size_t message_len,
    uint8_t *signature,
    size_t *signature_len)
{
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();

    if (!ctx)
        return 0;

    if (EVP_DigestSignInit(
            ctx, NULL, EVP_sha256(), NULL, key) <= 0)
        goto error;

    if (EVP_DigestSignUpdate(
            ctx, message, message_len) <= 0)
        goto error;

    if (EVP_DigestSignFinal(
            ctx, signature, signature_len) <= 0)
        goto error;

    EVP_MD_CTX_free(ctx);
    return 1;

error:
    EVP_MD_CTX_free(ctx);
    return 0;
}

static int verify_signature(
    EVP_PKEY *key,
    const uint8_t *message,
    size_t message_len,
    const uint8_t *signature,
    size_t signature_len)
{
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();

    if (!ctx)
        return 0;

    if (EVP_DigestVerifyInit(
            ctx, NULL, EVP_sha256(), NULL, key) <= 0)
        goto error;

    if (EVP_DigestVerifyUpdate(
            ctx, message, message_len) <= 0)
        goto error;

    int result = EVP_DigestVerifyFinal(
        ctx,
        signature,
        signature_len);

    EVP_MD_CTX_free(ctx);

    return result == 1;

error:
    EVP_MD_CTX_free(ctx);
    return 0;
}

int main(void)
{
    const uint8_t message[] =
        "PQC-Migrate research benchmark message";

    const size_t message_len = sizeof(message) - 1;

    uint8_t signature[256];

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
    printf("       PQC-Migrate ECDSA P-256 Benchmark\n");
    printf("=============================================\n\n");

    printf("Iterations: %d\n\n", BENCHMARK_ITERATIONS);

    /* Warm-up */
    EVP_PKEY *warmup_key = generate_key();

    if (warmup_key)
    {
        size_t warmup_len = sizeof(signature);

        sign_message(
            warmup_key,
            message,
            message_len,
            signature,
            &warmup_len);

        verify_signature(
            warmup_key,
            message,
            message_len,
            signature,
            warmup_len);

        EVP_PKEY_free(warmup_key);
    }

    for (int i = 0; i < BENCHMARK_ITERATIONS; i++)
    {
        EVP_PKEY *key = NULL;
        size_t signature_len = sizeof(signature);

        /* Key generation */

        clock_gettime(CLOCK_MONOTONIC, &start);

        key = generate_key();

        clock_gettime(CLOCK_MONOTONIC, &end);

        if (!key)
        {
            fprintf(stderr, "Key generation failed\n");
            return 1;
        }

        double elapsed = elapsed_us(start, end);

        keygen_total += elapsed;

        if (elapsed < keygen_min)
            keygen_min = elapsed;

        if (elapsed > keygen_max)
            keygen_max = elapsed;

        /* Signing */

        clock_gettime(CLOCK_MONOTONIC, &start);

        if (!sign_message(
                key,
                message,
                message_len,
                signature,
                &signature_len))
        {
            fprintf(stderr, "Signing failed\n");
            EVP_PKEY_free(key);
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

        if (!verify_signature(
                key,
                message,
                message_len,
                signature,
                signature_len))
        {
            fprintf(stderr, "Signature verification failed\n");
            EVP_PKEY_free(key);
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        verify_total += elapsed;

        if (elapsed < verify_min)
            verify_min = elapsed;

        if (elapsed > verify_max)
            verify_max = elapsed;

        EVP_PKEY_free(key);
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
        "ECDSA-P256",
        "SIGNATURE",
        "keygen",
        keygen);

    benchmark_write_csv(
        CSV_FILE,
        "ECDSA-P256",
        "SIGNATURE",
        "signing",
        signing);

    benchmark_write_csv(
        CSV_FILE,
        "ECDSA-P256",
        "SIGNATURE",
        "verification",
        verification);

    return 0;
}
