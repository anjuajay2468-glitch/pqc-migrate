#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>

#include <oqs/oqs.h>
#include <openssl/evp.h>

#define ITERATIONS 1000
#define X25519_SECRET_LEN 32
#define HYBRID_SECRET_LEN 32

static const unsigned char HYBRID_LABEL[] =
    "PQC-Migrate-HYBRID-X25519-MLKEM768";


static double elapsed_us(
    struct timespec *start,
    struct timespec *end
) {
    double seconds =
        (double)(end->tv_sec - start->tv_sec);

    double nanoseconds =
        (double)(end->tv_nsec - start->tv_nsec);

    return (seconds * 1000000.0) +
           (nanoseconds / 1000.0);
}


/*
 * ============================================================
 * X25519 key generation
 * ============================================================
 */
static int generate_x25519_key(EVP_PKEY **key)
{
    EVP_PKEY_CTX *ctx =
        EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);

    if (ctx == NULL) {
        return 0;
    }

    int result = 0;

    if (EVP_PKEY_keygen_init(ctx) <= 0) {
        goto cleanup;
    }

    if (EVP_PKEY_keygen(ctx, key) <= 0) {
        goto cleanup;
    }

    result = 1;

cleanup:
    EVP_PKEY_CTX_free(ctx);
    return result;
}


/*
 * ============================================================
 * X25519 shared-secret derivation
 * ============================================================
 */
static int derive_x25519(
    EVP_PKEY *private_key,
    EVP_PKEY *peer_key,
    unsigned char *secret,
    size_t *secret_len
) {
    EVP_PKEY_CTX *ctx =
        EVP_PKEY_CTX_new(private_key, NULL);

    if (ctx == NULL) {
        return 0;
    }

    int result = 0;

    if (EVP_PKEY_derive_init(ctx) <= 0) {
        goto cleanup;
    }

    if (EVP_PKEY_derive_set_peer(ctx, peer_key) <= 0) {
        goto cleanup;
    }

    if (EVP_PKEY_derive(
            ctx,
            secret,
            secret_len
        ) <= 0) {
        goto cleanup;
    }

    result = 1;

cleanup:
    EVP_PKEY_CTX_free(ctx);
    return result;
}


/*
 * ============================================================
 * Hybrid secret construction
 *
 * SHA-256(
 *     domain_label ||
 *     X25519_secret ||
 *     ML-KEM_secret
 * )
 * ============================================================
 */
static int combine_secrets(
    const unsigned char *x25519_secret,
    size_t x25519_len,
    const unsigned char *mlkem_secret,
    size_t mlkem_len,
    unsigned char *hybrid_secret
) {
    EVP_MD_CTX *ctx = EVP_MD_CTX_new();

    if (ctx == NULL) {
        return 0;
    }

    unsigned int digest_len = 0;
    int result = 0;

    if (EVP_DigestInit_ex(
            ctx,
            EVP_sha256(),
            NULL
        ) != 1) {
        goto cleanup;
    }

    if (EVP_DigestUpdate(
            ctx,
            HYBRID_LABEL,
            sizeof(HYBRID_LABEL) - 1
        ) != 1) {
        goto cleanup;
    }

    if (EVP_DigestUpdate(
            ctx,
            x25519_secret,
            x25519_len
        ) != 1) {
        goto cleanup;
    }

    if (EVP_DigestUpdate(
            ctx,
            mlkem_secret,
            mlkem_len
        ) != 1) {
        goto cleanup;
    }

    if (EVP_DigestFinal_ex(
            ctx,
            hybrid_secret,
            &digest_len
        ) != 1) {
        goto cleanup;
    }

    result =
        digest_len == HYBRID_SECRET_LEN;

cleanup:
    EVP_MD_CTX_free(ctx);
    return result;
}


