import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
from itertools import cycle
import player


class App(tk.Tk):
    COLOR_WIN = "#169c28"
    BLACK = "#000000"
    FIELD_FONT_STYLE = "Arial", 20, "bold"
    MAX_PLAYER = 2
    MAX_TURN = 9

    def __init__(self):
        super().__init__()
        self.title("TicTacToe")
        self.geometry("400x450")
        self.resizable = False
        self.players_types = {"Człowiek": player.PlayerHuman,
                              "Komputer": player.PlayerComputer}
        self._player_one, self._player_two = tk.StringVar(), tk.StringVar()
        self.board = [["", "", ""],
                      ["", "", ""],
                      ["", "", ""]]
        self.winner = False
        self.turn_count = 0
        self._create_widgets()

    def _create_widgets(self):
        """ Responsible for creating individual interface elements """
        # Creating menu options
        self._create_options()
        # Creating player setup fields
        self.players_setup_frame = self._create_players_setup_frame()
        self._create_players_setup()
        # Creating game fields
        self.fields_frame = self._create_fields_frame()
        self._create_fields()

    def _create_options(self):
        options = tk.Menu(self, tearoff=False)
        options.add_command(label="Zresetuj grę", command=self._reset_game)
        self.config(menu=options)

    def _create_players_setup_frame(self):
        frame = tk.LabelFrame(self, height=10, text="Konfiguracja rozgrywki")
        frame.pack(fill="both", padx=5, pady=5)
        return frame

    def _create_players_setup(self):
        """ Responsible for creating widgets responsible for the 
        configuration of players. """
        # pierwszy gracz
        
        lbl_player_1 = tk.Label(self.players_setup_frame,
                                text="Pierwszy gracz (X)")
        cbx_player_1 = ttk.Combobox(self.players_setup_frame,
                                    state="normal",
                                    textvariable=self._player_one)
        cbx_player_1['values'] = list(self.players_types.keys())
        # drugi gracz
        lbl_player_2 = tk.Label(self.players_setup_frame,
                                anchor=tk.W,
                                text="Drugi gracz (O)")
        cbx_player_2 = ttk.Combobox(self.players_setup_frame,
                                    state="normal",
                                    textvariable=self._player_two)
        cbx_player_2['values'] = list(self.players_types.keys())
        # osadzenie comboboxów
        lbl_player_1.grid(row=1, column=0)
        lbl_player_2.grid(row=1, column=1)
        cbx_player_1.grid(row=2, column=0, pady=5, padx=5)
        cbx_player_2.grid(row=2, column=1, pady=5, padx=(0, 5))
        # przycisk startu gry
        btn = tk.Button(self.players_setup_frame,
                        text="Graj",
                        command=self._start_game)
        btn.grid(row=1, column=3, rowspan=2, sticky=tk.N+tk.S, pady=(0, 5))

    def _start_game(self):
        """  """
        self._setup_players()
        self._change_fields_state(tk.NORMAL)
        # Sprawdzenie czy ilość graczy jest odpowiednia oraz czy pierwszy jest kompyter
        if len(self.players) == self.MAX_PLAYER \
                and isinstance(self.current_player,  player.PlayerComputer):
            self._turn()

    def _setup_players(self):
        """ Responsible for creating instances of player classes and their configuration. """
        self.players = []
        # Sprawdza czy wybrano graczy do gry
        if self._player_one.get() and self._player_two.get():
            self.players.append(
                self.players_types[self._player_one.get()]('X', turn=True)
            )
            self.players.append(
                self.players_types[self._player_two.get()]('O', turn=False)
            )
            self._players = cycle(self.players)
            self.current_player = next(self._players)
        else:
            messagebox.showwarning("Komunikat", "Nie wybrano graczy.")

    def toggle_player(self):
        """ Calls ``next()`` function on iterator object created by
        ``cycle(_players)`` . """
        self.current_player = next(self._players)

    def _create_fields_frame(self):
        """ Return tkinter frame for game fileds """
        frame = tk.LabelFrame(self, text="Pola gry")
        frame.pack(expand=True, fill="both", padx=5, pady=5)
        return frame

    def _create_fields(self):
        """ Responsible for creating buttons representing 
        the fields of the game and their base configuration.

        Inserts each button into a place in the ``self.board`` matrix based on 
        the successive passes of the loop for the successive rows and columns.

        Clicking on a field calls the lamda function 
        which calls the ``self._turn()`` method to pass 
        the coordinates of the clicked button.

        By default, the buttons are disabled. The status will change to assets 
        after selecting players."""
        self.fields_frame.rowconfigure(0, weight=1)
        for row in range(3):
            # Ustawienie parametrów szerokości i wysyokości kolumn i wierszy
            self.fields_frame.rowconfigure(row, weight=1)
            self.fields_frame.columnconfigure(row, weight=1)
            for column in range(3):
                self.board[row][column] = tk.Button(
                    self.fields_frame,
                    text=" ",
                    fg=self.BLACK,
                    font=self.FIELD_FONT_STYLE,
                    command=lambda row=row, column=column: self._turn(row, column))
                # Osadzenie przycisków w self.board na podstawie współrzędnych
                self.board[row][column].grid(
                    row=row, column=column, sticky=tk.NSEW, padx=2, pady=2)
        self._change_fields_state(tk.DISABLED)

    def _turn(self, row=None, column=None):
        """ Responsible for controlling the game. It calls the ``_player_move()`` interface on the current players. If the ``self.winner()`` method does not set the ``winner`` flag to true, it causes the next player to be changed and recursively calls itself.

        Args:
            row (_type_, optional): _description_. Defaults to None.
            column (_type_, optional): _description_. Defaults to None.
        """
        try:
            _move = self.current_player._player_move(self.board, row, column)
            _row, _column, _character = _move
            if self.board[_row][_column]["text"] == ' ':
                self.board[_row][_column]["text"] = _character
                self.turn_count += 1
                self._check_win()
                if not self.winner:
                    self.toggle_player()
                    self._turn()
            else:
                messagebox.showerror(
                    "Kółko i Krzyżyk", "Pole jest już zajęte!")
        except TypeError:
            pass

    def _check_win(self):
        """ Responsible for calling individual functions that check whether the current state of the game has a winner. """
        for player in self.players:
            if self.winner:  # Jeżeli jest zwycięsca wychodzi z pętli
                break
            if self._row_win(self.board, player.character) or \
                    self._col_win(self.board, player.character) or \
                    self._diagonal_win(self.board, player.character):
                self.winner = True
                self._change_fields_state(tk.DISABLED)
                messagebox.showinfo("Kółko i Krzyżyk",
                                    f"Wygrał {player.character}.")
        else:
            # Tie
            if self.turn_count == self.MAX_TURN and not self.winner:
                self._change_fields_state(tk.DISABLED)
                messagebox.showinfo("Kółko i Krzyżyk", "Remis!")

    def _row_win(self, board, character):
        for row in board:
            if all([cell['text'] == character for cell in row]):
                # change color if combo win
                for field in row:
                    field.config(
                        bg=self.COLOR_WIN
                    )
                return True
        return False

    def _col_win(self, board, character):
        for i in range(len(board)):
            if all([row[i]['text'] == character for row in board]):
                # change color if combo win
                for row in board:
                    row[i].config(
                        bg=self.COLOR_WIN
                    )
                return True
        return False

    def _diagonal_win(self, board, character):
        # diagonal
        if all([board[i][i]['text'] == character for i in range(0, len(board))]):
            # change color if combo win
            for i in range(0, len(board)):
                board[i][i].config(
                    bg=self.COLOR_WIN
                )
            return True
        # counter-diagonal with bit-wise negation (~) returns negative index
        if all([board[i][~i]['text'] == character for i in range(0, len(board))]):
            # change color if combo win
            for i in range(0, len(board)):
                board[i][~i].config(
                    bg=self.COLOR_WIN
                )
            return True
        return False

    def _change_fields_state(self, state, text: str = None, bg: str = None):
        """Responsible for changing the appearance of all game fields in accordance with the parameters provided.

        Args:
            ``state`` (): Tkinter global. Allows tk.DISABLED or tk.NORMAL. Defaults to None.
            ``text`` (str), optional): Change text in all fields. Defaults to None.
            ``bg`` (str), optional): Background color for all fiealds. Defaults to None.
        """
        for row in range(3):
            for column in range(3):
                self.board[row][column].config(state=state)
                if text is not None:
                    self.board[row][column]["text"] = " "
                if bg is not None:
                    self.board[row][column].config(bg=bg)

    def _reset_game(self):
        """ Restores the game to its default state. """
        self.turn_count = 0
        self.winner = False
        self._change_fields_state(
            state=tk.DISABLED,
            text=" ",
            bg="SystemButtonFace"
        )

    def run(self):
        self.mainloop()


if __name__ == '__main__':
    App().run()
