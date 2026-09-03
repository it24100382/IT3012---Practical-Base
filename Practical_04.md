# IT3012: Intelligent Agents - Practical 04
## Informed Search & Heuristics: A* Search Algorithm

---

### Part 1: Practical Implementation Summary

- **Step 1.1 (Heuristic Functions):** Implemented distance metric functions inside `SearchAgent`:
  - `manhattan_distance`: Calculates grid step distance $h(n) = |x_1 - x_2| + |y_1 - y_2|$. Verified checkpoint: $(0,0) \rightarrow (3,4)$ yields integer `7`.
  - `euclidean_distance`: Calculates straight-line distance $h(n) = \sqrt{(x_1 - x_2)^2 + (y_1 - y_2)^2}$. Verified checkpoint: $(0,0) \rightarrow (3,4)$ yields float `5.0`.
- **Step 1.2 (A* Search Implementation):** Created `astar_search()` using a Priority Queue (`heapq`) evaluating node priority $f(n) = g(n) + h(n)$. Stored tuple format: `(f_cost, g_cost, counter, current_pos, path_taken)`.
- **Step 1.3 (Decision Loop Integration):** Integrated `'AStar'` into `SearchAgent.sense_and_act()`, dynamically calculating optimal paths to remaining food items and executing offline step sequences.

---

### Part 2: Theoretical Evaluation & Lecture Mapping

#### Question 1: UCS vs. A* Node Prioritization
**(Understand) What is the key difference between how Uniform-Cost Search (UCS) and A* Search prioritize which node to explore next?**

- **UCS Evaluation Function ($f(n) = g(n)$):** Uniform-Cost Search prioritizes nodes strictly by path cost accumulated so far from the start state ($g(n)$). It explores blindly in expanding concentric cost circles without any directional knowledge of where the goal is located.
- **A* Evaluation Function ($f(n) = g(n) + h(n)$):** A* Search combines the path cost so far ($g(n)$) with an estimated cost to the goal ($h(n)$ heuristic). This heuristic evaluation steers node expansion directionally toward the goal, drastically reducing the search space and avoiding unnecessary expansions.

---

#### Question 2: Admissibility of Manhattan Distance
**(Analyze) In Step 1.1, you used Manhattan Distance. Why is Manhattan Distance considered an "admissible" heuristic for this specific 4-way movement grid, and what would happen to your A* algorithm if the heuristic was NOT admissible?**

- **Why Manhattan Distance is Admissible:** A heuristic $h(n)$ is admissible if it never overestimates the true cost to reach the goal ($h(n) \le h^*(n)$ for all nodes $n$). On a 2D grid restricted strictly to 4-way orthogonal movements ($\text{Up}, \text{Down}, \text{Left}, \text{Right}$), Manhattan distance represents the absolute minimum physical grid steps required between two points without obstacles. With obstacles present, the actual shortest path $h^*(n)$ can only be equal to or greater than Manhattan distance. Thus, $h(n) \le h^*(n)$ always holds.
- **Consequence of Non-Admissible Heuristic:** If $h(n)$ is not admissible (i.e. overestimates actual cost), $A^*$ Search loses its mathematical guarantee of optimality. $A^*$ may prematurely prune optimal paths and return a suboptimal solution.

---

#### Question 3: 8-Way Diagonal Movement & Alternative Heuristics
**(Evaluate) If we modified `visual_grid_game.py` to allow the agent to move diagonally (8-way movement), would Manhattan distance still be an admissible heuristic? Why or why not? Which metric should you switch to?**

- **Admissibility Failure:** No, Manhattan distance would **no longer be admissible**. In an 8-way movement grid, an agent can move diagonally from $(0,0)$ to $(1,1)$ in $1$ step (cost $1$ or $\sqrt{2} \approx 1.414$). However, Manhattan distance evaluates to $|1-0| + |1-0| = 2$. Because $h(n) = 2 > 1.414$, Manhattan distance overestimates the true optimal cost ($h(n) > h^*(n)$), violating admissibility.
- **Metric to Switch To:**
  - **Chebyshev Distance** (if diagonal cost $= 1$): $h(n) = \max(|x_1 - x_2|, |y_1 - y_2|)$.
  - **Octile Distance** (if diagonal cost $= \sqrt{2} \approx 1.414$): $h(n) = \Delta x + \Delta y + (\sqrt{2} - 2) \min(\Delta x, \Delta y)$.

---

#### Question 4: Multi-Food Heuristic Proposal
**(Create) When targeting multiple food items simultaneously, calculating the distance to just the single closest food item is a weak heuristic. Propose (in text) a stronger heuristic for navigating the grid to eat ALL remaining food efficiently.**

- **Proposed Multi-Food TSP Heuristic:** To visit all remaining food items efficiently, construct a combined heuristic function $h_{multi}(n)$ based on a **Minimum Spanning Tree (MST)**:
  $$h_{multi}(n) = \text{dist}(n, f_{\text{closest}}) + \text{weight}(\text{MST}(\mathcal{F}_{\text{remaining}}))$$
  1. Calculate the Manhattan/A* distance from current position $n$ to the nearest food pellet $f_{\text{closest}}$.
  2. Construct a complete graph where vertices are all uncollected food pellets $\mathcal{F}_{\text{remaining}}$, with edge weights equal to pairwise Manhattan distances between food items.
  3. Compute the total edge weight of the Minimum Spanning Tree (using Prim's or Kruskal's algorithm) connecting all remaining food vertices.
- **Why it is Stronger:** Since any valid path that eats all remaining food pellets must connect all food locations, the weight of the MST provides a tight, admissible lower bound on the Traveling Salesperson Problem (TSP) path cost, steering $A^*$ to clear the entire grid optimally.
