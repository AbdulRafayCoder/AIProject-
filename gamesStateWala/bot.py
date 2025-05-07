from command import Command
from buttons import Buttons
import csv
import keyboard  # Requires the `keyboard` library to capture keyboard inputs
import os

class Bot:

    def __init__(self):
        self.my_command = Command()
        self.buttn = Buttons()
        self.previous_buttons = Buttons()  # Track previous button states
        self.moves_log = []  # To store moves

    def fight(self, current_game_state, player):
        # Listen for keyboard input and update buttons
        self.listen_to_keyboard()

        # Save the moves if they create an impact
        self.save_moves(player)

        if player == "1":
            self.my_command.player_buttons = self.buttn
        elif player == "2":
            self.my_command.player2_buttons = self.buttn

        # Save the move and game state
        self.save_move_and_state(self.my_command, current_game_state)

        return self.my_command

    def listen_to_keyboard(self):
        # Reset button states
        self.buttn.init_buttons()

        # Map specified keys to button actions
        if keyboard.is_pressed('up'):
            self.buttn.up = True
        if keyboard.is_pressed('down'):
            self.buttn.down = True
        if keyboard.is_pressed('left'):
            self.buttn.left = True
        if keyboard.is_pressed('right'):
            self.buttn.right = True
        if keyboard.is_pressed('a'):
            self.buttn.X = True
        if keyboard.is_pressed('s'):
            self.buttn.Y = True
        if keyboard.is_pressed('w'):
            self.buttn.L = True
        if keyboard.is_pressed('e'):
            self.buttn.R = True
        if keyboard.is_pressed('z'):
            self.buttn.B = True
        if keyboard.is_pressed('x'):
            self.buttn.A = True

    def save_moves(self, player):
        # Check if the current button states differ from the previous states
        if self.buttn.object_to_dict() != self.previous_buttons.object_to_dict():
            # Save only impactful moves
            moves_dict = {
                "player": player,
                "moves": self.buttn.object_to_dict()
            }
            self.moves_log.append(moves_dict)

            # Save to CSV
            file_exists = os.path.exists("moves_log.csv")
            with open("moves_log.csv", "a", newline="") as file:
                writer = csv.DictWriter(file, fieldnames=["player"] + list(self.buttn.object_to_dict().keys()))
                if not file_exists:
                    writer.writeheader()  # Write header if file doesn't exist
                writer.writerow({"player": player, **self.buttn.object_to_dict()})

            # Update previous button states
            self.previous_buttons = Buttons(self.buttn.object_to_dict())

    def save_move_and_state(self, command, game_state):
        """
        Save the move and the corresponding game state to a CSV file.
        """
        file_path = "moves_and_states.csv"
        file_exists = os.path.exists(file_path)

        # Prepare data to save
        move_data = command.object_to_dict()
        game_state_data = game_state.object_to_dict()
        combined_data = {**move_data, **game_state_data}

        # Flatten nested dictionaries for CSV
        flattened_data = {}
        for key, value in combined_data.items():
            if isinstance(value, dict):
                for sub_key, sub_value in value.items():
                    flattened_data[f"{key}_{sub_key}"] = sub_value
            else:
                flattened_data[key] = value

        # Write to CSV
        with open(file_path, mode="a", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=flattened_data.keys())
            if not file_exists:
                writer.writeheader()  # Write header if file doesn't exist
            writer.writerow(flattened_data)
