import numpy as np
from pommerman import characters
from pommerman.constants import Action, Item
from pommerman.agents import BaseAgent


class MyAgent(BaseAgent):
    """ Our version of the base agent. """

    def __init__(self, character=characters.Bomber):
        super().__init__(character)
        self.queue = []

    def act(self, obs, action_space):
        # Main event that is being called on every turn.
        if len(self.queue) == 0:
            my_location = obs['position']
            board = obs['board']
            if self.check_left(board, my_location):
                self.queue.append(Action.Left)
            if self.check_right(board, my_location):
                self.queue.append(Action.Right)
            if self.check_up(board, my_location):
                self.queue.append(Action.Up)
            if self.check_down(board, my_location):
                self.queue.append(Action.Down)
        return self.queue.pop()

    def check_left(self, board, my_location):
        row, col = my_location
        if board[row, max(col - 1, 0)] == Item.Passage.value:
            return True
        return False

    def check_up(self, board, my_location):
        row, col = my_location
        if board[max(col - 1, 0), row] == Item.Passage.value:
            return True
        return False

    def check_right(self, board, my_location):
        row, col = my_location
        if board[row, min(col + 1, 7)] == Item.Passage.value:
            return True
        return False

    def check_down(self, board, my_location):
        row, col = my_location
        if board[min(col + 1, 7), row] == Item.Passage.value:
            return True
        return False
