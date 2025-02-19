# Uno with AI Players

This repository contains a Python implementation of the card game Uno, along with AI players that use decision trees and simple neural networks to play the game. The goal is to develop AI agents that can learn and make intelligent decisions in Uno.
Features

    Game Logic: Implements the complete rules of Uno, including special cards and actions.
    AI Players:
        Decision Tree Bots: Utilize ID3 and C4.5 decision tree algorithms to make game decisions based on learned patterns from game data.
        Neural Network Bot: Employs a simple neural network to predict the best card to play.
    Training: Includes scripts to train decision trees and neural networks using collected game data.
    Data Handling: Provides tools for collecting, processing, and analyzing game data.
    Modular Design: Allows for easy extension and experimentation with new AI algorithms and game variations.

## How it Works

    Game State: The GameState class stores all the information about the current state of the game, including players' hands, the discard pile, and the current player.
    AI Players: The AI players inherit from the BaseAIBot class and implement their own logic for selecting cards to play based on their chosen algorithm (decision tree or neural network).
    Decision Trees: The ID3Tree and C4_5Tree classes implement the respective decision tree algorithms. These trees are trained on game data to predict the best card to play given a particular game state.
    Neural Network: The SimpleNNBot uses a neural network to predict the probability of winning with each possible card in hand.
    Game Simulation: The Game class simulates Uno games between AI players, allowing for data collection and training.

## Getting Started

    Clone the repository: git clone https://github.com/your-username/uno-ai.git
    Install dependencies: pip install -r requirements.txt
    Run a game: python main.py (You might need to modify main.py to specify the AI players and game settings.)
    Train AI agents: Use the provided scripts (BuildTree.py, RF_Creator.py, baggingCreator.py) to train the decision trees and neural network.

## Future Work

    Improved AI: Experiment with more advanced AI algorithms, such as reinforcement learning or deeper neural networks.
    Game Variations: Implement different rule variations of Uno.
    User Interface: Develop a graphical user interface for playing against AI agents.
    Performance Optimization: Optimize the code for faster game simulations and training.

