import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

# Load the data
csv_file_path = r"/kaggle/input/street-fighter2/abuzar_data.csv"
data = pd.read_csv(csv_file_path)

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

# Preprocess the data
# Select input features (X)
X = data[[
    "timer", "health", "x_coord", "y_coord", "is_jumping", "is_crouching",
    "is_player_in_move", "player1_buttons up", "player1_buttons down",
    "player1_buttons right", "player1_buttons left"
]]

# Select target labels (y) including directional and move columns
y = data[[
    "player1_buttons up", "player1_buttons down", "player1_buttons right", "player1_buttons left",
    "Light_Punch", "Light_Kick", "Medium_Punch", "Medium_Kick", "Hard_Punch", "Hard_Kick", "Special_Move"
]]

# Convert boolean values in y to integers
y = y.astype(int)

# Normalize the input features
scaler = StandardScaler()
X = scaler.fit_transform(X)

# Convert target labels to numpy array
y = y.values

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Build the deep learning model
model = Sequential([
    Dense(128, activation='relu', input_shape=(X_train.shape[1],)),
    Dropout(0.3),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(y_train.shape[1], activation='sigmoid')  # Sigmoid for multi-label classification
])

# Compile the model
model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# Train the model
history = model.fit(X_train, y_train, epochs=50, batch_size=32, validation_split=0.2)

# Evaluate the model
loss, accuracy = model.evaluate(X_test, y_test)
print(f"Test Accuracy: {accuracy * 100:.2f}%")

# Save the model
model.save("ai_agent_model_with_moves.h5")