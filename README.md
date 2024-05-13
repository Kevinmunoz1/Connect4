# Connect4

##Overview
This Connect4 AI implementation allows you to play the classic Connect4 game against an AI, random player, or another human. The game is implemented in Python and utilizes advanced artificial intelligence techniques, including alpha-beta pruning and expectimax algorithms, to provide a challenging gaming experience.

Features
Multiple Player Types: Play against a sophisticated AI, a random decision-making player, or another human.
Graphical User Interface: The game features a simple GUI built with Tkinter, allowing for easy interaction and gameplay.
Configurable Time Limits: Set time limits for AI decision-making to ensure games progress smoothly without delays.
Requirements
To run this project, you need Python 3.x and the following libraries:

numpy
tkinter
multiprocessing
You can install the required packages using:

bash
Copy code
pip install numpy
Note: Tkinter usually comes pre-installed with Python. If it's not, refer to the Tkinter documentation for installation instructions.

Usage
To start the game, navigate to the project directory in your terminal and run:

bash
Copy code
python Connect4.py ai human --time 60
This command starts a game between an AI player and a human player with a 60-second time limit for AI moves.

Command Line Arguments
player1: First player type (ai, random, human).
player2: Second player type (ai, random, human).
--time: Optional. Time limit in seconds for AI moves. Default is 60 seconds.
Game Rules
Connect4 is played on a vertical board with 7 columns and 6 rows. The players take turns dropping colored discs into the columns. The first player to form a horizontal, vertical, or diagonal line of four discs wins the game.

Contributing
Contributions are welcome! Please fork the repository and open a pull request with your improvements.

License
This project is open-source and available under the MIT License.
