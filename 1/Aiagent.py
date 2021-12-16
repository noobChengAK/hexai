import copy
import socket
from random import choice, randrange
from time import sleep
import math
import numpy as np

from evaluate import QueenbeeAgent


class NaiveAgent():
    """This class describes the default Hex agent. It will randomly send a
    valid move at each turn, and it will choose to swap with a 50% chance.
    """

    HOST = "127.0.0.1"
    PORT = 1234

    def run(self):
        """A finite-state machine that cycles through waiting for input
        and sending moves.
        """

        self._board_size = 0
        self._board = []
        self._colour = ""
        self._turn_count = 1
        self._choices = []
        self.winner = None
        self.fair_area = [(0, 0), (1, 0), (0, 1), (10, 10), (9, 10), (10, 9)]
        states = {
            1: NaiveAgent._connect,
            2: NaiveAgent._wait_start,
            3: NaiveAgent._make_move,
            4: NaiveAgent._wait_message,
            5: NaiveAgent._close
        }
        self.RED = "R"
        self.BLUE = "B"
        res = states[1](self)
        while (res != 0):
            res = states[res](self)

    def _connect(self):
        """Connects to the socket and jumps to waiting for the start
        message.
        """

        self._s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._s.connect((NaiveAgent.HOST, NaiveAgent.PORT))

        return 2

    def _wait_start(self):
        """Initialises itself when receiving the start message, then
        answers if it is Red or waits if it is Blue.
        """

        data = self._s.recv(1024).decode("utf-8").strip().split(";")
        if (data[0] == "START"):
            self._board_size = int(data[1])
            # for i in range(self._board_size):
            #     for j in range(self._board_size):
            #         self._choices.append((i, j))
            self._board = np.full((self._board_size, self._board_size), "0")
            self._colour = data[2]

            if (self._colour == "R"):
                return 3
            else:
                return 4

        else:
            print("ERROR: No START message received.")
            return 0

    def _make_move(self):
        """Makes a random valid move. It will choose to swap with
        a coinflip.
        """
        # data = self._s.recv(1024).decode("utf-8").strip().split(";")
        # x, y = data[1].split(",")

        # if (self._turn_count == 2 and not (x, y)  in self.fair_area):
        if (self._turn_count == 2 and choice([0, 1]) == 1):
            msg = "SWAP\n"
        else:
            move = self.get_best_move(self._board,3)
            msg = f"{move[0]},{move[1]}\n"

        self._s.sendall(bytes(msg, "utf-8"))

        return 4

    def _wait_message(self):
        """Waits for a new change message when it is not its turn."""

        self._turn_count += 1

        data = self._s.recv(1024).decode("utf-8").strip().split(";")
        if (data[0] == "END" or data[-1] == "END"):
            return 5
        else:

            if (data[1] == "SWAP"):
                self._colour = self.opp_colour()
                for i in range(self._board_size):
                    for j in range(self._board_size):
                        if self._board[i][j] == "R":
                            self._board[i][j] = "B"
                        else:
                            self._board[i][j] = "R"
                        break
            else:
                x, y = data[1].split(",")
                if data[-1] == self._colour:
                    self._board[int(x)][int(y)] = self.opp_colour()
                else:
                    self._board[int(x)][int(y)] = self._colour
                # self._choices.remove((int(x), int(y)))

            if (data[-1] == self._colour):
                return 3

        return 4

    def _close(self):
        """Closes the socket."""

        self._s.close()
        return 0

    def get_best_move(self, board, depth):
        bestmove = None
        alpha = -math.inf
        beta = math.inf
        moves = self.get_moves()
        for move in moves:
            updatedBoard = self.updateBoardWithMove(copy.deepcopy(board), move, self._colour)
            evaluation = self.alpha_beta_pruning(updatedBoard, depth - 1, True, alpha, beta)
            if alpha < evaluation:
                alpha = evaluation
                bestmove = move
        return bestmove

    def alpha_beta_pruning(self, board, depth, isMaximizingPlayer, alpha, beta):  # customize depth will impact speed

        if depth <= 0 or self.isBoardFull():
            return QueenbeeAgent.evaluate(board)
        else:
            if isMaximizingPlayer:
                bestValue = -math.inf
                moves = self.get_moves()
                for move in moves:
                    updatedBoard = self.updateBoardWithMove(copy.deepcopy(board), move, self._colour)
                    bestValue = max(bestValue, self.alpha_beta_pruning(updatedBoard, depth - 1, False, alpha, beta))
                    # nodevalue, _, _ = self.alpha_beta_pruning(updatedBoard, depth - 1, False, alpha, beta)
                    # node = max(bestValue,nodevalue)
                    alpha = max(alpha, bestValue)

                    if beta <= alpha:
                        break
                return bestValue
            else:
                bestValue = math.inf
                moves = self.get_moves()
                for move in moves:
                    updateBoard = self.updateBoardWithMove(copy.deepcopy(board), move, self.opp_colour())
                    bestValue = min(bestValue, self.alpha_beta_pruning(updateBoard, depth - 1, True, alpha, beta))
                    beta = min(beta, bestValue)
                    # node = min(bestValue, nodevalue)

                    if beta <= alpha:
                        break

                return bestValue

    def getNeighbours(self, x, y):
        """Return a list of neighbours of the given position.
        """
        ls = [(x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1), (x - 1, y + 1), (x + 1, y - 1)]
        newls = []
        for (i, j) in ls:
            if i >= 0 and i < self._board_size and j >= 0 and j < self._board_size:
                newls.append((i, j))
        return newls

    def isBoardFull(self):
        return np.all(self._board != "0")
        # return not (0 in sum(self.board, []))  # check if board is full

    def get_moves(self):
        # movelist =[]
        # for i in range(self._board_size):
        #     for j in range(self._board_size):
        #         if self._board[i][j] == 0:
        #             movelist.append([i,j])
        # return movelist
        results = np.where(self._board == "0")
        return list(zip(results[0], results[1]))

    def updateBoardWithMove(self, board, move, color):
        (x, y) = move
        board[x][y] = color
        return board

    def opp_colour(self):
        """Returns the char representation of the colour opposite to the
        current one.
        """

        if self._colour == "R":
            return "B"
        elif self._colour == "B":
            return "R"
        else:
            return "None"


if (__name__ == "__main__"):
    agent = NaiveAgent()
    agent.run()
