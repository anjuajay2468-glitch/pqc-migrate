#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <oqs/oqs.h>
#include <openssl/evp.h>

#define X25519_SECRET_LEN 32
#define HYBRID_SECRET_LEN 32
#define VALIDATION_ITERATIONS 100

static const unsigned char HYBRID_LABEL[] =
    "PQC-Migrate-HYBRID-X25519-MLKEM768";


/*
 * ============================================================
 * Combine X25519 and ML-KEM shared secrets.
 *
 * hybrid_secret =
 *
 * SHA-256(
 *     domain_label ||
 *     X25519_shared_secret ||
 *     ML-KEM_shared_secret
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
    int success = 0;

    if (EVP_DigestInit_ex(ctx, EVP_sha256(), NULL) != 1) {
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

    success = (digest_len == HYBRID_SECRET_LEN);

cleanup:
    EVP_MD_CTX_free(ctx);
    return success;
}


/*
 * ============================================================
 * Generate one X25519 key pair.
 * ============================================================
 */
static int generate_x25519_key(EVP_PKEY **key)
{
    EVP_PKEY_CTX *ctx =
        EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);

    if (ctx == NULL) {
        return 0;
    }

    int success = 0;

    if (EVP_PKEY_keygen_init(ctx) <= 0) {
        goto cleanup;
    }

    if (EVP_PKEY_keygen(ctx, key) <= 0) {
        goto cleanup;
    }

    success = 1;

cleanup:
    EVP_PKEY_CTX_free(ctx);
    return success;
}


