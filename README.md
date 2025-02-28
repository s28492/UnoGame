# Uno with AI Agents

This repository contains a Python implementation of the card game Uno, along with AI players that use decision trees and simple neural networks to play the game. The goal is to develop AI agents that can learn and make intelligent decisions in Uno.


## How it Works
**Game**: The Game class purpose is to implement game logic, provide all rules are followed, carry out the game, and return data about the game conducted.

- **Game State**: The GameState class stores all the information about the current state of the game, including players' hands, the discard pile, and the current player.

- **AI Players**: The AI players inherit from the BaseAIBot class and implement their own logic for selecting cards to play based on their chosen algorithm (decision tree or neural network).

- **Decision Trees**: The ID3Tree and C4_5Tree classes implement the respective decision tree algorithms. These trees are trained on game data to predict the best card to play given a particular game state.

- **Neural Network**: The SimpleNNBot uses a neural network to predict the probability of winning with each possible card in hand.

- **Game Simulation**: The Game class simulates Uno games between AI players for MCTS agent, allowing for data collection and training.
### Heuristic Agents:

- **AgressiveBot**: Plays aggressively by prioritizing action cards and high-value cards.

- **BasicLogicBot**: Uses basic logic to play matching cards or draw when necessary.

- **BLBUpgradedColorChoosingBot**: An upgraded version of BasicLogicBot with improved color choosing strategy.

- **RandomBot**: Plays randomly by selecting valid cards available to play. 

### AI Agents:

- **C4_5Bot**: Uses a decision tree (C4.5 algorithm) trained on game data to make decisions.

- **NaiveBayesianBot**: Employs a Naive Bayesian classifier to predict the best card to play.

- **SimpleNNBot**: Utilizes an Imitation Learning algorithm to predict the best card to play.

- **MCTSBot**: Implements a Monte Carlo Tree Search algorithm to explore possible moves and select the most promising one.


## Getting Started

    ...

## TODO:

- **Improved AI**: Experiment with more advanced AI algorithms, such as Deep Q-Learning or Actor-Critic.

- **User Interface**: Develop more approachable UI allowing user for less interaction with raw Command Line.

- **Performance Optimization**: Optimize the code for faster game simulations and training. I'm already implementing Cython version of game simulation that will benefit speed of play overall, but especially MCTS since its so intense reliance on conducting tens od thousand simulations for each game.
