import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

# Load the data we generated in Step 1
df = pd.read_csv('synthetic_complaints.csv')

print("Loaded data:")
print(df.head())
print(f"\nTotal complaints: {len(df)}")

# Features = the clues the model will learn from
# Target = what we want the model to predict (withdrawal_zone)
features = ['hop_count', 'amount', 'delay_minutes']
target = 'withdrawal_zone'

X = df[features]   # Input data (clues)
y = df[target]      # Output we want to predict (zone)

# XGBoost needs numbers, not text - so convert zone names into numbers
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

print("\nZone name to number mapping:")
for zone, number in zip(label_encoder.classes_, range(len(label_encoder.classes_))):
    print(f"{zone} -> {number}")

# Split data: 80% for training, 20% for testing
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42
)

print(f"\nTraining data size: {len(X_train)}")
print(f"Testing data size: {len(X_test)}")