/*
 * ============================================================
 * Derive X25519 shared secret.
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

    int success = 0;

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

    success = 1;

cleanup:
    EVP_PKEY_CTX_free(ctx);
    return success;
}


int main(void)
{
    printf("=============================================\n");
    printf("   PQC-Migrate Hybrid Validation\n");
    printf("=============================================\n\n");

    printf("Configuration\n");
    printf("---------------------------------------------\n");
    printf("Classical component:       X25519\n");
    printf("PQC component:             ML-KEM-768\n");
    printf("Combination:               SHA-256\n");
    printf("Validation iterations:    %d\n\n",
           VALIDATION_ITERATIONS);


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
     * Counters
     * ========================================================
     */

    int x25519_successes = 0;
    int mlkem_successes = 0;
    int hybrid_successes = 0;

    int x25519_tamper_passes = 0;
    int mlkem_tamper_passes = 0;


    /*
     * ========================================================
     * Repeated validation
     * ========================================================
     */

    for (int iteration = 0;
         iteration < VALIDATION_ITERATIONS;
         iteration++) {

        EVP_PKEY *alice_key = NULL;
        EVP_PKEY *bob_key = NULL;


        /*
         * ----------------------------------------------------
         * X25519 key generation
         * ----------------------------------------------------
         */

        if (!generate_x25519_key(&alice_key) ||
            !generate_x25519_key(&bob_key)) {

            fprintf(
                stderr,
                "ERROR: X25519 key generation failed "
                "at iteration %d.\n",
                iteration + 1
            );

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);
            goto failure;
        }


        /*
         * ----------------------------------------------------
         * X25519 shared secrets
         * ----------------------------------------------------
         */

        unsigned char alice_x25519[
            X25519_SECRET_LEN
        ];

        unsigned char bob_x25519[
            X25519_SECRET_LEN
        ];

        size_t alice_x25519_len =
            sizeof(alice_x25519);

        size_t bob_x25519_len =
            sizeof(bob_x25519);


        if (!derive_x25519(
                alice_key,
                bob_key,
                alice_x25519,
                &alice_x25519_len
            )) {

            fprintf(
                stderr,
                "ERROR: Alice X25519 derivation failed "
                "at iteration %d.\n",
                iteration + 1
            );

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);
            goto failure;
        }


        if (!derive_x25519(
                bob_key,
                alice_key,
                bob_x25519,
                &bob_x25519_len
            )) {

            fprintf(
                stderr,
                "ERROR: Bob X25519 derivation failed "
                "at iteration %d.\n",
                iteration + 1
            );

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);
            goto failure;
        }


        int x25519_match =
            alice_x25519_len == bob_x25519_len &&
            memcmp(
                alice_x25519,
                bob_x25519,
                X25519_SECRET_LEN
            ) == 0;

        if (x25519_match) {
            x25519_successes++;
        }


        /*
         * ----------------------------------------------------
         * ML-KEM key generation
         * ----------------------------------------------------
         */

        unsigned char *public_key =
            malloc(kem->length_public_key);

        unsigned char *secret_key =
            malloc(kem->length_secret_key);

        unsigned char *ciphertext =
            malloc(kem->length_ciphertext);

        unsigned char *alice_mlkem =
            malloc(kem->length_shared_secret);

        unsigned char *bob_mlkem =
            malloc(kem->length_shared_secret);


        if (public_key == NULL ||
            secret_key == NULL ||
            ciphertext == NULL ||
            alice_mlkem == NULL ||
            bob_mlkem == NULL) {

            fprintf(
                stderr,
                "ERROR: ML-KEM allocation failed "
                "at iteration %d.\n",
                iteration + 1
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(alice_mlkem);
            free(bob_mlkem);

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
                "ERROR: ML-KEM key generation failed "
                "at iteration %d.\n",
                iteration + 1
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(alice_mlkem);
            free(bob_mlkem);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        /*
         * ML-KEM encapsulation.
         *
         * bob_mlkem becomes the encapsulator secret.
         */

        if (OQS_KEM_encaps(
                kem,
                ciphertext,
                bob_mlkem,
                public_key
            ) != OQS_SUCCESS) {

            fprintf(
                stderr,
                "ERROR: ML-KEM encapsulation failed "
                "at iteration %d.\n",
                iteration + 1
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(alice_mlkem);
            free(bob_mlkem);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        /*
         * ML-KEM decapsulation.
         */

        if (OQS_KEM_decaps(
                kem,
                alice_mlkem,
                ciphertext,
                secret_key
            ) != OQS_SUCCESS) {

            fprintf(
                stderr,
                "ERROR: ML-KEM decapsulation failed "
                "at iteration %d.\n",
                iteration + 1
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(alice_mlkem);
            free(bob_mlkem);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        int mlkem_match =
            memcmp(
                alice_mlkem,
                bob_mlkem,
                kem->length_shared_secret
            ) == 0;

        if (mlkem_match) {
            mlkem_successes++;
        }


        /*
         * ----------------------------------------------------
         * Hybrid secret
         * ----------------------------------------------------
         */

        unsigned char alice_hybrid[
            HYBRID_SECRET_LEN
        ];

        unsigned char bob_hybrid[
            HYBRID_SECRET_LEN
        ];


        if (!combine_secrets(
                alice_x25519,
                X25519_SECRET_LEN,
                alice_mlkem,
                kem->length_shared_secret,
                alice_hybrid
            ) ||
            !combine_secrets(
                bob_x25519,
                X25519_SECRET_LEN,
                bob_mlkem,
                kem->length_shared_secret,
                bob_hybrid
            )) {

            fprintf(
                stderr,
                "ERROR: Hybrid construction failed "
                "at iteration %d.\n",
                iteration + 1
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(alice_mlkem);
            free(bob_mlkem);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        int hybrid_match =
            memcmp(
                alice_hybrid,
                bob_hybrid,
                HYBRID_SECRET_LEN
            ) == 0;

        if (hybrid_match) {
            hybrid_successes++;
        }


        /*
         * ----------------------------------------------------
         * Tampering test: X25519 contribution
         * ----------------------------------------------------
         */

        unsigned char tampered_x25519[
            X25519_SECRET_LEN
        ];

        memcpy(
            tampered_x25519,
            alice_x25519,
            X25519_SECRET_LEN
        );

        tampered_x25519[0] ^= 0x01;


        unsigned char tampered_x25519_hybrid[
            HYBRID_SECRET_LEN
        ];


        if (!combine_secrets(
                tampered_x25519,
                X25519_SECRET_LEN,
                alice_mlkem,
                kem->length_shared_secret,
                tampered_x25519_hybrid
            )) {

            fprintf(
                stderr,
                "ERROR: X25519 tampering test failed "
                "to execute at iteration %d.\n",
                iteration + 1
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(alice_mlkem);
            free(bob_mlkem);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        if (memcmp(
                alice_hybrid,
                tampered_x25519_hybrid,
                HYBRID_SECRET_LEN
            ) != 0) {

            x25519_tamper_passes++;
        }


        /*
         * ----------------------------------------------------
         * Tampering test: ML-KEM contribution
         * ----------------------------------------------------
         */

        unsigned char *tampered_mlkem =
            malloc(kem->length_shared_secret);

        if (tampered_mlkem == NULL) {

            fprintf(
                stderr,
                "ERROR: ML-KEM tampering allocation failed.\n"
            );

            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(alice_mlkem);
            free(bob_mlkem);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        memcpy(
            tampered_mlkem,
            alice_mlkem,
            kem->length_shared_secret
        );

        tampered_mlkem[0] ^= 0x01;


        unsigned char tampered_mlkem_hybrid[
            HYBRID_SECRET_LEN
        ];


        if (!combine_secrets(
                alice_x25519,
                X25519_SECRET_LEN,
                tampered_mlkem,
                kem->length_shared_secret,
                tampered_mlkem_hybrid
            )) {

            fprintf(
                stderr,
                "ERROR: ML-KEM tampering test failed "
                "to execute at iteration %d.\n",
                iteration + 1
            );

            free(tampered_mlkem);
            free(public_key);
            free(secret_key);
            free(ciphertext);
            free(alice_mlkem);
            free(bob_mlkem);

            EVP_PKEY_free(alice_key);
            EVP_PKEY_free(bob_key);

            goto failure;
        }


        if (memcmp(
                alice_hybrid,
                tampered_mlkem_hybrid,
                HYBRID_SECRET_LEN
            ) != 0) {

            mlkem_tamper_passes++;
        }


        /*
         * Cleanup iteration.
         */

        free(tampered_mlkem);
        free(public_key);
        free(secret_key);
        free(ciphertext);
        free(alice_mlkem);
        free(bob_mlkem);

        EVP_PKEY_free(alice_key);
        EVP_PKEY_free(bob_key);
    }


    /*
     * ========================================================
     * Results
     * ========================================================
     */

    printf("VALIDATION RESULTS\n");
    printf("---------------------------------------------\n");

    printf(
        "X25519 agreement:              %d / %d\n",
        x25519_successes,
        VALIDATION_ITERATIONS
    );

    printf(
        "ML-KEM agreement:              %d / %d\n",
        mlkem_successes,
        VALIDATION_ITERATIONS
    );

    printf(
        "Hybrid agreement:              %d / %d\n",
        hybrid_successes,
        VALIDATION_ITERATIONS
    );

    printf(
        "X25519 tampering detected:     %d / %d\n",
        x25519_tamper_passes,
        VALIDATION_ITERATIONS
    );

    printf(
        "ML-KEM tampering detected:     %d / %d\n",
        mlkem_tamper_passes,
        VALIDATION_ITERATIONS
    );


    /*
     * ========================================================
     * Final evaluation
     * ========================================================
     */

    int validation_success =
        x25519_successes == VALIDATION_ITERATIONS &&
        mlkem_successes == VALIDATION_ITERATIONS &&
        hybrid_successes == VALIDATION_ITERATIONS &&
        x25519_tamper_passes == VALIDATION_ITERATIONS &&
        mlkem_tamper_passes == VALIDATION_ITERATIONS;


    printf("\nFINAL RESULT\n");
    printf("---------------------------------------------\n");

    if (validation_success) {
        printf(
            "ALL HYBRID VALIDATION CHECKS: SUCCESS\n"
        );
    } else {
        printf(
            "HYBRID VALIDATION CHECKS: FAILED\n"
        );
    }


    OQS_KEM_free(kem);

    return validation_success
        ? EXIT_SUCCESS
        : EXIT_FAILURE;


failure:

    OQS_KEM_free(kem);

    return EXIT_FAILURE;
}
