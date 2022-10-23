import random

class Player:
    def __init__(self, character, turn):
        self.character = character
        self.turn = turn
        
    def _empty_fields(self, board):
        " Returns list of tuples. Every tuple contains x and y coordinates of aviable field "
        return [(i1,i2) for (i1,v1) in enumerate(board) for (i2,v2) in enumerate(v1) if v2['text'] == ' ']
    
    def _player_move(self, board):
        pass

class PlayerHuman(Player):
    def __init__(self, character, turn):
        super().__init__(character, turn)
        
    def __str__(self):
        return "Człowiek"

    def _player_move(self, board, row, column):
        return row, column, self.character

        
class PlayerComputer(Player):
    def __init__(self, character, turn):
        super().__init__(character, turn)
        
    def __str__(self):
        return "Komputer"
        
    def _player_move(self, board, row=None, column=None):
        try:
            _empty_fields = self._empty_fields(board)
            return random.choice(_empty_fields) + (self.character,)
        except IndexError:
            return

