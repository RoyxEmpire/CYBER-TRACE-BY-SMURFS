import pandas as pd
import random
from faker import Faker

fake = Faker()
data = []

# Zone codes with real approximate lat/long (Chennai, Mumbai, Delhi areas)
zone_coordinates = {
    '600001': {'lat': 13.0827, 'lon': 80.2707},   # Chennai central
    '600028': {'lat': 13.0067, 'lon': 80.2206},   # Chennai (Guindy area)
    '400001': {'lat': 18.9388, 'lon': 72.8354},   # Mumbai central
    '110001': {'lat': 28.6139, 'lon': 77.2090},   # Delhi central
    '700001': {'lat': 22.5726, 'lon': 88.3639},   # Kolkata central
}

zones = list(zone_coordinates.keys())

for i in range(500):
    complaint_id = f"CMP{i+1000}"
    hop_count = random.randint(2, 8)
    amount = random.randint(5000, 100000)
    delay = random.randint(1, 60)
    account_age_days = random.randint(1, 1000)
    kyc_verified = random.choice([0, 1])
    num_source_accounts = random.randint(1, 5)
    device_change_count = random.randint(0, 4)
    ip_zone_mismatch = random.choice([0, 1])
    round_amount_flag = 1 if amount % 1000 == 0 else 0
    common_final_account = random.choice([0, 1])

    risk_score = 0
    if hop_count >= 6:
        risk_score = risk_score + 1
    if account_age_days < 30:
        risk_score = risk_score + 1
    if kyc_verified == 0:
        risk_score = risk_score + 1
    if device_change_count >= 2:
        risk_score = risk_score + 1
    if ip_zone_mismatch == 1:
        risk_score = risk_score + 1
    if common_final_account == 1:
        risk_score = risk_score + 1

    if risk_score >= 4:
        zone = '600028'
    elif risk_score == 3:
        zone = '400001'
    elif risk_score == 2:
        zone = '700001'
    elif risk_score == 1:
        zone = '600001'
    else:
        zone = '110001'

    if random.random() < 0.1:
        zone = random.choice(zones)

    # Add small random jitter to lat/lon so points aren't all identical
    base_lat = zone_coordinates[zone]['lat']
    base_lon = zone_coordinates[zone]['lon']
    jitter_lat = base_lat + random.uniform(-0.02, 0.02)
    jitter_lon = base_lon + random.uniform(-0.02, 0.02)

    row = {}
    row['complaint_id'] = complaint_id
    row['hop_count'] = hop_count
    row['amount'] = amount
    row['delay_minutes'] = delay
    row['account_age_days'] = account_age_days
    row['kyc_verified'] = kyc_verified
    row['num_source_accounts'] = num_source_accounts
    row['device_change_count'] = device_change_count
    row['ip_zone_mismatch'] = ip_zone_mismatch
    row['round_amount_flag'] = round_amount_flag
    row['common_final_account'] = common_final_account
    row['withdrawal_zone'] = zone
    row['latitude'] = round(jitter_lat, 6)
    row['longitude'] = round(jitter_lon, 6)

    data.append(row)

df = pd.DataFrame(data)
save_path = r'd:\CLG WORKS\PROJECTS\HACKATHONS\SIH 2026\TEST DATA GENERATOR\synthetic_complaints.csv'
df.to_csv(save_path, index=False)

print("Data generated successfully!")
print(df.head())
print("Zone distribution:")
print(df['withdrawal_zone'].value_counts())
print("Columns:", list(df.columns))