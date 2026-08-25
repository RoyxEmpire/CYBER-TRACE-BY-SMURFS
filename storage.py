from pathlib import Path
import sqlite3
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent

DATA_PATH = (
    BASE_DIR
    / "TEST DATA GENERATOR"
    / "synthetic_complaints.csv"
)

DB_PATH = BASE_DIR / "cybertrace.db"


def create_database(connection):
    connection.execute("""
        CREATE TABLE IF NOT EXISTS complaints (
            complaint_id TEXT PRIMARY KEY,
            hop_count INTEGER,
            amount REAL,
            delay_minutes INTEGER,
            account_age_days INTEGER,
            kyc_verified INTEGER,
            num_source_accounts INTEGER,
            device_change_count INTEGER,
            ip_zone_mismatch INTEGER,
            round_amount_flag INTEGER,
            common_final_account INTEGER,
            withdrawal_zone TEXT,
            latitude REAL,
            longitude REAL,
            evidence_hash TEXT,
            risk_score REAL,
            created_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()


def insert_complaints(connection, dataframe):
    columns = [
        "complaint_id",
        "hop_count",
        "amount",
        "delay_minutes",
        "account_age_days",
        "kyc_verified",
        "num_source_accounts",
        "device_change_count",
        "ip_zone_mismatch",
        "round_amount_flag",
        "common_final_account",
        "withdrawal_zone",
        "latitude",
        "longitude"
    ]

    insert_query = """
        INSERT OR REPLACE INTO complaints (
            complaint_id,
            hop_count,
            amount,
            delay_minutes,
            account_age_days,
            kyc_verified,
            num_source_accounts,
            device_change_count,
            ip_zone_mismatch,
            round_amount_flag,
            common_final_account,
            withdrawal_zone,
            latitude,
            longitude
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """

    rows = dataframe[columns].itertuples(
        index=False,
        name=None
    )

    connection.executemany(insert_query, rows)
    connection.commit()


def show_summary(connection):
    total = connection.execute(
        "SELECT COUNT(*) FROM complaints"
    ).fetchone()[0]

    print(f"\nTotal complaints stored: {total}")

    print("\nLatest complaints:")
    rows = connection.execute("""
        SELECT complaint_id, amount, withdrawal_zone
        FROM complaints
        ORDER BY rowid DESC
        LIMIT 5
    """).fetchall()

    for row in rows:
        print(row)


def main():
    if not DATA_PATH.exists():
        raise FileNotFoundError(
            f"CSV file not found:\n{DATA_PATH}"
        )

    dataframe = pd.read_csv(DATA_PATH)

    required_columns = [
        "complaint_id",
        "hop_count",
        "amount",
        "delay_minutes",
        "account_age_days",
        "kyc_verified",
        "num_source_accounts",
        "device_change_count",
        "ip_zone_mismatch",
        "round_amount_flag",
        "common_final_account",
        "withdrawal_zone",
        "latitude",
        "longitude"
    ]

    missing_columns = [
        column for column in required_columns
        if column not in dataframe.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing columns: {missing_columns}"
        )

    with sqlite3.connect(DB_PATH) as connection:
        create_database(connection)
        insert_complaints(connection, dataframe)
        show_summary(connection)

    print(f"\nDatabase saved to:\n{DB_PATH}")


if __name__ == "__main__":
    main()