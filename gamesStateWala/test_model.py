import joblib
import pandas as pd

# Load the model and scaler
model = joblib.load("ai_agent_model_with_moves.pkl")
scaler = joblib.load("scaler.pkl")

# Create a sample input based on Player 2's features
sample_input = {
    "timer": 100,  # Mid-game timer
    "Player1 health": 120,  # Opponent's health
    "Player1 x_coord": 400,  # Opponent's position
    "Player1 y_coord": 300,  # Opponent on the ground
    "Player1 is_jumping": False,
    "Player1 is_crouching": False,
    "Player1 is_player_in_move": False,
    "player1_buttons up": False,
    "player1_buttons down": False,
    "player1_buttons right": False,
    "player1_buttons left": False,
}

# Convert to DataFrame and scale
sample_df = pd.DataFrame([sample_input])
scaled_input = scaler.transform(sample_df)

# Predict using the model
predictions = model.predict(scaled_input)
print("Predictions (Raw):", predictions)

# Map predictions to labels
labels = [
    "player1_buttons up", "player1_buttons down", "player1_buttons right", "player1_buttons left",
    "Light_Punch", "Light_Kick", "Medium_Punch", "Medium_Kick", "Hard_Punch", "Hard_Kick", "Special_Move"
]
predicted_labels = {label: bool(pred) for label, pred in zip(labels, predictions[0])}
print("Predicted Labels:", predicted_labels)