int main(void)
{
    printf("=============================================\n");
    printf("   PQC-Migrate Hybrid Performance Benchmark\n");
    printf("=============================================\n\n");

    printf("Configuration\n");
    printf("---------------------------------------------\n");
    printf("Classical component:       X25519\n");
    printf("PQC component:             ML-KEM-768\n");
    printf("Combination:               SHA-256\n");
    printf("Iterations:                %d\n\n",
           ITERATIONS);


    /*
     * ========================================================
     * Initialize ML-KEM
     * ========================================================
     */

    OQS_KEM *kem =
        OQS_KEM_new(OQS_KEM_alg_ml_kem_768);

    if (kem == NULL) {
        fprintf(
            stderr,
            "ERROR: ML-KEM-768 unavailable.\n"
        );

        return EXIT_FAILURE;
    }


    /*
     * ========================================================
     * Accumulators
     * ========================================================
     */

    double x25519_total = 0.0;
    double x25519_min = 1e30;
    double x25519_max = 0.0;

    double mlkem_total = 0.0;
    double mlkem_min = 1e30;
    double mlkem_max = 0.0;

    double hybrid_total = 0.0;
    double hybrid_min = 1e30;
    double hybrid_max = 0.0;

    double combined_total = 0.0;
    double combined_min = 1e30;
    double combined_max = 0.0;

    int successful = 0;


    /*
     * ========================================================
     * Benchmark loop
     * ========================================================
     */

    for (int i = 0; i < ITERATIONS; i++) {

        struct timespec start;
        struct timespec end;


        /*
         * ----------------------------------------------------
         * X25519 setup
         * ----------------------------------------------------
         */

        EVP_PKEY *alice_key = NULL;
        EVP_PKEY *bob_key = NULL;

        if (!generate_x25519_key(&alice_key) ||
            !generate_x25519_key(&bob_key)) {

            fprintf(
                stderr,
                "ERROR: X25519 key generation failed "
                "at iteration %d.\n",
                i + 1
            );

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);
            goto failure;
        }


        unsigned char x25519_secret[
            X25519_SECRET_LEN
        ];

        size_t x25519_secret_len =
            sizeof(x25519_secret);


        /*
         * ----------------------------------------------------
         * X25519 benchmark
         * ----------------------------------------------------
         */

        clock_gettime(
            CLOCK_MONOTONIC,
            &start
        );

        int x25519_ok =
            derive_x25519(
                alice_key,
                bob_key,
                x25519_secret,
                &x25519_secret_len
            );

        clock_gettime(
            CLOCK_MONOTONIC,
            &end
        );

        if (!x25519_ok ||
            x25519_secret_len != X25519_SECRET_LEN) {

            fprintf(
                stderr,
                "ERROR: X25519 derivation failed "
                "at iteration %d.\n",
                i + 1
            );

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);
            goto failure;
        }


        double x25519_time =
            elapsed_us(&start, &end);

        x25519_total += x25519_time;

        if (x25519_time < x25519_min)
            x25519_min = x25519_time;

        if (x25519_time > x25519_max)
            x25519_max = x25519_time;


        /*
         * ----------------------------------------------------
         * ML-KEM setup
         * ----------------------------------------------------
         */

        unsigned char *public_key =
            malloc(kem->length_public_key);

        unsigned char *secret_key =
            malloc(kem->length_secret_key);

        unsigned char *ciphertext =
            malloc(kem->length_ciphertext);

        unsigned char *mlkem_secret =
            malloc(kem->length_shared_secret);


        if (public_key == NULL ||
            secret_key == NULL ||
            ciphertext == NULL ||
            mlkem_secret == NULL) {

            fprintf(
                stderr,
                "ERROR: ML-KEM allocation failed.\n"
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(mlkem_secret);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        if (OQS_KEM_keypair(
                kem,
                public_key,
                secret_key
            ) != OQS_SUCCESS) {

            fprintf(
                stderr,
                "ERROR: ML-KEM key generation failed.\n"
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(mlkem_secret);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        /*
         * ----------------------------------------------------
         * ML-KEM encapsulation + decapsulation
         *
         * The timing below covers the complete ML-KEM
         * key-establishment operation.
         * ----------------------------------------------------
         */

        unsigned char *encapsulated_secret =
            malloc(kem->length_shared_secret);

        if (encapsulated_secret == NULL) {

            fprintf(
                stderr,
                "ERROR: ML-KEM secret allocation failed.\n"
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(mlkem_secret);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        clock_gettime(
            CLOCK_MONOTONIC,
            &start
        );

        int encaps_ok =
            OQS_KEM_encaps(
                kem,
                ciphertext,
                encapsulated_secret,
                public_key
            );

        int decaps_ok =
            encaps_ok == OQS_SUCCESS
                ? OQS_KEM_decaps(
                    kem,
                    mlkem_secret,
                    ciphertext,
                    secret_key
                )
                : OQS_ERROR;

        clock_gettime(
            CLOCK_MONOTONIC,
            &end
        );


        if (encaps_ok != OQS_SUCCESS ||
            decaps_ok != OQS_SUCCESS ||
            memcmp(
                encapsulated_secret,
                mlkem_secret,
                kem->length_shared_secret
            ) != 0) {

            fprintf(
                stderr,
                "ERROR: ML-KEM operation failed "
                "at iteration %d.\n",
                i + 1
            );

            free(encapsulated_secret);
            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(mlkem_secret);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        double mlkem_time =
            elapsed_us(&start, &end);

        mlkem_total += mlkem_time;

        if (mlkem_time < mlkem_min)
            mlkem_min = mlkem_time;

        if (mlkem_time > mlkem_max)
            mlkem_max = mlkem_time;


        /*
         * ----------------------------------------------------
         * Hybrid combination benchmark
         * ----------------------------------------------------
         */

        unsigned char hybrid_secret[
            HYBRID_SECRET_LEN
        ];


        clock_gettime(
            CLOCK_MONOTONIC,
            &start
        );

        int hybrid_ok =
            combine_secrets(
                x25519_secret,
                X25519_SECRET_LEN,
                mlkem_secret,
                kem->length_shared_secret,
                hybrid_secret
            );

        clock_gettime(
            CLOCK_MONOTONIC,
            &end
        );


        if (!hybrid_ok) {

            fprintf(
                stderr,
                "ERROR: Hybrid construction failed "
                "at iteration %d.\n",
                i + 1
            );

            free(encapsulated_secret);
            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(mlkem_secret);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        double hybrid_time =
            elapsed_us(&start, &end);

        hybrid_total += hybrid_time;

        if (hybrid_time < hybrid_min)
            hybrid_min = hybrid_time;

        if (hybrid_time > hybrid_max)
            hybrid_max = hybrid_time;


        /*
         * ----------------------------------------------------
         * Total combined operation
         *
         * X25519 + ML-KEM + hybrid combination
         * ----------------------------------------------------
         */

        double combined_time =
            x25519_time +
            mlkem_time +
            hybrid_time;

        combined_total += combined_time;

        if (combined_time < combined_min)
            combined_min = combined_time;

        if (combined_time > combined_max)
            combined_max = combined_time;


        successful++;


        /*
         * Cleanup
         */

        free(encapsulated_secret);
        free(public_key);
        free(secret_key);
        free(ciphertext);
        free(mlkem_secret);

        EVP_PKEY_free(alice_key);
        EVP_PKEY_free(bob_key);
    }


    /*
     * ========================================================
     * Results
     * ========================================================
     */

    printf("RESULTS\n");
    printf("---------------------------------------------\n");

    printf("Successful iterations: %d / %d\n\n",
           successful,
           ITERATIONS);


    printf("X25519\n");
    printf("  Average: %.3f us\n",
           x25519_total / ITERATIONS);

    printf("  Minimum: %.3f us\n",
           x25519_min);

    printf("  Maximum: %.3f us\n\n",
           x25519_max);


    printf("ML-KEM-768\n");
    printf("  Average: %.3f us\n",
           mlkem_total / ITERATIONS);

    printf("  Minimum: %.3f us\n",
           mlkem_min);

    printf("  Maximum: %.3f us\n\n",
           mlkem_max);


    printf("Hybrid combination\n");
    printf("  Average: %.3f us\n",
           hybrid_total / ITERATIONS);

    printf("  Minimum: %.3f us\n",
           hybrid_min);

    printf("  Maximum: %.3f us\n\n",
           hybrid_max);


    printf("Total hybrid operation\n");
    printf("  Average: %.3f us\n",
           combined_total / ITERATIONS);

    printf("  Minimum: %.3f us\n",
           combined_min);

    printf("  Maximum: %.3f us\n\n",
           combined_max);


    /*
     * ========================================================
     * Final validation
     * ========================================================
     */

    printf("FINAL RESULT\n");
    printf("---------------------------------------------\n");

    if (successful == ITERATIONS) {

        printf(
            "ALL HYBRID PERFORMANCE CHECKS: SUCCESS\n"
        );

    } else {

        printf(
            "HYBRID PERFORMANCE CHECKS: FAILED\n"
        );
    }


    OQS_KEM_free(kem);

    return successful == ITERATIONS
        ? EXIT_SUCCESS
        : EXIT_FAILURE;


failure:

    OQS_KEM_free(kem);

    return EXIT_FAILURE;
}
