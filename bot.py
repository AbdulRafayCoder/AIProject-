import csv
import os
from command import Command
from buttons import Buttons

class Bot:
    def __init__(self):
        self.my_command = Command()
        self.buttn = Buttons()
        self.csv_file = "game_state_log.csv"
        self.write_csv_header()

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

    def fight(self, current_game_state, player):
        """Main fight logic."""
        # Log the current game state to the CSV file only if a move is made
        self.log_game_state(current_game_state)

        # Reset buttons at the start of each frame
        self.buttn.reset()

        # Assign the updated buttons to the command
        if player == "1":
            self.my_command.player_buttons = self.buttn
        elif player == "2":
            self.my_command.player2_buttons = self.buttn

        return self.my_command