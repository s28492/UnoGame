"""
@author Cyprian Szewczak s2849
"""

import tkinter as tk
from tkinter import messagebox
from Game import *
from Player import *


class UnoGUI(tk.Tk):
    def __init__(self, game):
        super().__init__()
        self.game = game
        self.title("UNO Game")

        self.current_player = None
        self.top_card = None

        self.player_hand_frame = tk.Frame(self)
        self.top_card_frame = tk.Frame(self)
        self.action_frame = tk.Frame(self)

        self.setup_ui()

    def setup_ui(self):
        self.player_hand_frame.pack(fill=tk.X)
        self.top_card_frame.pack(fill=tk.X)
        self.action_frame.pack(fill=tk.X)

        # Placeholder for top card
        tk.Label(self.top_card_frame, text="Top Card: ").pack(side=tk.LEFT)
        self.top_card_label = tk.Label(self.top_card_frame, text="")
        self.top_card_label.pack(side=tk.LEFT)

        # Action buttons
        tk.Button(self.action_frame, text="Draw Card", command=self.draw_card).pack(side=tk.LEFT)
        tk.Button(self.action_frame, text="Surrender", command=self.surrender).pack(side=tk.LEFT)

    def update_ui(self):
        # Clear the current player's hand
        for widget in self.player_hand_frame.winfo_children():
            widget.destroy()

        # Display current player's hand
        for card in self.current_player.hand:
            card_button = tk.Button(self.player_hand_frame, text=str(card), command=lambda c=card: self.play_card(c))
            card_button.pack(side=tk.LEFT, padx=2)

        # Update top card
        self.top_card_label.config(text=str(self.top_card))

    def play_card(self, card):
        if card.match(self.game.card_on_top):
            # Simulate playing the card
            self.game.card_on_top = card
            self.current_player.hand.remove(card)
            messagebox.showinfo("Play Card", f"Played {card}")
            self.next_turn()
        else:
            messagebox.showerror("Invalid Move", "You can't play this card.")

    def draw_card(self):
        if len(self.game.deck) > 0:
            drawn_card = self.game.deck.pop(0)
            self.current_player.hand.append(drawn_card)
            messagebox.showinfo("Draw Card", f"Drew {drawn_card}")
            self.update_ui()
        else:
            messagebox.showerror("Empty Deck", "The deck is empty.")

    def surrender(self):
        response = messagebox.askyesno("Surrender", "Are you sure you want to surrender?")
        if response:
            # Handle surrender logic, possibly removing the player from the game
            messagebox.showinfo("Surrender", f"{self.current_player} has surrendered.")
            self.game.drop_player(self.current_player)
            self.next_turn()

    def start_game(self):
        self.game.initialize_game()
        self.current_player = self.game.players[0]
        self.top_card = self.game.card_on_top
        self.update_ui()


if __name__ == "__main__":
    # Example usage
    players = [Player("Alice"), Player("Bob"), Player("Charlie")]
    game = Game(*players)

    app = UnoGUI(game)
    app.start_game()
    app.mainloop()