# agent.py
import math
import random
import heapq
from collections import deque


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
    """Problem-solving / planning agent using BFS, DFS, UCS, and A* Search algorithms."""

    def __init__(self):
        self.plan = []
        self.active_algo = 'AStar'
        self.directions = [('Up', (0, 1)), ('Down', (0, -1)), ('Left', (-1, 0)), ('Right', (1, 0))]

    def _get_neighbors(self, pos, walls, grid_size):
        x, y = pos
        width, height = grid_size
        walls_set = set(tuple(w) for w in walls)
        neighbors = []
        for action, (dx, dy) in self.directions:
            nx, ny = x + dx, y + dy
            if 0 <= nx < width and 0 <= ny < height and (nx, ny) not in walls_set:
                neighbors.append((action, (nx, ny)))
        return neighbors

    def manhattan_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal
        return abs(x1 - x2) + abs(y1 - y2)

    def euclidean_distance(self, pos, goal):
        x1, y1 = pos
        x2, y2 = goal
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

    def bfs_search(self, start_pos, goal_pos, walls, grid_size):
        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)
        if start_pos == goal_pos:
            return []

        queue = deque([(start_pos, [])])
        reached = {start_pos}

        while queue:
            curr_pos, path = queue.popleft()
            for action, neighbor in self._get_neighbors(curr_pos, walls, grid_size):
                if neighbor == goal_pos:
                    return path + [action]
                if neighbor not in reached:
                    reached.add(neighbor)
                    queue.append((neighbor, path + [action]))
        return None

    def dfs_search(self, start_pos, goal_pos, walls, grid_size):
        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)
        if start_pos == goal_pos:
            return []

        stack = [(start_pos, [])]
        reached = {start_pos}

        while stack:
            curr_pos, path = stack.pop()
            if curr_pos == goal_pos:
                return path

            for action, neighbor in self._get_neighbors(curr_pos, walls, grid_size):
                if neighbor not in reached:
                    reached.add(neighbor)
                    stack.append((neighbor, path + [action]))
        return None

    def ucs_search(self, start_pos, goal_pos, walls, grid_size):
        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)
        if start_pos == goal_pos:
            return []

        counter = 0
        pq = [(0, counter, start_pos, [])]
        reached = {start_pos: 0}

        while pq:
            g_cost, _, curr_pos, path = heapq.heappop(pq)
            if curr_pos == goal_pos:
                return path

            for action, neighbor in self._get_neighbors(curr_pos, walls, grid_size):
                new_g = g_cost + 1
                if neighbor not in reached or new_g < reached[neighbor]:
                    reached[neighbor] = new_g
                    counter += 1
                    heapq.heappush(pq, (new_g, counter, neighbor, path + [action]))
        return None

    def astar_search(self, start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan'):
        start_pos = tuple(start_pos)
        goal_pos = tuple(goal_pos)
        if start_pos == goal_pos:
            return []

        heuristic_fn = self.manhattan_distance if heuristic_type == 'manhattan' else self.euclidean_distance

        counter = 0
        h_start = heuristic_fn(start_pos, goal_pos)
        f_start = 0 + h_start

        # Tuple: (f_cost, g_cost, counter, current_pos, path_taken)
        pq = [(f_start, 0, counter, start_pos, [])]
        reached_states = {start_pos: 0}

        while pq:
            f_cost, g_cost, _, current_pos, path_taken = heapq.heappop(pq)
            if current_pos == goal_pos:
                return path_taken

            for action, neighbor in self._get_neighbors(current_pos, walls, grid_size):
                new_g = g_cost + 1
                if neighbor not in reached_states or new_g < reached_states[neighbor]:
                    reached_states[neighbor] = new_g
                    h_new = heuristic_fn(neighbor, goal_pos)
                    f_new = new_g + h_new
                    counter += 1
                    heapq.heappush(pq, (f_new, new_g, counter, neighbor, path_taken + [action]))
        return None

    def sense_and_act(self, percept: dict) -> str:
        if self.plan:
            return self.plan.pop(0)

        agent_pos = tuple(percept.get('agent_pos', (0, 0)))
        grid_size = percept.get('grid_size', (10, 10))
        walls = percept.get('walls', [])
        all_food = percept.get('all_food', [])

        if all_food:
            closest_food = min(all_food, key=lambda f: self.manhattan_distance(agent_pos, tuple(f)))
            goal_pos = tuple(closest_food)

            if self.active_algo == 'AStar':
                path = self.astar_search(agent_pos, goal_pos, walls, grid_size, heuristic_type='manhattan')
            elif self.active_algo == 'BFS':
                path = self.bfs_search(agent_pos, goal_pos, walls, grid_size)
            elif self.active_algo == 'DFS':
                path = self.dfs_search(agent_pos, goal_pos, walls, grid_size)
            elif self.active_algo == 'UCS':
                path = self.ucs_search(agent_pos, goal_pos, walls, grid_size)
            else:
                path = None

            if path:
                self.plan = list(path)
                return self.plan.pop(0)

        return 'Up'



