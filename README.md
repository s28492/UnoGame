# UnoGame
This documentation outlines the structure and functionality of a custom UNO game implemented in Python. The game is designed to be played in a console environment, supporting multiple players, a variety of card types, and adhering to the standard rules of UNO with some unique features.

Overview
The game consists of several classes that represent the different components and actors within the game, including:

Player: Represents a player in the game, holding their hand of cards and managing their actions.
Card: The basic card type with a value and color.
Special Cards: Including ReverseCard, StopCard, Plus2Card, Plus4Card, and ColorCard, each with unique effects on the game.
SurrenderCard and DrawCard: Special action cards allowing players to surrender or draw cards.
Game: Manages the overall game state, including the deck, the pile of played cards, player turns, and the flow of the game.
Class Descriptions
Player
Attributes:
name: The player's name.
hand: A list of Card objects the player currently holds.
stop_status, stopped, takes_status: Status indicators for special game conditions affecting the player.
Methods:
show_hand(): Displays the player's current hand of cards.
move(): Handles the player's action each turn, allowing them to play a card, draw, or surrender.
Card
Attributes:
value: The card's value (e.g., "1", "2", "Reverse").
color: The card's color ("Red", "Green", "Blue", "Yellow").
Methods:
play(game): Executes the card's effect on the game state.
match(other): Checks if the card can be played on top of other.
Special Cards
Each special card (ReverseCard, StopCard, Plus2Card, Plus4Card, ColorCard) extends Card with overridden play methods to implement their unique effects in the game.

Game
Attributes:
players: A list of Player objects participating in the game.
deck: The current deck of cards from which players can draw.
pile: The pile of played cards.
card_on_top: The top card of the pile, determining what can be played next.
index_of_a_player, direction, turns_to_stop, cards_to_take: Variables managing the flow of turns and special conditions.
Methods:
play(): Starts and manages the main game loop, cycling through player turns.
Various utility methods to manage the game state, such as shuffle_deck(), deal_cards_to_players(), and handling special actions like wanna_stop() and wanna_take().
Game Flow
Game Setup: Instantiate Game with Player objects. The game initializes by creating a deck, shuffling it, dealing cards to players, and starting the main game loop.
Player Turns: Players take turns according to the game's direction. On their turn, players can play a card from their hand if it matches the card_on_top in color or value, or they can draw a card if unable to play.
Special Cards: Playing special cards alters the game state, affecting subsequent turns (e.g., reversing the turn order, skipping players, forcing players to draw cards).
Winning: The game continues until a player wins by playing all their cards.
Running the Game
To start the game, ensure all classes (Player, Card and its subclasses, Game) are correctly defined in their respective files. Create a game instance by initializing Game with the desired Player objects and call the play() method to begin.