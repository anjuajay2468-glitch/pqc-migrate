#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#include <oqs/oqs.h>
#include <openssl/evp.h>

#define X25519_SECRET_LEN 32
#define HYBRID_SECRET_LEN 32

static const unsigned char HYBRID_LABEL[] =
    "PQC-Migrate-HYBRID-X25519-MLKEM768";


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

    int success = 0;
    unsigned int digest_len = 0;

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


static int combine_with_label(
    const unsigned char *label,
    size_t label_len,
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

    int success = 0;
    unsigned int digest_len = 0;

    if (EVP_DigestInit_ex(ctx, EVP_sha256(), NULL) != 1) {
        goto cleanup;
    }

    if (EVP_DigestUpdate(
            ctx,
            label,
            label_len
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


static void print_hex(
    const unsigned char *data,
    size_t len
) {
    for (size_t i = 0; i < len; i++) {
        printf("%02x", data[i]);
    }

    printf("\n");
}


static int secrets_equal(
    const unsigned char *a,
    const unsigned char *b,
    size_t len
) {
    return memcmp(a, b, len) == 0;
}


int main(void) {

    printf("=============================================\n");
    printf("   PQC-Migrate Hybrid Secret Construction\n");
    printf("=============================================\n\n");


    /*
     * ========================================================
     * ML-KEM initialization
     * ========================================================
     */

    OQS_KEM *kem = OQS_KEM_new(OQS_KEM_alg_ml_kem_768);

    if (kem == NULL) {
        fprintf(stderr,
                "ERROR: ML-KEM-768 is unavailable.\n");
        return EXIT_FAILURE;
    }


    /*
     * ========================================================
     * X25519 key generation
     * ========================================================
     */

    EVP_PKEY_CTX *alice_ctx =
        EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);

    EVP_PKEY_CTX *bob_ctx =
        EVP_PKEY_CTX_new_id(EVP_PKEY_X25519, NULL);

    EVP_PKEY *alice_key = NULL;
    EVP_PKEY *bob_key = NULL;
    EVP_PKEY_CTX *derive_ctx = NULL;

    if (alice_ctx == NULL ||
        bob_ctx == NULL) {

        fprintf(stderr,
                "ERROR: X25519 context creation failed.\n");

        goto failure;
    }

    if (EVP_PKEY_keygen_init(alice_ctx) <= 0 ||
        EVP_PKEY_keygen(alice_ctx, &alice_key) <= 0) {

        fprintf(stderr,
                "ERROR: Alice X25519 key generation failed.\n");

        goto failure;
    }

    if (EVP_PKEY_keygen_init(bob_ctx) <= 0 ||
        EVP_PKEY_keygen(bob_ctx, &bob_key) <= 0) {

        fprintf(stderr,
                "ERROR: Bob X25519 key generation failed.\n");

        goto failure;
    }


    /*
     * ========================================================
     * X25519 shared-secret derivation
     * ========================================================
     */

    unsigned char alice_x25519[X25519_SECRET_LEN];
    unsigned char bob_x25519[X25519_SECRET_LEN];

    size_t alice_x25519_len =
        sizeof(alice_x25519);

    size_t bob_x25519_len =
        sizeof(bob_x25519);


    derive_ctx =
        EVP_PKEY_CTX_new(alice_key, NULL);

    if (derive_ctx == NULL ||
        EVP_PKEY_derive_init(derive_ctx) <= 0 ||
        EVP_PKEY_derive_set_peer(
            derive_ctx,
            bob_key
        ) <= 0 ||
        EVP_PKEY_derive(
            derive_ctx,
            alice_x25519,
            &alice_x25519_len
        ) <= 0) {

        fprintf(stderr,
                "ERROR: Alice X25519 derivation failed.\n");

        goto failure;
    }

    EVP_PKEY_CTX_free(derive_ctx);
    derive_ctx = NULL;


    derive_ctx =
        EVP_PKEY_CTX_new(bob_key, NULL);

    if (derive_ctx == NULL ||
        EVP_PKEY_derive_init(derive_ctx) <= 0 ||
        EVP_PKEY_derive_set_peer(
            derive_ctx,
            alice_key
        ) <= 0 ||
        EVP_PKEY_derive(
            derive_ctx,
            bob_x25519,
            &bob_x25519_len
        ) <= 0) {

        fprintf(stderr,
                "ERROR: Bob X25519 derivation failed.\n");

        goto failure;
    }

    EVP_PKEY_CTX_free(derive_ctx);
    derive_ctx = NULL;


    /*
     * ========================================================
     * ML-KEM memory allocation
     * ========================================================
     */

    unsigned char *mlkem_public_key =
        malloc(kem->length_public_key);

    unsigned char *mlkem_secret_key =
        malloc(kem->length_secret_key);

    unsigned char *mlkem_ciphertext =
        malloc(kem->length_ciphertext);

    unsigned char *alice_mlkem_secret =
        malloc(kem->length_shared_secret);

    unsigned char *bob_mlkem_secret =
        malloc(kem->length_shared_secret);


    if (mlkem_public_key == NULL ||
        mlkem_secret_key == NULL ||
        mlkem_ciphertext == NULL ||
        alice_mlkem_secret == NULL ||
        bob_mlkem_secret == NULL) {

        fprintf(stderr,
                "ERROR: ML-KEM memory allocation failed.\n");

        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }


    /*
     * ========================================================
     * ML-KEM key generation
     * ========================================================
     */

    if (OQS_KEM_keypair(
            kem,
            mlkem_public_key,
            mlkem_secret_key
        ) != OQS_SUCCESS) {

        fprintf(stderr,
                "ERROR: ML-KEM key generation failed.\n");

        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }


    /*
     * ========================================================
     * ML-KEM encapsulation
     * ========================================================
     */

    if (OQS_KEM_encaps(
            kem,
            mlkem_ciphertext,
            bob_mlkem_secret,
            mlkem_public_key
        ) != OQS_SUCCESS) {

        fprintf(stderr,
                "ERROR: ML-KEM encapsulation failed.\n");

        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }


    /*
     * ========================================================
     * ML-KEM decapsulation
     * ========================================================
     */

    if (OQS_KEM_decaps(
            kem,
            alice_mlkem_secret,
            mlkem_ciphertext,
            mlkem_secret_key
        ) != OQS_SUCCESS) {

        fprintf(stderr,
                "ERROR: ML-KEM decapsulation failed.\n");

        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }


    /*
     * ========================================================
     * Component correctness
     * ========================================================
     */

    int x25519_match =
        alice_x25519_len == bob_x25519_len &&
        secrets_equal(
            alice_x25519,
            bob_x25519,
            X25519_SECRET_LEN
        );

    int mlkem_match =
        secrets_equal(
            alice_mlkem_secret,
            bob_mlkem_secret,
            kem->length_shared_secret
        );


    /*
     * ========================================================
     * Construct hybrid secrets
     * ========================================================
     */

    unsigned char hybrid_alice[HYBRID_SECRET_LEN];
    unsigned char hybrid_bob[HYBRID_SECRET_LEN];

    if (!combine_secrets(
            alice_x25519,
            X25519_SECRET_LEN,
            alice_mlkem_secret,
            kem->length_shared_secret,
            hybrid_alice
        )) {

        fprintf(stderr,
                "ERROR: Alice hybrid construction failed.\n");

        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }


    if (!combine_secrets(
            bob_x25519,
            X25519_SECRET_LEN,
            bob_mlkem_secret,
            kem->length_shared_secret,
            hybrid_bob
        )) {

        fprintf(stderr,
                "ERROR: Bob hybrid construction failed.\n");

        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }


    int hybrid_match =
        secrets_equal(
            hybrid_alice,
            hybrid_bob,
            HYBRID_SECRET_LEN
        );


    /*
     * ========================================================
     * Negative Test 1
     *
     * Change the X25519 contribution.
     * ========================================================
     */

    unsigned char modified_x25519[X25519_SECRET_LEN];

    memcpy(
        modified_x25519,
        alice_x25519,
        X25519_SECRET_LEN
    );

    modified_x25519[0] ^= 0x01;


    unsigned char modified_x25519_hybrid[
        HYBRID_SECRET_LEN
    ];

    if (!combine_secrets(
            modified_x25519,
            X25519_SECRET_LEN,
            alice_mlkem_secret,
            kem->length_shared_secret,
            modified_x25519_hybrid
        )) {

        fprintf(stderr,
                "ERROR: X25519 contribution test failed.\n");

        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }


    int x25519_contribution_test =
        !secrets_equal(
            hybrid_alice,
            modified_x25519_hybrid,
            HYBRID_SECRET_LEN
        );


    /*
     * ========================================================
     * Negative Test 2
     *
     * Change the ML-KEM contribution.
     * ========================================================
     */

    unsigned char *modified_mlkem =
        malloc(kem->length_shared_secret);

    if (modified_mlkem == NULL) {

        fprintf(stderr,
                "ERROR: ML-KEM test allocation failed.\n");

        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }

    memcpy(
        modified_mlkem,
        alice_mlkem_secret,
        kem->length_shared_secret
    );

    modified_mlkem[0] ^= 0x01;


    unsigned char modified_mlkem_hybrid[
        HYBRID_SECRET_LEN
    ];

    if (!combine_secrets(
            alice_x25519,
            X25519_SECRET_LEN,
            modified_mlkem,
            kem->length_shared_secret,
            modified_mlkem_hybrid
        )) {

        fprintf(stderr,
                "ERROR: ML-KEM contribution test failed.\n");

        free(modified_mlkem);
        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }


    int mlkem_contribution_test =
        !secrets_equal(
            hybrid_alice,
            modified_mlkem_hybrid,
            HYBRID_SECRET_LEN
        );


    /*
     * ========================================================
     * Negative Test 3
     *
     * Change the domain-separation label.
     * ========================================================
     */

    static const unsigned char wrong_label[] =
        "PQC-Migrate-WRONG-DOMAIN";

    unsigned char wrong_domain_hybrid[
        HYBRID_SECRET_LEN
    ];

    if (!combine_with_label(
            wrong_label,
            sizeof(wrong_label) - 1,
            alice_x25519,
            X25519_SECRET_LEN,
            alice_mlkem_secret,
            kem->length_shared_secret,
            wrong_domain_hybrid
        )) {

        fprintf(stderr,
                "ERROR: Domain separation test failed.\n");

        free(modified_mlkem);
        free(mlkem_public_key);
        free(mlkem_secret_key);
        free(mlkem_ciphertext);
        free(alice_mlkem_secret);
        free(bob_mlkem_secret);

        goto failure;
    }


    int domain_separation_test =
        !secrets_equal(
            hybrid_alice,
            wrong_domain_hybrid,
            HYBRID_SECRET_LEN
        );


    /*
     * ========================================================
     * Results
     * ========================================================
     */

    printf("HYBRID CONSTRUCTION\n");
    printf("---------------------------------------------\n");

    printf("Hash function:               SHA-256\n");

    printf(
        "Domain label:               %s\n",
        HYBRID_LABEL
    );

    printf(
        "X25519 contribution:        %d bytes\n",
        X25519_SECRET_LEN
    );

    printf(
        "ML-KEM contribution:        %zu bytes\n",
        kem->length_shared_secret
    );

    printf(
        "Hybrid secret:               %d bytes\n",
        HYBRID_SECRET_LEN
    );


    printf("\nCOMPONENT CORRECTNESS\n");
    printf("---------------------------------------------\n");

    printf(
        "X25519 shared secret:       %s\n",
        x25519_match ? "SUCCESS" : "FAILED"
    );

    printf(
        "ML-KEM shared secret:       %s\n",
        mlkem_match ? "SUCCESS" : "FAILED"
    );


    printf("\nHYBRID AGREEMENT\n");
    printf("---------------------------------------------\n");

    printf("Alice hybrid secret:        ");
    print_hex(
        hybrid_alice,
        HYBRID_SECRET_LEN
    );

    printf("Bob hybrid secret:          ");
    print_hex(
        hybrid_bob,
        HYBRID_SECRET_LEN
    );

    printf(
        "Hybrid shared-secret match: %s\n",
        hybrid_match ? "SUCCESS" : "FAILED"
    );


    printf("\nCONTRIBUTION TESTS\n");
    printf("---------------------------------------------\n");

    printf(
        "Changing X25519 changes hybrid:       %s\n",
        x25519_contribution_test
            ? "PASS"
            : "FAILED"
    );

    printf(
        "Changing ML-KEM changes hybrid:       %s\n",
        mlkem_contribution_test
            ? "PASS"
            : "FAILED"
    );

    printf(
        "Changing domain label changes hybrid: %s\n",
        domain_separation_test
            ? "PASS"
            : "FAILED"
    );


    /*
     * ========================================================
     * Final result
     * ========================================================
     */

    int all_pass =
        x25519_match &&
        mlkem_match &&
        hybrid_match &&
        x25519_contribution_test &&
        mlkem_contribution_test &&
        domain_separation_test;


    printf("\nFINAL RESULT\n");
    printf("---------------------------------------------\n");

    if (all_pass) {
        printf(
            "ALL HYBRID CONSTRUCTION CHECKS: SUCCESS\n"
        );
    } else {
        printf(
            "HYBRID CONSTRUCTION CHECKS: FAILED\n"
        );
    }


    /*
     * ========================================================
     * Cleanup
     * ========================================================
     */

    free(modified_mlkem);
    free(mlkem_public_key);
    free(mlkem_secret_key);
    free(mlkem_ciphertext);
    free(alice_mlkem_secret);
    free(bob_mlkem_secret);

    EVP_PKEY_CTX_free(alice_ctx);
    EVP_PKEY_CTX_free(bob_ctx);
    EVP_PKEY_CTX_free(derive_ctx);

    EVP_PKEY_free(alice_key);
    EVP_PKEY_free(bob_key);

    OQS_KEM_free(kem);

    return all_pass
        ? EXIT_SUCCESS
        : EXIT_FAILURE;


failure:

    EVP_PKEY_CTX_free(alice_ctx);
    EVP_PKEY_CTX_free(bob_ctx);
    EVP_PKEY_CTX_free(derive_ctx);

    EVP_PKEY_free(alice_key);
    EVP_PKEY_free(bob_key);

    OQS_KEM_free(kem);

    return EXIT_FAILURE;
}
