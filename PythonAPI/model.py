import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.model_selection import train_test_split
import joblib
import os

# Load the dataset (assuming CSV/TSV format or pre-cleaned JSON)
df = pd.read_csv("/kaggle/input/dataset-streetfighter-gamestate/current_game_state0.txt", delimiter="\t")  # Or pd.read_json(...) if it's a JSON
print(df.columns.tolist())

# Clean/Convert boolean string values to actual booleans
bool_columns = [
    'is_jumping', 'is_crouching', 'is_player_in_move',
    'Player2 is_jumping', 'Player2 is_crouching', 'Player2 is_player_in_move',
    'player1_buttons up', 'player1_buttons down', 'player1_buttons right', 'player1_buttons left'
]
for col in bool_columns:
    df[col] = df[col].astype(str).str.upper().map({'TRUE': True, 'FALSE': False})

# Drop unnecessary columns
df = df[df['has_round_started'].astype(str).str.upper() == 'TRUE']  # Optional: only use active frames

# Define feature columns and label columns
feature_cols = [
    'Player1_ID', 'health', 'x_coord', 'y_coord', 'is_jumping', 'is_crouching', 'is_player_in_move', 'move_id',
    'Player2_ID', 'Player2 health', 'Player2 x_coord', 'Player2 y_coord',
    'Player2 is_jumping', 'Player2 is_crouching', 'Player2 is_player_in_move', 'Player2 move_id'
]

label_cols = [
    'player1_buttons up', 'player1_buttons down', 'player1_buttons right', 'player1_buttons left'
]

# Prepare features and labels
X = df[feature_cols]
y = df[label_cols]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model = MultiOutputClassifier(RandomForestClassifier(n_estimators=100, random_state=42))
model.fit(X_train, y_train)

# Save model
os.makedirs("model", exist_ok=True)
joblib.dump(model, "model/sf2_model.pkl")

# Optional: Evaluate
accuracy = model.score(X_test, y_test)
print(f"✅ Model trained with accuracy: {accuracy:.2f}")
