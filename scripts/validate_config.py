#!/usr/bin/env python3

import sys
from pathlib import Path

CONFIG = Path("configs/experiment.yaml")

REQUIRED_SECTIONS = [
    "project:",
    "benchmark:",
    "classical:",
    "pqc:",
    "results:",
    "environment:",
]

def main():
    if not CONFIG.exists():
        print("ERROR: experiment.yaml not found")
        return 1

    text = CONFIG.read_text()

    missing = []

    for section in REQUIRED_SECTIONS:
        if section not in text:
            missing.append(section)

    if missing:
        print("Configuration validation: FAILED")
        print("Missing sections:")

        for section in missing:
            print(f"  - {section}")

        return 1

    required_algorithms = [
        "X25519",
        "RSA-2048",
        "ECDSA-P256",
        "ML-KEM-768",
        "ML-DSA-65",
    ]

    missing_algorithms = []

    for algorithm in required_algorithms:
        if algorithm not in text:
            missing_algorithms.append(algorithm)

    if missing_algorithms:
        print("Configuration validation: FAILED")
        print("Missing algorithms:")

        for algorithm in missing_algorithms:
            print(f"  - {algorithm}")

        return 1

    print("=============================================")
    print("       PQC-Migrate Configuration Check")
    print("=============================================")
    print()
    print("Configuration: VALID")
    print()
    print("Required sections: PASS")
    print("Required algorithms: PASS")
    print("Benchmark configuration: PASS")
    print("Results configuration: PASS")
    print()
    print("Configuration validation: SUCCESS")

    return 0


if __name__ == "__main__":
    sys.exit(main())

