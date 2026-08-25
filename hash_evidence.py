from pathlib import Path
import hashlib
import json
from datetime import datetime, timezone


# Project paths
BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR
    / "TEST DATA GENERATOR"
    / "synthetic_complaints.csv"
)

HASH_PATH = BASE_DIR / "evidence_hash.json"


def calculate_sha256(file_path):
    sha256_hash = hashlib.sha256()

    with open(file_path, "rb") as file:
        for chunk in iter(lambda: file.read(1024 * 1024), b""):
            sha256_hash.update(chunk)

    return sha256_hash.hexdigest()


if not DATA_PATH.exists():
    raise FileNotFoundError(
        f"Evidence file not found:\n{DATA_PATH}"
    )


file_hash = calculate_sha256(DATA_PATH)

evidence_record = {
    "file_name": DATA_PATH.name,
    "file_path": str(DATA_PATH),
    "algorithm": "SHA-256",
    "hash": file_hash,
    "created_at_utc": datetime.now(
        timezone.utc
    ).isoformat()
}

with open(HASH_PATH, "w", encoding="utf-8") as file:
    json.dump(evidence_record, file, indent=4)

print("Evidence hash generated successfully!")
print(f"\nFile: {DATA_PATH}")
print(f"SHA-256: {file_hash}")
print(f"\nHash record saved to:\n{HASH_PATH}")