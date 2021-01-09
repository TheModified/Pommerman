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
            if self.check_if_left_is_clear_space(board, my_location):
                self.queue.append(Action.Left)
            if self.check_if_up_is_clear_space(board, my_location):
                self.queue.append(Action.Up)
            if self.check_if_right_is_clear_space(board, my_location):
                self.queue.append(Action.Right)
            if self.check_if_down_is_clear_space(board, my_location):
                self.queue.append(Action.Down)

            if not self.queue:
                self.queue.append(Action.Stop)

        return self.queue.pop()

    def check_if_left_is_clear_space(self, board: np.array, my_location: tuple) -> bool:
        """
        Checks if we can move to the left. Returns true if possible.
        """
        row, col = my_location
        if board[row, max(col - 1, 0)] == Item.Passage.value:
            return True
        return False

    def check_if_up_is_clear_space(self, board, my_location):
        """
        Checks if we can move up. Returns true if possible.
        """
        row, col = my_location
        if board[max(col - 1, 0), row] == Item.Passage.value:
            return True
        return False

    def check_if_right_is_clear_space(self, board, my_location):
        """
        Checks if we can move to the right. Returns true if possible.
        """
        row, col = my_location
        if board[row, min(col + 1, 7)] == Item.Passage.value:
            return True
        return False

    def check_if_down_is_clear_space(self, board, my_location):

        """
        Checks if we can move down. Returns true if possible.
        """
        row, col = my_location
        if board[min(col + 1, 7), row] == Item.Passage.value:
            return True
        return False
