# Uno with AI Agents
### Hey there! 👋
This is my pet project, where i learn and implement ML algorithms in Uno game.

This repository contains a Python implementation of game known and beloved by millions, along with AI players that use decision trees and simple neural networks to play the game. The goal is to develop AI agents that can learn and make intelligent decisions in Uno.
For simplification games are played only between 2 players at once.

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

## Report

In "Raport_z_projektu.pdf" i provided report on this project which elaborates on the game implementation and C4.5 algorithm. Soon this report will be expanded to elaborate on different algorithms such as MCTS, Naive Bayes and Imitation Learning.

<span style="color: firebrick"> Report is only in Polish language.</span>



## Getting Started
**Instruction for linux**
### Downloading project
1. Download project from github


    git clone https://github.com/s28492/UnoGame

2. Install all required packages from "/UnoGame" folder

    
    pip install -r requirements.txt
or

    conda install --file requirements.txt


### Creating data for C4.5 Tree

*This part shows how to play games between heuristic bots to collect data for C4.5, Naive Bayes and Imitation Learning algorithms* 

1. From the main project folder run *main.py*

       python3 -m Uno.main
2. Now program will allow user to choose if only heuristic bots should play against each other, or if C4.5 agent should also join. For now since there isn't any model of C4.5 bot trained 
     
        
## TODO:

- **Improved AI**: Experiment with more advanced AI algorithms, such as Deep Q-Learning or Actor-Critic.

- **User Interface**: Develop more approachable UI allowing user for less interaction with raw Command Line.

- **Performance Optimization**: Optimize the code for faster game simulations and training. I'm already implementing Cython version of game simulation that will benefit speed of play overall, but especially MCTS since its so intense reliance on conducting tens od thousand simulations for each game.

- **Add configs**: Just add configs. 
