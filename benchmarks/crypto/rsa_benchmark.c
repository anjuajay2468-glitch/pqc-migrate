#include <stdio.h>
#include <stdint.h>
#include <string.h>
#include <time.h>

#include <openssl/evp.h>
#include <openssl/rsa.h>
#include <openssl/err.h>

#include "common/benchmark.h"

#define CSV_FILE "../results/crypto/baseline.csv"

static double elapsed_us(struct timespec start, struct timespec end)
{
    return (end.tv_sec - start.tv_sec) * 1000000.0 +
           (end.tv_nsec - start.tv_nsec) / 1000.0;
}

static EVP_PKEY *generate_rsa_key(void)
{
    EVP_PKEY_CTX *ctx =
        EVP_PKEY_CTX_new_id(EVP_PKEY_RSA, NULL);

    if (!ctx)
        return NULL;

    if (EVP_PKEY_keygen_init(ctx) <= 0)
        goto error;

    if (EVP_PKEY_CTX_set_rsa_keygen_bits(ctx, 2048) <= 0)
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

static int encrypt_message(
    EVP_PKEY *key,
    const uint8_t *message,
    size_t message_len,
    uint8_t *ciphertext,
    size_t *ciphertext_len)
{
    EVP_PKEY_CTX *ctx =
        EVP_PKEY_CTX_new(key, NULL);

    if (!ctx)
        return 0;

    if (EVP_PKEY_encrypt_init(ctx) <= 0)
        goto error;

    if (EVP_PKEY_CTX_set_rsa_padding(
            ctx, RSA_PKCS1_OAEP_PADDING) <= 0)
        goto error;

    if (EVP_PKEY_CTX_set_rsa_oaep_md(
            ctx, EVP_sha256()) <= 0)
        goto error;

    if (EVP_PKEY_CTX_set_rsa_mgf1_md(
            ctx, EVP_sha256()) <= 0)
        goto error;

    if (EVP_PKEY_encrypt(
            ctx,
            ciphertext,
            ciphertext_len,
            message,
            message_len) <= 0)
        goto error;

    EVP_PKEY_CTX_free(ctx);
    return 1;

error:
    EVP_PKEY_CTX_free(ctx);
    return 0;
}

static int decrypt_message(
    EVP_PKEY *key,
    const uint8_t *ciphertext,
    size_t ciphertext_len,
    uint8_t *message,
    size_t *message_len)
{
    EVP_PKEY_CTX *ctx =
        EVP_PKEY_CTX_new(key, NULL);

    if (!ctx)
        return 0;

    if (EVP_PKEY_decrypt_init(ctx) <= 0)
        goto error;

    if (EVP_PKEY_CTX_set_rsa_padding(
            ctx, RSA_PKCS1_OAEP_PADDING) <= 0)
        goto error;

    if (EVP_PKEY_CTX_set_rsa_oaep_md(
            ctx, EVP_sha256()) <= 0)
        goto error;

    if (EVP_PKEY_CTX_set_rsa_mgf1_md(
            ctx, EVP_sha256()) <= 0)
        goto error;

    if (EVP_PKEY_decrypt(
            ctx,
            message,
            message_len,
            ciphertext,
            ciphertext_len) <= 0)
        goto error;

    EVP_PKEY_CTX_free(ctx);
    return 1;

error:
    EVP_PKEY_CTX_free(ctx);
    return 0;
}

int main(void)
{
    const uint8_t message[] =
        "PQC-Migrate RSA benchmark";

    const size_t message_len = sizeof(message) - 1;

    uint8_t ciphertext[256];
    uint8_t decrypted[256];

    double keygen_total = 0.0;
    double encrypt_total = 0.0;
    double decrypt_total = 0.0;

    double keygen_min = 1e30;
    double keygen_max = 0.0;

    double encrypt_min = 1e30;
    double encrypt_max = 0.0;

    double decrypt_min = 1e30;
    double decrypt_max = 0.0;

    struct timespec start, end;

    printf("=============================================\n");
    printf("       PQC-Migrate RSA-2048 Benchmark\n");
    printf("=============================================\n\n");

    printf("Iterations: %d\n\n", BENCHMARK_ITERATIONS);

    for (int i = 0; i < BENCHMARK_ITERATIONS; i++)
    {
        EVP_PKEY *key = NULL;
        size_t ciphertext_len = sizeof(ciphertext);
        size_t decrypted_len = sizeof(decrypted);

        /* Key generation */

        clock_gettime(CLOCK_MONOTONIC, &start);

        key = generate_rsa_key();

        clock_gettime(CLOCK_MONOTONIC, &end);

        if (!key)
        {
            fprintf(stderr, "RSA key generation failed\n");
            return 1;
        }

        double elapsed = elapsed_us(start, end);

        keygen_total += elapsed;

        if (elapsed < keygen_min)
            keygen_min = elapsed;

        if (elapsed > keygen_max)
            keygen_max = elapsed;

        /* Encryption */

        clock_gettime(CLOCK_MONOTONIC, &start);

        if (!encrypt_message(
                key,
                message,
                message_len,
                ciphertext,
                &ciphertext_len))
        {
            fprintf(stderr, "RSA encryption failed\n");
            EVP_PKEY_free(key);
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        encrypt_total += elapsed;

        if (elapsed < encrypt_min)
            encrypt_min = elapsed;

        if (elapsed > encrypt_max)
            encrypt_max = elapsed;

        /* Decryption */

        clock_gettime(CLOCK_MONOTONIC, &start);

        if (!decrypt_message(
                key,
                ciphertext,
                ciphertext_len,
                decrypted,
                &decrypted_len))
        {
            fprintf(stderr, "RSA decryption failed\n");
            EVP_PKEY_free(key);
            return 1;
        }

        clock_gettime(CLOCK_MONOTONIC, &end);

        elapsed = elapsed_us(start, end);

        decrypt_total += elapsed;

        if (elapsed < decrypt_min)
            decrypt_min = elapsed;

        if (elapsed > decrypt_max)
            decrypt_max = elapsed;

        /* Correctness */

        if (decrypted_len != message_len ||
            memcmp(
                decrypted,
                message,
                message_len) != 0)
        {
            fprintf(stderr,
                    "RSA plaintext mismatch at iteration %d\n",
                    i);

            EVP_PKEY_free(key);
            return 1;
        }

        EVP_PKEY_free(key);
    }

    BenchmarkResult keygen = {
        keygen_total / BENCHMARK_ITERATIONS,
        keygen_min,
        keygen_max
    };

    BenchmarkResult encryption = {
        encrypt_total / BENCHMARK_ITERATIONS,
        encrypt_min,
        encrypt_max
    };

    BenchmarkResult decryption = {
        decrypt_total / BENCHMARK_ITERATIONS,
        decrypt_min,
        decrypt_max
    };

    printf("RESULTS\n");
    printf("---------------------------------------------\n");

    printf("Key Generation\n");
    printf("  Average: %.3f us\n", keygen.average_us);
    printf("  Minimum: %.3f us\n", keygen.minimum_us);
    printf("  Maximum: %.3f us\n\n", keygen.maximum_us);

    printf("Encryption\n");
    printf("  Average: %.3f us\n", encryption.average_us);
    printf("  Minimum: %.3f us\n", encryption.minimum_us);
    printf("  Maximum: %.3f us\n\n", encryption.maximum_us);

    printf("Decryption\n");
    printf("  Average: %.3f us\n", decryption.average_us);
    printf("  Minimum: %.3f us\n", decryption.minimum_us);
    printf("  Maximum: %.3f us\n\n", decryption.maximum_us);

    printf("All plaintext checks: SUCCESS\n");

    benchmark_write_csv(
        CSV_FILE,
        "RSA-2048",
        "KEM",
        "keygen",
        keygen
    );

    benchmark_write_csv(
        CSV_FILE,
        "RSA-2048",
        "KEM",
        "encryption",
        encryption
    );

    benchmark_write_csv(
        CSV_FILE,
        "RSA-2048",
        "KEM",
        "decryption",
        decryption
    );

    return 0;
}
