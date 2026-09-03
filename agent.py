# agent.py
import random


class GreedyGridAgent:
    """A simple agent that tries to move around systematically to clear the grid."""

    def __init__(self):
        self.actions_pool = ['Up', 'Down', 'Left', 'Right']

    def sense_and_act(self, percept: dict) -> str:
        pos = percept.get('agent_pos', [0, 0])
        return random.choice(self.actions_pool)


class SimpleReflexAgent:
    """Condition-action agent with no memory-based planning.

    This agent reacts only to the current percept, with no stored history.
    """

    def __init__(self):
        self.facing = 'Up'
        self.turn_left = {'Up': 'Left', 'Left': 'Down', 'Down': 'Right', 'Right': 'Up'}
        self.turn_right = {'Up': 'Right', 'Right': 'Down', 'Down': 'Left', 'Left': 'Up'}

    def sense_and_act(self, percept: dict) -> str:
        if percept.get('food_here'):
            action = self.facing
            return action

        if percept.get('wall_ahead'):
            action = self.turn_left[self.facing]
            self.facing = action
            return action

        action = self.facing
        return action


class ModelBasedAgent:
    """A simple model-based agent that remembers previously visited cells and avoids repeating dead-end loops."""

    def __init__(self):
        self.facing = 'Up'
        self.turn_left = {'Up': 'Left', 'Left': 'Down', 'Down': 'Right', 'Right': 'Up'}
        self.turn_right = {'Up': 'Right', 'Right': 'Down', 'Down': 'Left', 'Left': 'Up'}
        self.visited_cells = set()
        self.last_position = None
        self.last_action = None

    def _move(self, pos, direction):
        x, y = pos
        deltas = {'Up': (0, 1), 'Down': (0, -1), 'Left': (-1, 0), 'Right': (1, 0)}
        dx, dy = deltas[direction]
        return (x + dx, y + dy)

    def sense_and_act(self, percept: dict) -> str:
        pos = tuple(percept.get('agent_pos', (0, 0)))
        if self.last_position is not None and pos != self.last_position:
            self.visited_cells.add(self.last_position)
        self.visited_cells.add(pos)
        self.last_position = pos

        left_dir = self.turn_left[self.facing]
        right_dir = self.turn_right[self.facing]
        left_cell = self._move(pos, left_dir)
        right_cell = self._move(pos, right_dir)
        ahead_cell = self._move(pos, self.facing)

        if percept.get('food_here'):
            self.last_action = self.facing
            return self.facing

        if percept.get('wall_ahead'):
            if left_cell in self.visited_cells and right_cell not in self.visited_cells:
                action = right_dir
            elif right_cell in self.visited_cells and left_cell not in self.visited_cells:
                action = left_dir
            else:
                action = left_dir
            self.facing = action
            self.last_action = action
            return action

        if ahead_cell in self.visited_cells and left_cell not in self.visited_cells:
            action = left_dir
        elif ahead_cell in self.visited_cells and right_cell not in self.visited_cells:
            action = right_dir
        else:
            action = self.facing

        self.facing = action
        self.last_action = action
        return action


class SearchAgent:
    """Problem-solving / planning agent for search algorithms (BFS, DFS, UCS, A*)."""

    def __init__(self):
        self.plan = []
        self.active_algo = 'BFS'

