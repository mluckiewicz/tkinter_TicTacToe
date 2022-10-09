import tkinter as tk
from tkinter import DISABLED, NORMAL, messagebox


class App(tk.Tk):
    
    FIELD_FONT = "Arial, 48"
    
    def __init__(self):
        super().__init__()
        self.geometry("400x400")
        self.title("Kółko i krzyżyk")
        self.resizable = False
        self.turn = True
        self.turn_count = 0
        self.winner = False
        self.game_state = [["", "", ""],
                            ["", "", ""],
                            ["", "", ""]]
        
        self.fields_possition = {
            "f1": (0, 0), "f2": (0, 1), "f3": (0, 2),
            "f4": (1, 0), "f5": (1, 1), "f6": (1, 2),
            "f7": (2, 0), "f8": (2, 1), "f9": (2, 2),
        }
        self.fields = []
        self.fields_frame = self.create_fields_frame() # ramka pól gry
        
        self.fields_frame.rowconfigure(0, weight=1)
        # # ustawienie szerokości kollumn i wysokości wierszy
        for i in range(3):
             self.fields_frame.rowconfigure(i, weight=1)
             self.fields_frame.columnconfigure(i, weight=1)
            
        self.create_options()
        self.create_fields() #utworzenie pól gry
        
    def create_options_frame(self):
        options_frame = tk.Frame(self)
        options_frame.pack(expand=True, fill="both")
        return options_frame

    def create_fields_frame(self):
        fields_frame = tk.Frame(self)
        fields_frame.pack(expand=True, fill="both")
        return fields_frame
    
    def create_options(self):
        options = tk.Menu(self, tearoff=False)
        options.add_command(label="Zresetuj grę", command=self.reset)
        self.config(menu=options)
        
        
    def create_fields(self):
        for field_name, possition in self.fields_possition.items():
            field = tk.Button(
                    self.fields_frame,
                    name=field_name,
                    text=" ",
                    font=self.FIELD_FONT)
            field.grid(
                    row=possition[0], 
                    column=possition[1],
                    padx=1, pady=1, 
                    sticky=tk.NSEW)
            field["command"] = lambda i=field: self.update_field(i)
            self.fields.append(field)

    def update_field(self, btn):
        if btn["text"] == " " and self.turn:
            btn["text"] = "X"
            self.turn = False
            self.turn_count += 1
            coord = self.fields_possition[btn.__dict__["_name"]]
            self.game_state[coord[0]][coord[1]] = "X"
        elif btn["text"] == " " and not self.turn:
            btn["text"] = "O"
            self.turn = True
            self.turn_count += 1
            coord = self.fields_possition[btn.__dict__["_name"]]
            self.game_state[coord[0]][coord[1]] = "O"
        else:
            messagebox.showerror("Kółko i Krzyżyk", "To pole jest już zajęte!.")
        self.check_win() # check if any sign wins

    def check_win(self):
        # Check if someone wins
        for sing in ("X", "O"):
            if self.row_win(self.game_state, sing) or \
                self.col_win(self.game_state, sing) or \
                self.diagonal_win(self.game_state, sing):
                self.winner = True
                self.disable_all_fields()
                messagebox.showinfo("Kółko i Krzyżyk", f"Wygrał {sing}")
        else:
            # Tie
            if self.turn_count == 9 and self.winner == False:
                self.disable_all_fields()
                messagebox.showinfo("Kółko i Krzyżyk", "Remis!.")

    def row_win(self, board, player):
        for row in board:
            if all([cell == player for cell in row]):
                return True
        return False

    def col_win(self, board, player):
        for i in range(len(board)):
            if all([row[i] == player for row in board]):
                return True
        return False

    def diagonal_win(self, board, player):
        # diagonal
        if all([board[i][i] == player for i in range(0, len(board))]):
            return True
        # counter-diagonal with bit-wise negation (~) returns negative index
        if all([board[i][~i] == player for i in range(0, len(board))]):
            return True
        return False
    
    def disable_all_fields(self):
        for field in self.fields:
            field.config(state=DISABLED)
            
    def reset(self):

        self.turn_count = 0
        self.turn = True
        self.winner = False
        
        for field in self.fields:
            field["text"] = " "
            field.config(state=NORMAL)
            
        for i in range(len(self.game_state)):
            for j in range(len(self.game_state)):
                self.game_state[i][j] = ""
                
    def run(self):
        self.mainloop()

if __name__ == '__main__':
    App().run()