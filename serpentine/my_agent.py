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
            goal_location = self.move_to_safe_location(obs, my_location)

            if self.can_place_bomb(obs['board'], obs['bomb_life'], obs['ammo'], my_location):
                self.queue.append(Action.Bomb)

            for direction in self.create_path(board, my_location, goal_location):
                self.queue.append(direction.action)

            if not self.queue:
                self.queue.append(Action.Stop)

        return self.queue.pop(0)

    def in_bounds(self, location: tuple) -> bool:
        return 0 <= min(location) and max(location) <= 7

    def check_direction(self, board: np.array, location: tuple, direction: Direction) -> bool:
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
            if point == goal_location:
                break
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

    def can_place_bomb(self, board: np.ndarray, bomb_life: np.ndarray, ammo: int, my_location: tuple) -> bool:
        return bomb_life[my_location] == 0 and ammo > 0 and self.find_explodable_neighbours(board, my_location)

    def create_danger_map(self, obs: dict) -> np.ndarray:
        danger_map = obs['flame_life']
        danger_map[danger_map > 0] = 1

        bombs = np.where(obs['bomb_life'] > 0)
        bombs_timers = map(int, obs['bomb_life'][bombs])
        bomb_strength = map(int, obs['bomb_blast_strength'][bombs])

        for row, col, timer, strength in zip(*bombs, bombs_timers, bomb_strength):
            strength -= 1

            row_low, row_high = max(row - strength, 0), min(row + strength, 7)
            col_low, col_high = max(col - strength, 0), min(col + strength, 7)

            for row_danger in range(row_low, row_high + 1):
                danger_map[row_danger, col] = timer

            for col_danger in range(col_low, col_high + 1):
                danger_map[row, col_danger] = timer

        return danger_map

    def find_reachable_safe_locations(self, board: np.ndarray, danger_map: np.ndarray, location: tuple) -> list:
        to_visit = [location]
        visited = []

        while to_visit:
            point = to_visit.pop(0)

            for direction in Directions.NEIGHBORS:
                new_point = tuple(np.array(point) + direction.array)

                if not self.in_bounds(new_point) or new_point in visited or danger_map[new_point] == 1:
                    continue

                if self.check_direction(board, point, direction):
                    to_visit.append(new_point)

            visited.append(point)

        return visited

    def move_to_safe_location(self, obs, location: tuple):

        danger_map = self.create_danger_map(obs)

        safe_locations = self.find_reachable_safe_locations(obs['board'], danger_map, location)
        fully_safe_locations = [location for location in safe_locations if danger_map[location] == 0]

        for safe_location in fully_safe_locations:
            if self.find_explodable_neighbours(obs['board'], safe_location):
                return safe_location

        if fully_safe_locations:
            return fully_safe_locations[0]
        return location

    def find_explodable_neighbours(self, board: np.ndarray, location: tuple) -> int:
        explodable_count = 0
        explodable = [Item.Agent1.value, Item.Wood.value, Item.ExtraBomb.value,
                      Item.IncrRange.value, Item.Kick.value]

        for direction in Directions.NEIGHBORS:
            new_point = tuple(direction.array + np.array(location))
            if self.in_bounds(new_point) and board[new_point] in explodable:
                explodable_count += 1

        return explodable_count
