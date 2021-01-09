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
        goal_location = (2, 2)

        if len(self.queue) == 0:
            my_location = obs['position']
            board = obs['board']
            if self.can_move_to(board, my_location, goal_location):
                print("Can now move to this location: ", goal_location)
            if self.check_left(board, my_location):
                self.queue.append(Action.Left)
            if self.check_up(board, my_location):
                self.queue.append(Action.Up)
            if self.check_right(board, my_location):
                self.queue.append(Action.Right)
            if self.check_down(board, my_location):
                self.queue.append(Action.Down)

            if not self.queue:
                self.queue.append(Action.Stop)

        return self.queue.pop()

    def check_left(self, board: np.array, my_location: tuple) -> bool:
        """
        Checks if we can move to the left. Returns true if possible.
        """
        row, col = my_location
        if board[row, max(col - 1, 0)] == Item.Passage.value:
            return True
        return False

    def check_up(self, board: np.array, my_location: tuple) -> bool:
        """
        Checks if we can move up. Returns true if possible.
        """
        row, col = my_location
        if board[max(col - 1, 0), row] == Item.Passage.value:
            return True
        return False

    def check_right(self, board: np.array, my_location: tuple) -> bool:
        """
        Checks if we can move to the right. Returns true if possible.
        """
        row, col = my_location
        if board[row, min(col + 1, 7)] == Item.Passage.value:
            return True
        return False

    def check_down(self, board: np.array, my_location: tuple) -> bool:

        """
        Checks if we can move down. Returns true if possible.
        """
        row, col = my_location
        if board[min(col + 1, 7), row] == Item.Passage.value:
            return True
        return False

    def can_move_to(self, board: np.array, my_location: tuple, goal_location: tuple) -> bool:
        directions = dict(left=np.array([0, -1]), right=np.array([0, 1]), down=np.array([-1, 0]), up=np.array([1, 0]))

        to_visit = [my_location]
        visited = []

        while to_visit:
            next_location = to_visit.pop(0)
            for key, value in directions.items():

                new_point = tuple(np.array(next_location) + value)
                if new_point == goal_location:
                    return True

                if min(new_point) < 0 or max(new_point) > 7:
                    continue

                if new_point in visited:
                    continue

                if key == "left" and self.check_left(board, tuple(next_location)):
                    to_visit.append(new_point)
                elif key == "right" and self.check_right(board, tuple(next_location)):
                    to_visit.append(new_point)
                elif key == "up" and self.check_up(board, tuple(next_location)):
                    to_visit.append(new_point)
                elif key == "down" and self.check_down(board, tuple(next_location)):
                    to_visit.append(new_point)

            visited.append(next_location)

        return False



