import socket
import json
import sys  # Import sys to use sys.argv
from game_state import GameState
from bot import Bot
from pynput import keyboard

# Global variable to store the current key states
key_states = {
    "up": False,
    "down": False,
    "left": False,
    "right": False,
    "W": False,
    "E": False,
    "A": False,
    "S": False,
    "Z": False,
    "X": False
}

def on_press(key):
    """Handle key press events."""
    try:
        if key.char == 'w':
            key_states["W"] = True
        elif key.char == 'e':
            key_states["E"] = True
        elif key.char == 'a':
            key_states["A"] = True
        elif key.char == 's':
            print("S key pressed")  # Debug log
            key_states["S"] = True
        elif key.char == 'z':
            key_states["Z"] = True
        elif key.char == 'x':
            key_states["X"] = True
    except AttributeError:
        if key == keyboard.Key.up:
            key_states["up"] = True
        elif key == keyboard.Key.down:
            key_states["down"] = True
        elif key == keyboard.Key.left:
            key_states["left"] = True
        elif key == keyboard.Key.right:
            key_states["right"] = True

def on_release(key):
    """Handle key release events."""
    try:
        if key.char == 'w':
            key_states["W"] = False
        elif key.char == 'e':
            key_states["E"] = False
        elif key.char == 'a':
            key_states["A"] = False
        elif key.char == 's':
            key_states["S"] = False
        elif key.char == 'z':
            key_states["Z"] = False
        elif key.char == 'x':
            key_states["X"] = False
    except AttributeError:
        if key == keyboard.Key.up:
            key_states["up"] = False
        elif key == keyboard.Key.down:
            key_states["down"] = False
        elif key == keyboard.Key.left:
            key_states["left"] = False
        elif key == keyboard.Key.right:
            key_states["right"] = False

def connect(port):
    """For making a connection with the game."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("127.0.0.1", port))
    server_socket.listen(5)
    (client_socket, _) = server_socket.accept()
    print("Connected to game!")
    return client_socket

def send(client_socket, command):
    """Send updated command to Bizhawk so the game reacts accordingly."""
    command_dict = command.object_to_dict()
    pay_load = json.dumps(command_dict).encode()
    client_socket.sendall(pay_load)

def receive(client_socket):
    """Receive the game state and return it."""
    pay_load = client_socket.recv(4096)
    input_dict = json.loads(pay_load.decode())
    game_state = GameState(input_dict)
    return game_state

def map_keys_to_buttons(bot_command):
    """Map the current key states to the bot's button commands."""
    # Movement keys
    bot_command.player_buttons.up = key_states["up"]
    bot_command.player_buttons.down = key_states["down"]
    bot_command.player_buttons.left = key_states["left"]
    bot_command.player_buttons.right = key_states["right"]

    # Action keys
    bot_command.player_buttons.Y = key_states["S"]  # Light punch
    bot_command.player_buttons.B = key_states["X"]  # Light kick
    bot_command.player_buttons.X = key_states["A"]  # Medium punch
    bot_command.player_buttons.A = key_states["Z"]  # Medium kick
    bot_command.player_buttons.L = key_states["W"]  # Hard punch
    bot_command.player_buttons.R = key_states["E"]  # Hard kick

    # Log active moves to the console
    active_moves = []
    for key, state in key_states.items():
        if state:
            active_moves.append(key)
    if active_moves:
        print(f"Active moves: {', '.join(active_moves)}")

def main():
    if sys.argv[1] == '1':
        client_socket = connect(9999)
    elif sys.argv[1] == '2':
        client_socket = connect(10000)

    current_game_state = None
    bot = Bot()

    # Start listening to keyboard events
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    while (current_game_state is None) or (not current_game_state.is_round_over):
        current_game_state = receive(client_socket)
        bot_command = bot.fight(current_game_state, sys.argv[1])

        # Map keyboard inputs to bot commands
        map_keys_to_buttons(bot_command)

        send(client_socket, bot_command)

    listener.stop()

if __name__ == '__main__':
    main()