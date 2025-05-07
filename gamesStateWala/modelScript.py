import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.multioutput import MultiOutputClassifier
from sklearn.metrics import accuracy_score
import joblib  # For saving the model
from sklearn.utils import resample

# Load the data
csv_file_path = r"complete_csv.csv"
data = pd.read_csv(csv_file_path)

# Handle missing values
if data.isnull().values.any():
    print("Dataset contains missing values. Filling missing values with column means.")
    data.fillna(data.mean(), inplace=True)

# Drop constant columns, but exclude essential columns
essential_columns = [
    "player2_buttons up", "player2_buttons down", "player2_buttons right", "player2_buttons left"
]
constant_columns = [col for col in data.columns if data[col].nunique() <= 1 and col not in essential_columns]
if constant_columns:
    print(f"The following columns have constant values and will be dropped: {constant_columns}")
    data.drop(columns=constant_columns, inplace=True)

# Map move_id to individual move columns
move_mapping = {
    0: "Idle",
    1: "Light_Punch",
    2: "Light_Kick",
    3: "Medium_Punch",
    4: "Medium_Kick",
    5: "Hard_Punch",
    6: "Hard_Kick",
    7: "Special_Move"
}

# Add columns for each move
for move_id, move_name in move_mapping.items():
    data[move_name] = (data["move_id"] == move_id).astype(int)

# Debug: Print column names in the dataset
print("Columns in dataset:", data.columns.tolist())

# Preprocess the data
# Select input features (X) for Player 1
X = data[ [
    "timer", "health", "x_coord", "y_coord", "is_jumping", "is_crouching",
    "is_player_in_move", "player1_buttons up", "player1_buttons down",
    "player1_buttons right", "player1_buttons left"
]]

# Select target labels (y) including directional and move columns for Player 1
y = data[[
    "player1_buttons up", "player1_buttons down", "player1_buttons right", "player1_buttons left",
    "Light_Punch", "Light_Kick", "Medium_Punch", "Medium_Kick", "Hard_Punch", "Hard_Kick", "Special_Move"
]]

# Ensure target labels are integers
y = y.astype(int)

# Normalize the input features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Convert target labels to numpy array
y = y.values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Balance the dataset using oversampling
data_majority = data[data["move_id"] == 0]  # Example: majority class
data_minority = data[data["move_id"] != 0]  # Example: minority classes

data_minority_upsampled = resample(
    data_minority,
    replace=True,
    n_samples=len(data_majority),
    random_state=42
)

data = pd.concat([data_majority, data_minority_upsampled])

# Log class distribution after balancing
print("Class Distribution After Balancing:")
print(data["move_id"].value_counts())

# Wrap RandomForestClassifier with MultiOutputClassifier
base_model = RandomForestClassifier(
    n_estimators=200,  # Increase the number of trees
    max_depth=20,      # Limit the depth of each tree
    min_samples_split=5,  # Minimum samples required to split a node
    random_state=42
)
model = MultiOutputClassifier(base_model)
model.fit(X_train, y_train)

# Perform cross-validation
cv_scores = cross_val_score(model, X_train, y_train, cv=5, scoring="accuracy")
print(f"Cross-Validation Accuracy: {cv_scores.mean() * 100:.2f}%")

# Evaluate the model
y_pred = model.predict(X_test)
accuracy = (y_pred == y_test).mean()  # Calculate accuracy for multi-label classification
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Log training and validation accuracy
from sklearn.metrics import accuracy_score

y_train_pred = model.predict(X_train)
train_accuracy = accuracy_score(y_train, y_train_pred)
print(f"Training Accuracy: {train_accuracy * 100:.2f}%")

y_test_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_test_pred)
print(f"Validation Accuracy: {test_accuracy * 100:.2f}%")

# Save the model and scaler
joblib.dump(model, "ai_agent_model_with_moves.pkl")
print('Saved ai_agent_model_with_moves.pkl')
joblib.dump(scaler, "scaler.pkl")
print('Saved scaler.pkl')
# Analyze the dataset
print("\nDataset Info:")
print(data.info())
print("\nDataset Description:")
print(data.describe())
print("\nClass Distribution:")
print(data["move_id"].value_counts())