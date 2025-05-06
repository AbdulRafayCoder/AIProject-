class Buttons:

    def __init__(self, buttons_dict=None):

        if buttons_dict is not None:
            self.dict_to_object(buttons_dict)
        else:
            self.init_buttons()

    def init_buttons(self):
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.select = False
        self.start = False
        self.Y = False
        self.B = False
        self.X = False
        self.A = False
        self.L = False
        self.R = False

    def dict_to_object(self, buttons_dict):

        self.up = buttons_dict['Up']
        self.down = buttons_dict['Down']
        self.right = buttons_dict['Right']
        self.left = buttons_dict['Left']
        self.select = buttons_dict['Select']
        self.start = buttons_dict['Start']
        self.Y = buttons_dict['Y']
        self.B = buttons_dict['B']
        self.X = buttons_dict['X']
        self.A = buttons_dict['A']
        self.L = buttons_dict['L']
        self.R = buttons_dict['R']

    def object_to_dict(self):
        """Convert button states to a dictionary with standard Python bool values."""
        buttons_dict = {
            'Up': bool(self.up),
            'Down': bool(self.down),
            'Right': bool(self.right),
            'Left': bool(self.left),
            'Select': bool(self.select),
            'Start': bool(self.start),
            'Y': bool(self.Y),
            'B': bool(self.B),
            'X': bool(self.X),
            'A': bool(self.A),
            'L': bool(self.L),
            'R': bool(self.R)
        }
        return buttons_dict
    
    def reset(self):
        """Reset all button states to False."""
        self.up = False
        self.down = False
        self.right = False
        self.left = False
        self.select = False
        self.start = False
        self.Y = False
        self.B = False
        self.X = False
        self.A = False
        self.L = False
        self.R = False