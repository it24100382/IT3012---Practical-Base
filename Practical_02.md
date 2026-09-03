# IT3012: Intelligent Agents - Practical 02
## Agent Architectures: Simple Reflex vs. Model-Based Agents

---

### Part 1: Practical Implementation Summary

- **Step 1.1 (Partial Observability):** Modified `get_percept()` in `visual_grid_game.py` to handicap the agent's perception from global coordinates `(agent_pos)` to local percept booleans (`wall_ahead`, `food_here`).
- **Step 1.2 (Simple Reflex Agent):** Implemented `SimpleReflexAgent` in `agent.py` using strict IF-THEN Condition-Action rules with zero percept history memory. Observed that under partial observability, the reflex agent gets trapped in infinite looping cycles around U-shaped walls.
- **Step 1.3 (Model-Based Agent):** Upgraded the architecture to `ModelBasedAgent` in `agent.py` by maintaining internal memory state (`visited_cells`, `last_position`, `last_action`). The agent updates its belief state model before acting, successfully detecting loops and taking alternate escape paths.

---

### Part 2: Theoretical Evaluation & Lecture Mapping

#### Question 1: Table-Driven Agent Limitations
**(Remember) According to Lecture 02, why is it impossible to program a mathematically perfect "Table-Driven Agent" for complex environments like Chess? What happens as the agent's lifetime increases?**

- **Combinatorial Explosion:** A Table-Driven Agent explicitly stores a lookup table mapping every possible percept sequence history to an optimal action ($T: \mathcal{P}^* \rightarrow \mathcal{A}$). In complex environments like Chess ($10^{120}$ possible game states) or grid navigation over time $T$, the size of the lookup table grows exponentially ($|\mathcal{P}|^T$).
- **Lifetime Escalation:** As the agent's lifetime $T$ increases, the number of possible percept histories becomes astronomically large. It requires infinite physical memory storage, impossible human lookup programming, and unfeasible search time. Thus, agent programs with state abstraction must replace explicit lookup tables.

---

#### Question 2: Condition-Action Rules Code Mapping
**(Understand) Look at the code you wrote for your `SimpleReflexAgent`. Identify and explain the specific lines of code that represent the "Condition-Action Rules" discussed in the lecture.**

In `agent.py`, the following lines in `SimpleReflexAgent.sense_and_act()` represent Condition-Action rules ($\text{IF condition THEN action}$):

```python
# Condition-Action Rule 1: IF food is detected at current position THEN collect / stay on food
if percept.get('food_here'):
    return self.facing

# Condition-Action Rule 2: IF wall is ahead THEN turn left
if percept.get('wall_ahead'):
    self.facing = self.turn_left[self.facing]
    return self.facing

# Default Action Rule: ELSE move forward
return self.facing
```
- **Explanation:** Each `if` statement checks an immediate sensor boolean (the **Condition**) and directly returns a motor movement action (the **Action**) without referencing past states or future consequences.

---

#### Question 3: Reflex Agent Infinite Loop Failure Analysis
**(Analyze) Your `SimpleReflexAgent` likely got stuck in an infinite loop during Step 1.2. Based on the lecture, analyze exactly why this happened. How did the combination of "Partial Observability" and a lack of "Percept History" cause this failure?**

- **Identical Percepts at Different States:** Under Partial Observability, global position coordinates are hidden. When the agent arrives at position $A$ facing a wall, its percept is `{'wall_ahead': True, 'food_here': False}`. When it turns left, steps forward, hits a wall at $B$, turns left, and returns to $A$, its percept is *identically* `{'wall_ahead': True, 'food_here': False}`.
- **Lack of Memory (No Percept History):** Because the reflex agent has no memory of ever visiting $A$ before or executing previous turns, it cannot distinguish state $(A, \text{turn}_1)$ from $(A, \text{turn}_2)$. Applying deterministic condition-action rules to identical percepts produces identical actions every cycle, trapping the agent in an infinite deterministic loop.

---

#### Question 4: Model-Based Agent State Evaluation
**(Evaluate) In Step 1.3, you added an internal state to your `ModelBasedAgent`. Evaluate how your specific code handles the "Transition Model" (how the world evolves) and the "Sensor Model" (how the agent's actions affect the world).**

- **Transition Model:** Handled by `_move(pos, direction)` and internal memory state updates:
  ```python
  pos = tuple(percept.get('agent_pos', (0, 0)))
  if self.last_position is not None and pos != self.last_position:
      self.visited_cells.add(self.last_position)
  self.visited_cells.add(pos)
  ```
  This tracks how the environment evolves as a result of movement actions over time, updating the agent's internal map belief.
- **Sensor Model:** Handled by evaluating relative adjacent coordinates (`ahead_cell`, `left_cell`, `right_cell`) against `self.visited_cells` before choosing an action:
  ```python
  if ahead_cell in self.visited_cells and left_cell not in self.visited_cells:
      action = left_dir
  ```
  By combining sensor signals with predicted transition outcomes, the agent realizes when moving forward would re-enter a visited loop, allowing it to choose alternative unvisited directions and escape traps.
