import numpy as np

class AIPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'ai'
        self.player_string = 'Player {}:ai'.format(player_number)
        #Defining the max depth for the Alpa-beta algortihm:
        self.max_depth= 4

    def winning_move(self, board, player):
        # Check horizontal locations for a win
        for c in range(board.shape[1] - 3):
            for r in range(board.shape[0]):
                if (board[r][c] == player and board[r][c + 1] == player and 
                    board[r][c + 2] == player and board[r][c + 3] == player):
                    return True

        # Check vertical locations for a win
        for c in range(board.shape[1]):
            for r in range(board.shape[0] - 3):
                if (board[r][c] == player and board[r + 1][c] == player and 
                    board[r + 2][c] == player and board[r + 3][c] == player):
                    return True

        # Check positively sloped diagonals
        for c in range(board.shape[1] - 3):
            for r in range(board.shape[0] - 3):
                if (board[r][c] == player and board[r + 1][c + 1] == player and 
                    board[r + 2][c + 2] == player and board[r + 3][c + 3] == player):
                    return True

        # Check negatively sloped diagonals
        for c in range(board.shape[1] - 3):
            for r in range(3, board.shape[0]):
                if (board[r][c] == player and board[r - 1][c + 1] == player and 
                    board[r - 2][c + 2] == player and board[r - 3][c + 3] == player):
                    return True

        return False

    def make_move(self, board, col, player_number):
        """
        Make a move on the board by placing the player's piece in the specified column.

        INPUTS:
        - board: the game board represented as a numpy array
        - col: the column index where the piece should be placed
        - player_number: the number representing the player (1 or 2)
        """
        # Starting from the bottom row, place the player's piece in the first available spot
        for row in reversed(range(board.shape[0])):
            if board[row, col] == 0:
                board[row, col] = player_number
                return
        # If the column is full, you may want to raise an error or handle it appropriately
        raise ValueError(f"Column {col} is full.")



    def valid_moves(self, board):
        valid_moves = []
        for col in range(board.shape[1]):  # board.shape[1] gives the number of columns
            if board[0][col] == 0:  # If the top entry of a column is 0, the column has space
                valid_moves.append(col)
        return valid_moves

    def is_terminal_node(self, board):
        
        # Check for victory for each player
        for player in [1, 2]:  # Assuming player numbers are 1 and 2
            if self.winning_move(board, player):
                return True

        # Check if there are any valid moves left
        if 0 in board[0]:  # Check the top row for any zeros, which indicate available moves
            return False

        # If no player has won and there are no valid moves left, it's a terminal node (draw)
        return True


    def get_alpha_beta_move(self, board):
        best_score = float("-inf")
        best_move = None
        alpha = float("-inf")
        beta = float("inf")
        valid_moves = self.valid_moves(board)

        # Iterate over all valid moves
        for move in valid_moves:
            temp_board = board.copy()
            self.make_move(temp_board, move, self.player_number)
            # Call the alpha-beta search function, starting with depth, alpha, beta, and maximizing_player=False
            score = self.alpha_beta_search(temp_board, depth=self.max_depth, alpha=alpha, beta=beta, maximizing_player=False)
            # Update best_score and best_move if a better score is found
            if score > best_score:
                best_score = score
                best_move = move
            # Update the alpha value
            alpha = max(alpha, best_score)

        return best_move
        
        """
        Given the current state of the board, return the next move based on
        the alpha-beta pruning algorithm

        This will play against either itself or a human player

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

    def alpha_beta_search(self, board, depth, alpha, beta, maximizing_player):


     # Check if we have reached the maximum depth or if the game is over (terminal state)
        if depth == 0 or self.is_terminal_node(board):
            # If the game is over or if the depth is 0, return the evaluation function value
            return self.evaluation_function(board)

        # If we are the maximizing player
        if maximizing_player:
            max_eval = float("-inf")  # Initialize the maximum evaluation score to negative infinity
            for move in self.valid_moves(board):
                temp_board = board.copy()
                self.make_move(temp_board, move, self.player_number)
                eval = self.alpha_beta_search(temp_board, depth-1, alpha, beta, False)
                max_eval = max(max_eval, eval)
                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  # Beta cut-off
            return max_eval
        else:  # If we are the minimizing player
            min_eval = float("inf")  # Initialize the minimum evaluation score to infinity
            for move in self.valid_moves(board):
                temp_board = board.copy()
                self.make_move(temp_board, move, 3 - self.player_number)  # Assume player numbers are 1 and 2
                eval = self.alpha_beta_search(temp_board, depth-1, alpha, beta, True)
                min_eval = min(min_eval, eval)
                beta = min(beta, eval)
                if beta <= alpha:
                    break  # Alpha cut-off
            return min_eval



    def expectimax_search(self, board, depth, maximizing_player):
        if depth == 0 or self.is_terminal_node(board):  
            return self.evaluation_function(board) 

        if maximizing_player:
            best_score = float("-inf")
            for move in self.valid_moves(board):
                temp_board = board.copy()
                self.make_move(temp_board, move, self.player_number)
                score = self.expectimax_search(temp_board, depth - 1, False)
                best_score = max(best_score, score)
            return best_score
        else:  # Chance node
            scores = []
            valid_moves = self.valid_moves(board)
            if not valid_moves:  # Check if there are no valid moves left
                return self.evaluation_function(board)

            for move in valid_moves:
                temp_board = board.copy()
                self.make_move(temp_board, move, 3 - self.player_number)
                score = self.expectimax_search(temp_board, depth - 1, True)
                scores.append(score)

            # Since the opponent plays randomly, we take the average of the scores
            average_score = sum(scores) / len(scores) if scores else 0
            return average_score

            # Since the opponent plays randomly, we take the average of the scores
            average_score = sum(scores) / len(scores)
            return average_score
    
    def get_expectimax_move(self, board):
        best_score = float("-inf")
        best_move = None
        valid_moves = self.valid_moves(board)
       
        for move in valid_moves:
            temp_board = board.copy()
            self.make_move(temp_board, move, self.player_number)
            score = self.expectimax_search(temp_board, depth=4, maximizing_player=False)
            if score > best_score:
                best_score = score
                best_move = move

        return best_move

        
        """
        Given the current state of the board, return the next move based on
        the expectimax algorithm.

        This will play against the random player, who chooses any valid move
        with equal probability

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

    
    def evaluation_function(self, board):
        score = 0
        # Define player and opponent numbers
        player = self.player_number
        opponent = 3 - player  # Assuming player numbers are 1 and 2
        
        # Define the score for various patterns
        THREE_IN_A_ROW = 100
        TWO_IN_A_ROW = 10
        ONE_IN_A_ROW = 1

        # Check horizontal spaces
        for row in range(board.shape[0]):
            for col in range(board.shape[1] - 3):
                window = list(board[row, col:col+4])
                score += self.score_window(window, player, opponent, THREE_IN_A_ROW, TWO_IN_A_ROW, ONE_IN_A_ROW)

        # Check vertical spaces
        for row in range(board.shape[0] - 3):
            for col in range(board.shape[1]):
                window = list(board[row:row+4, col])
                score += self.score_window(window, player, opponent, THREE_IN_A_ROW, TWO_IN_A_ROW, ONE_IN_A_ROW)

        # Check positive diagonal spaces
        for row in range(board.shape[0] - 3):
            for col in range(board.shape[1] - 3):
                window = [board[row+i, col+i] for i in range(4)]
                score += self.score_window(window, player, opponent, THREE_IN_A_ROW, TWO_IN_A_ROW, ONE_IN_A_ROW)

        # Check negative diagonal spaces
        for row in range(3, board.shape[0]):
            for col in range(board.shape[1] - 3):
                window = [board[row-i, col+i] for i in range(4)]
                score += self.score_window(window, player, opponent, THREE_IN_A_ROW, TWO_IN_A_ROW, ONE_IN_A_ROW)

        return score
        """
        Given the current stat of the board, return the scalar value that 
        represents the evaluation function for the current player
       
        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The utility value for the current board
        """
       
       
    def score_window(self, window, player, opponent, THREE_IN_A_ROW, TWO_IN_A_ROW, ONE_IN_A_ROW):
            """
            Score a window of four slots according to how favorable it is for the player.
    
            INPUTS:
            - window: a list containing 4 integers representing a line on the board
            - player: the player number
            - opponent: the opponent player number
            - THREE_IN_A_ROW: the score for having three in a row
            - TWO_IN_A_ROW: the score for having two in a row
            - ONE_IN_A_ROW: the score for having one in a row
    
            RETURNS:
            - score: a score for the window
            """
            score = 0
            # If there are three in a row and the fourth is empty, that's a high score
            if window.count(player) == 3 and window.count(0) == 1:
                score += THREE_IN_A_ROW
            # If there are two in a row and the rest are empty, that's a moderate score
            elif window.count(player) == 2 and window.count(0) == 2:
                score += TWO_IN_A_ROW
            # If there's one in a row and the rest are empty, that's a low score
            elif window.count(player) == 1 and window.count(0) == 3:
                score += ONE_IN_A_ROW
    
            # Optionally, you can also subtract points if the opponent has a favorable position
            if window.count(opponent) == 3 and window.count(0) == 1:
                score -= 5 * THREE_IN_A_ROW
    
            return score



class RandomPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'random'
        self.player_string = 'Player {}:random'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state select a random column from the available
        valid moves.

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """
        valid_cols = []
        for col in range(board.shape[1]):
            if 0 in board[:,col]:
                valid_cols.append(col)

        return np.random.choice(valid_cols)


class HumanPlayer:
    def __init__(self, player_number):
        self.player_number = player_number
        self.type = 'human'
        self.player_string = 'Player {}:human'.format(player_number)

    def get_move(self, board):
        """
        Given the current board state returns the human input for next move

        INPUTS:
        board - a numpy array containing the state of the board using the
                following encoding:
                - the board maintains its same two dimensions
                    - row 0 is the top of the board and so is
                      the last row filled
                - spaces that are unoccupied are marked as 0
                - spaces that are occupied by player 1 have a 1 in them
                - spaces that are occupied by player 2 have a 2 in them

        RETURNS:
        The 0 based index of the column that represents the next move
        """

        valid_cols = []
        for i, col in enumerate(board.T):
            if 0 in col:
                valid_cols.append(i)

        move = int(input('Enter your move: '))

        while move not in valid_cols:
            print('Column full, choose from:{}'.format(valid_cols))
            move = int(input('Enter your move: '))

        return move

