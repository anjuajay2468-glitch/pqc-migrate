#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <oqs/oqs.h>

int main(void) {
    OQS_KEM *kem = OQS_KEM_new(OQS_KEM_alg_ml_kem_768);

    if (kem == NULL) {
        fprintf(stderr, "ERROR: ML-KEM-768 is not available.\n");
        return EXIT_FAILURE;
    }

    printf("=============================================\n");
    printf("       PQC-Migrate ML-KEM-768 Analysis\n");
    printf("=============================================\n\n");

    printf("Algorithm: %s\n\n", kem->method_name);

    printf("PARAMETERS\n");
    printf("---------------------------------------------\n");
    printf("Public key size:    %zu bytes\n", kem->length_public_key);
    printf("Secret key size:    %zu bytes\n", kem->length_secret_key);
    printf("Ciphertext size:    %zu bytes\n", kem->length_ciphertext);
    printf("Shared secret size: %zu bytes\n\n", kem->length_shared_secret);

    uint8_t *public_key = malloc(kem->length_public_key);
    uint8_t *secret_key = malloc(kem->length_secret_key);
    uint8_t *ciphertext = malloc(kem->length_ciphertext);
    uint8_t *alice_secret = malloc(kem->length_shared_secret);
    uint8_t *bob_secret = malloc(kem->length_shared_secret);

    if (!public_key || !secret_key || !ciphertext ||
        !alice_secret || !bob_secret) {
        fprintf(stderr, "ERROR: Memory allocation failed.\n");
        OQS_KEM_free(kem);
        free(public_key);
        free(secret_key);
        free(ciphertext);
        free(alice_secret);
        free(bob_secret);
        return EXIT_FAILURE;
    }

    printf("CORRECTNESS TEST\n");
    printf("---------------------------------------------\n");

    int keygen_ok = OQS_KEM_keypair(
        kem,
        public_key,
        secret_key
    );

    if (keygen_ok != OQS_SUCCESS) {
        fprintf(stderr, "Key generation: FAILED\n");
        return EXIT_FAILURE;
    }

    printf("Key generation: SUCCESS\n");

    int enc_ok = OQS_KEM_encaps(
        kem,
        ciphertext,
        bob_secret,
        public_key
    );

    if (enc_ok != OQS_SUCCESS) {
        fprintf(stderr, "Encapsulation: FAILED\n");
        return EXIT_FAILURE;
    }

    printf("Encapsulation: SUCCESS\n");

    int dec_ok = OQS_KEM_decaps(
        kem,
        alice_secret,
        ciphertext,
        secret_key
    );

    if (dec_ok != OQS_SUCCESS) {
        fprintf(stderr, "Decapsulation: FAILED\n");
        return EXIT_FAILURE;
    }

    printf("Decapsulation: SUCCESS\n");

    int secrets_match = memcmp(
        alice_secret,
        bob_secret,
        kem->length_shared_secret
    ) == 0;

    printf(
        "Shared secret verification: %s\n",
        secrets_match ? "SUCCESS" : "FAILED"
    );

    printf("\nSIZE SUMMARY\n");
    printf("---------------------------------------------\n");
    printf("Public key:       %zu bytes\n", kem->length_public_key);
    printf("Secret key:       %zu bytes\n", kem->length_secret_key);
    printf("Ciphertext:       %zu bytes\n", kem->length_ciphertext);
    printf("Shared secret:    %zu bytes\n", kem->length_shared_secret);

    OQS_KEM_free(kem);

    free(public_key);
    free(secret_key);
    free(ciphertext);
    free(alice_secret);
    free(bob_secret);

    return secrets_match ? EXIT_SUCCESS : EXIT_FAILURE;
}
