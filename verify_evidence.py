from pathlib import Path
import hashlib
import json


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


with open(HASH_PATH, "r", encoding="utf-8") as file:
    evidence_record = json.load(file)

old_hash = evidence_record["hash"]
new_hash = calculate_sha256(DATA_PATH)

print(f"Original hash: {old_hash}")
print(f"Current hash:  {new_hash}")

if old_hash == new_hash:
    print("\nSTATUS: Evidence is unchanged.")
else:
    print("\nSTATUS: WARNING - Evidence was modified!")