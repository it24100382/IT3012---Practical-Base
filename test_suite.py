import unittest
from agent import SimpleReflexAgent, ModelBasedAgent, SearchAgent
from visual_grid_game import VisualGridHuntGame


class TestTrapGeneration(unittest.TestCase):
    def test_toxic_traps_are_created_safely(self):
        game = VisualGridHuntGame(width=10, height=10, num_food=5)

        self.assertTrue(hasattr(game, 'toxic_traps'))
        self.assertIsInstance(game.toxic_traps, set)

        for pos in game.toxic_traps:
            self.assertNotEqual(pos, (0, 0))
            self.assertNotIn(pos, game.walls)
            self.assertNotIn(pos, game.food_positions)
            self.assertIn(pos[0], range(game.width))
            self.assertIn(pos[1], range(game.height))


class TestPractical1And2_ReflexAgents(unittest.TestCase):
    """
    Tests for Practicals 1 & 2: Simple Reflex and Model-Based Agents.
    Focuses on Condition-Action rules, partial observability, and memory.
    """

    def setUp(self):
        # Instantiate agents (assuming students have created these classes)
        try:
            self.simple_agent = SimpleReflexAgent()
            self.model_agent = ModelBasedAgent()
        except NameError:
            self.fail("Agent classes not found. Ensure SimpleReflexAgent and ModelBasedAgent are defined.")

    def test_simple_reflex_logic(self):
        """Test 1: Simple Reflex Agent should react purely to immediate percepts."""
        # Scenario A: Food is present -> Agent should want to collect/stay/move appropriately
        percept_food = {'wall_ahead': False, 'food_here': True}
        action = self.simple_agent.sense_and_act(percept_food)
        self.assertIsNotNone(action, "SimpleReflexAgent returned None instead of an action.")

        # Scenario B: Wall is ahead -> Agent must turn or change direction
        percept_wall = {'wall_ahead': True, 'food_here': False}
        action_wall = self.simple_agent.sense_and_act(percept_wall)
        self.assertIn(action_wall, ['Left', 'Right', 'Down', 'Up'],
                      "Agent did not output a valid movement action when facing a wall.")

    def test_model_based_memory(self):
        """Test 2: Model-Based Agent should maintain internal state to escape loops."""
        # Feed the exact same percept twice to simulate being stuck in a corner
        percept = {'wall_ahead': True, 'food_here': False}

        action_1 = self.model_agent.sense_and_act(percept)
        action_2 = self.model_agent.sense_and_act(percept)

        # A simple reflex agent would return the exact same action twice.
        # A model-based agent should remember the previous failure and try a DIFFERENT action.
        self.assertNotEqual(
            action_1,
            action_2,
            "ModelBasedAgent returned the exact same action twice in a row for the same percept. Internal state/memory is not working correctly."
        )


class TestPractical3_SearchAgent(unittest.TestCase):
    """
    Tests for Practical 3: Problem-Solving Agents.
    Focuses on offline planning and Breadth-First Search (BFS) implementation.
    """

    def setUp(self):
        try:
            self.search_agent = SearchAgent()
        except NameError:
            self.fail("SearchAgent class not found.")

    def test_bfs_shortest_path(self):
        """Test 3: BFS must find the optimal (shortest) path in a static maze."""
        # Mock Environment Data
        grid_size = (4, 4)
        start_pos = (0, 0)
        goal_pos = (3, 3)

        # Create a U-shaped wall trap that the agent must navigate around
        # Grid layout (S=Start, G=Goal, W=Wall):
        # 3 | . . . G
        # 2 | W W W .
        # 1 | . . . .
        # 0 | S W W .
        #   ---------
        #     0 1 2 3
        walls = [(1, 0), (2, 0), (0, 2), (1, 2), (2, 2)]

        # Run student's BFS algorithm
        try:
            path = self.search_agent.bfs_search(start_pos, goal_pos, walls, grid_size)
        except AttributeError:
            self.fail("bfs_search method not implemented in SearchAgent.")

        # Verify the path is valid and optimal
        self.assertIsNotNone(path, "BFS returned None. No path found.")
        self.assertIsInstance(path, list, "BFS should return a list of actions (strings).")

        # The shortest path taking Manhattan distance around these specific walls is exactly 6 steps.
        # Path: Up -> Right -> Right -> Right -> Up -> Up
        self.assertEqual(len(path), 6, f"BFS did not find the optimal path. Expected 6 steps, got {len(path)}.")

    def test_bfs_unreachable_goal(self):
        """Test 4: BFS must correctly return failure (None/Empty) if goal is blocked."""
        grid_size = (3, 3)
        start_pos = (0, 0)
        goal_pos = (2, 2)

        # Box the goal in completely
        walls = [(1, 2), (2, 1), (1, 1)]

        path = self.search_agent.bfs_search(start_pos, goal_pos, walls, grid_size)

        # The agent should realize it's impossible and return None or an empty list
        is_empty_or_none = (path is None) or (len(path) == 0)
        self.assertTrue(is_empty_or_none, "BFS should return None or [] when the goal is unreachable.")


class TestPractical4_InformedSearchAgent(unittest.TestCase):
    """
    Tests for Practical 4: Informed Search Agents & Heuristics.
    Focuses on Manhattan distance, Euclidean distance, and A* Search.
    """

    def setUp(self):
        try:
            self.search_agent = SearchAgent()
        except NameError:
            self.fail("SearchAgent class not found.")

    def test_heuristics(self):
        """Test 5: Verify Manhattan distance returns 7 and Euclidean returns 5.0 for (0,0) -> (3,4)."""
        start = (0, 0)
        goal = (3, 4)

        manhattan = self.search_agent.manhattan_distance(start, goal)
        euclidean = self.search_agent.euclidean_distance(start, goal)

        self.assertEqual(manhattan, 7, f"Expected Manhattan distance 7, got {manhattan}.")
        self.assertAlmostEqual(euclidean, 5.0, places=2, msg=f"Expected Euclidean distance 5.0, got {euclidean}.")

    def test_astar_search_optimal_path(self):
        """Test 6: A* Search must find optimal path around maze walls."""
        grid_size = (4, 4)
        start_pos = (0, 0)
        goal_pos = (3, 3)
        walls = [(1, 0), (2, 0), (0, 2), (1, 2), (2, 2)]

        path = self.search_agent.astar_search(start_pos, goal_pos, walls, grid_size, heuristic_type='manhattan')

        self.assertIsNotNone(path, "A* Search returned None. Path should be found.")
        self.assertEqual(len(path), 6, f"A* Search path expected 6 steps, got {len(path)}.")


if __name__ == '__main__':
    # Run the test suite
    print("=== IT3012: Intelligent Agents - Autograder Test Suite ===\n")
    unittest.main(verbosity=2)