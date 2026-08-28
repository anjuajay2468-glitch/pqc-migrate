#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <oqs/oqs.h>

int main(void) {
    OQS_SIG *sig = OQS_SIG_new(OQS_SIG_alg_ml_dsa_65);

    if (sig == NULL) {
        fprintf(stderr, "ERROR: ML-DSA-65 is not available.\n");
        return EXIT_FAILURE;
    }

    printf("=============================================\n");
    printf("       PQC-Migrate ML-DSA-65 Analysis\n");
    printf("=============================================\n\n");

    printf("Algorithm: %s\n\n", sig->method_name);

    printf("PARAMETERS\n");
    printf("---------------------------------------------\n");
    printf("Public key size: %zu bytes\n", sig->length_public_key);
    printf("Secret key size: %zu bytes\n", sig->length_secret_key);
    printf("Signature size:  %zu bytes\n", sig->length_signature);
    printf("\n");

    uint8_t *public_key = malloc(sig->length_public_key);
    uint8_t *secret_key = malloc(sig->length_secret_key);
    uint8_t *signature = malloc(sig->length_signature);

    const uint8_t message[] =
        "PQC-Migrate ML-DSA-65 correctness test";
    size_t message_len = sizeof(message) - 1;

    if (!public_key || !secret_key || !signature) {
        fprintf(stderr, "ERROR: Memory allocation failed.\n");
        OQS_SIG_free(sig);
        free(public_key);
        free(secret_key);
        free(signature);
        return EXIT_FAILURE;
    }

    printf("CORRECTNESS TEST\n");
    printf("---------------------------------------------\n");

    int keygen_ok = OQS_SIG_keypair(
        sig,
        public_key,
        secret_key
    );

    if (keygen_ok != OQS_SUCCESS) {
        fprintf(stderr, "Key generation: FAILED\n");
        return EXIT_FAILURE;
    }

    printf("Key generation: SUCCESS\n");

    size_t signature_len = 0;

    int sign_ok = OQS_SIG_sign(
        sig,
        signature,
        &signature_len,
        message,
        message_len,
        secret_key
    );

    if (sign_ok != OQS_SUCCESS) {
        fprintf(stderr, "Signing: FAILED\n");
        return EXIT_FAILURE;
    }

    printf("Signing: SUCCESS\n");
    printf("Actual signature length: %zu bytes\n", signature_len);

    int verify_ok = OQS_SIG_verify(
        sig,
        message,
        message_len,
        signature,
        signature_len,
        public_key
    );

    if (verify_ok != OQS_SUCCESS) {
        fprintf(stderr, "Verification: FAILED\n");
        return EXIT_FAILURE;
    }

    printf("Verification: SUCCESS\n");

    printf("\nSIZE SUMMARY\n");
    printf("---------------------------------------------\n");
    printf("Public key:       %zu bytes\n", sig->length_public_key);
    printf("Secret key:       %zu bytes\n", sig->length_secret_key);
    printf("Signature:        %zu bytes\n", signature_len);

    OQS_SIG_free(sig);

    free(public_key);
    free(secret_key);
    free(signature);

    return EXIT_SUCCESS;
}
