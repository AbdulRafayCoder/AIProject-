import csv
import os
import numpy as np
from tensorflow.keras.models import load_model
from command import Command
from buttons import Buttons

class Bot:
    def __init__(self):
        self.my_command = Command()
        self.buttn = Buttons()
        self.csv_file = "game_state_log.csv"
        self.write_csv_header()

        # Load the trained model
        self.model = load_model("ai_agent_model_with_moves.h5")

    def write_csv_header(self):
        """Write the header row to the CSV file if it doesn't exist."""
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, mode='w', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    "timer", "fight_result", "has_round_started", "is_round_over",
                    "Player1_ID", "health", "x_coord", "y_coord", "is_jumping", "is_crouching", "is_player_in_move", "move_id",
                    "player1_buttons up", "player1_buttons down", "player1_buttons right", "player1_buttons left",
                    "Player2_ID", "Player2 health", "Player2 x_coord", "Player2 y_coord", "Player2 is_jumping", "Player2 is_crouching",
                    "Player2 is_player_in_move", "Player2 move_id", "player2_buttons up", "player2_buttons down",
                    "player2_buttons right", "player2_buttons left"
                ])

    def preprocess_game_state(self, game_state):
        """Extract and preprocess features from the game state."""
        features = [
            game_state.timer,                     # 1
            game_state.player1.health,           # 2
            game_state.player1.x_coord,          # 3
            game_state.player1.y_coord,          # 4
            game_state.player1.is_jumping,       # 5
            game_state.player1.is_crouching,     # 6
            game_state.player1.is_player_in_move, # 7
            game_state.player1.move_id,          # 8
            game_state.player2.health,           # 9
            game_state.player2.x_coord,          # 10
            game_state.player2.y_coord           # 11
        ]
        # Convert to numpy array and reshape for the model
        return np.array(features).reshape(1, -1)

    def map_predictions_to_buttons(self, predictions):
        """Map model predictions to button presses."""
        # Reset all button states
        self.buttn.reset()

        # Map the 11 output units to button states
        self.buttn.up = predictions[0][0] > 0.5
        self.buttn.down = predictions[0][1] > 0.5
        self.buttn.left = predictions[0][2] > 0.5
        self.buttn.right = predictions[0][3] > 0.5
        self.buttn.Y = predictions[0][4] > 0.5
        self.buttn.B = predictions[0][5] > 0.5
        self.buttn.X = predictions[0][6] > 0.5
        self.buttn.A = predictions[0][7] > 0.5
        self.buttn.L = predictions[0][8] > 0.5
        self.buttn.R = predictions[0][9] > 0.5
        self.buttn.select = predictions[0][10] > 0.5

        # Debug log for predictions and button states
        print("Predictions:", predictions)
        print("Mapped Buttons (Python bool):", self.buttn.object_to_dict())

    def fight(self, current_game_state, player):
        """Main fight logic."""
        # Log the current game state to the CSV file
        self.log_game_state(current_game_state)

        # Preprocess the game state
        input_features = self.preprocess_game_state(current_game_state)

        # Predict the moves using the model
        predictions = self.model.predict(input_features)

        # Map predictions to button presses
        self.map_predictions_to_buttons(predictions)

        # Assign the updated buttons to the command
        if player == "1":
            self.my_command.player_buttons = self.buttn
        elif player == "2":
            self.my_command.player2_buttons = self.buttn

        # Debug log for the command object
        print("Updated Command Object:", self.my_command.object_to_dict())

        # Ensure the command is returned with updated buttons
        return self.my_command

    def log_game_state(self, game_state):
        """Log the current game state to the CSV file only if a move is made by the player."""
        # Check if any button is pressed by Player 1
        if (game_state.player1.player_buttons.up or
            game_state.player1.player_buttons.down or
            game_state.player1.player_buttons.left or
            game_state.player1.player_buttons.right or
            game_state.player1.player_buttons.Y or
            game_state.player1.player_buttons.B or
            game_state.player1.player_buttons.X or
            game_state.player1.player_buttons.A or
            game_state.player1.player_buttons.L or
            game_state.player1.player_buttons.R):
            
            # Log the game state to the CSV file
            with open(self.csv_file, mode='a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([
                    game_state.timer,
                    game_state.fight_result,
                    game_state.has_round_started,
                    game_state.is_round_over,
                    game_state.player1.player_id,
                    game_state.player1.health,
                    game_state.player1.x_coord,
                    game_state.player1.y_coord,
                    game_state.player1.is_jumping,
                    game_state.player1.is_crouching,
                    game_state.player1.is_player_in_move,
                    game_state.player1.move_id,
                    game_state.player1.player_buttons.up,
                    game_state.player1.player_buttons.down,
                    game_state.player1.player_buttons.right,
                    game_state.player1.player_buttons.left,
                    game_state.player2.player_id,
                    game_state.player2.health,
                    game_state.player2.x_coord,
                    game_state.player2.y_coord,
                    game_state.player2.is_jumping,
                    game_state.player2.is_crouching,
                    game_state.player2.is_player_in_move,
                    game_state.player2.move_id,
                    game_state.player2.player_buttons.up,
                    game_state.player2.player_buttons.down,
                    game_state.player2.player_buttons.right,
                    game_state.player2.player_buttons.left
                ])