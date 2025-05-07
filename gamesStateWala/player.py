from buttons import Buttons

class Player:

    def __init__(self, player_dict):
        
        self.dict_to_object(player_dict)
    
    def dict_to_object(self, player_dict):
        
        self.player_id = player_dict['character']
        self.health = player_dict['health']
        self.x_coord = player_dict['x']
        self.y_coord = player_dict['y']
        self.is_jumping = player_dict['jumping']
        self.is_crouching = player_dict['crouching']
        self.player_buttons = Buttons(player_dict['buttons'])
        self.is_player_in_move = player_dict['in_move']
        self.move_id = player_dict['move']

    def object_to_dict(self):
        return {
            "player_id": self.player_id,
            "health": self.health,
            "x_coord": self.x_coord,
            "y_coord": self.y_coord,
            "is_jumping": self.is_jumping,
            "is_crouching": self.is_crouching,
            "player_buttons": self.player_buttons.object_to_dict(),
            "is_player_in_move": self.is_player_in_move,
            "move_id": self.move_id
        }
