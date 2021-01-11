import numpy as np

from pommerman import characters
from pommerman.constants import Action, Item
from pommerman.agents import BaseAgent

from serpentine.directions import Direction, Directions


class MyAgent(BaseAgent):
    """ Our version of the base agent. """

    def __init__(self, character=characters.Bomber):
        super().__init__(character)
        self.queue = []

    def act(self, obs, action_space):
        # Main event that is being called on every turn.
        if not self.queue:
            my_location = obs['position']
            board = obs['board']
            goal_location = (6, 6)

            for direction in self.create_path(board, my_location, goal_location):
                self.queue.append(direction.action)

            if not self.queue:
                self.queue.append(Action.Stop)

            return self.queue.pop(0)

    def in_bounds(self, location: tuple) -> bool:
        return 0 <= min(location) and max(location) <= 7

    def check_direction(self, board: np.array, location: tuple, direction: Directions) -> bool:
        new_location = np.array(location) + direction.array
        if not self.in_bounds(new_location):
            return False

        return board[tuple(new_location)] == Item.Passage.value

    def reverse_path(self, came_from: dict, came_from_direction: dict, goal_location: tuple) -> list:
        current = goal_location
        parent = came_from.get(goal_location, None)
        path = []

        while parent is not None:
            path.append(came_from_direction[current])
            current, parent = parent, came_from.get(parent, None)
        return list(reversed(path))

    def create_path(self, board: np.array, my_location: tuple, goal_location: tuple) -> list:
        to_visit = [my_location]
        visited = []

        came_from = dict()
        came_from[my_location] = None

        came_from_direction = dict()
        came_from_direction[my_location] = Directions.ZERO

        while to_visit:
            point = to_visit.pop(0)
            if point == goal_location: break
            for direction in Directions.NEIGHBORS:
                new_point = tuple(np.array(point) + direction.array)

                if not self.in_bounds(new_point):
                    continue

                if new_point in visited:
                    continue

                if self.check_direction(board, point, direction):
                    to_visit.append(new_point)
                    came_from[new_point] = point
                    came_from_direction[new_point] = direction

            visited.append(point)
        return self.reverse_path(came_from, came_from_direction, goal_location)
