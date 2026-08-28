#include <stdio.h>
#include <string.h>
#include <oqs/oqs.h>

int main(void)
{
    OQS_KEM *kem = OQS_KEM_new("ML-KEM-768");

    if (kem == NULL)
    {
        fprintf(stderr, "Failed to initialize ML-KEM-768\n");
        return 1;
    }

    printf("=== PQC-Migrate: ML-KEM-768 Test ===\n\n");

    printf("Algorithm: %s\n", kem->method_name);

    uint8_t public_key[kem->length_public_key];
    uint8_t secret_key[kem->length_secret_key];
    uint8_t ciphertext[kem->length_ciphertext];
    uint8_t shared_secret_alice[kem->length_shared_secret];
    uint8_t shared_secret_bob[kem->length_shared_secret];

    printf("\nGenerating key pair...\n");

    if (OQS_KEM_keypair(kem, public_key, secret_key) != OQS_SUCCESS)
    {
        fprintf(stderr, "Key generation failed\n");
        OQS_KEM_free(kem);
        return 1;
    }

    printf("Key generation: SUCCESS\n");

    printf("\nBob encapsulating shared secret...\n");

    if (OQS_KEM_encaps(kem, ciphertext, shared_secret_bob, public_key) != OQS_SUCCESS)
    {
        fprintf(stderr, "Encapsulation failed\n");
        OQS_KEM_free(kem);
        return 1;
    }

    printf("Encapsulation: SUCCESS\n");

    printf("\nAlice decapsulating shared secret...\n");

    if (OQS_KEM_decaps(kem, shared_secret_alice, ciphertext, secret_key) != OQS_SUCCESS)
    {
        fprintf(stderr, "Decapsulation failed\n");
        OQS_KEM_free(kem);
        return 1;
    }

    printf("Decapsulation: SUCCESS\n");

    if (memcmp(shared_secret_alice,
               shared_secret_bob,
               kem->length_shared_secret) == 0)
    {
        printf("\nShared secret verification: SUCCESS\n");
        printf("Alice and Bob derived the SAME shared secret.\n");
    }
    else
    {
        printf("\nShared secret verification: FAILED\n");
    }

    OQS_KEM_free(kem);

    return 0;
}
