# IT3012: Intelligent Agents - Practical 01 / Tutorial 01
## Introduction to Intelligent Agents

---

### Part A: Conceptual Foundations

#### Question 1: Machine Learning Filter vs. Intelligent Agent

**Context:** Machine learning extracts static feature weights to map historical inputs to labels, whereas an intelligent agent builds a dynamic feedback loop that alters and reacts to its environment state.

##### 1.1 How does a Machine Learning model process data compared to an agent?
- **Machine Learning Model:** Processes data in an offline, batch, or pattern-recognition fashion ($f: X \rightarrow Y$). It maps static feature vectors to class labels or continuous numbers using pre-trained weights without an active environment state feedback loop. The model does not execute physical or environmental actions that change the source data generator.
- **Intelligent Agent:** Operates inside an active perception-action feedback loop ($\text{Percept} \rightarrow \text{Decision/Action} \rightarrow \text{Environment Change} \rightarrow \text{New Percept}$). An agent receives percepts $p_t$ from sensors, selects an action $a_t$ via its agent program, and executes $a_t$ using actuators to modify the external environment state $s_{t+1}$, which directly changes future percepts $p_{t+1}$.

##### 1.2 Does modifying the external environment state define an agent structure?
- Yes. Modifying the external environment state through actuators is a key defining characteristic of an agent structure. Pure computational classifiers (e.g. image filters) only output values. An agent, by definition, perceives its environment through sensors and acts upon that environment via actuators to alter the world state toward a goal or utility maximization.

---

#### Question 2: Rationality vs. Omniscience

**Context:** Omniscience requires absolute foreknowledge of real-world outcomes (impossible), while rationality maximizes expected utility based strictly on available percept history.

##### 2.1 Define omniscience and explain why it is non-trivial or impossible.
- **Omniscience** means knowing the actual, exact outcome of every action in advance with 100% certainty (absolute foreknowledge of future states).
- **Why it is non-trivial or impossible:** Real-world environments contain partial observability, unobserved variables, stochastic/random dynamics, complex non-deterministic multi-agent interactions, and chaotic events. Because an agent cannot perceive hidden parameters or future random events, perfect foreknowledge is physically and computationally impossible.

##### 2.2 How does expected utility bound rationality during unpredictable events?
- Rationality does not demand perfection or omniscience; it demands **expected utility maximization** conditioned strictly on the agent's available percept sequence history up to the present moment ($\max \mathbb{E}[U(a) \mid H]$). During unpredictable or stochastic events, a rational agent selects the action that mathematically yields the highest expected performance metric given its current belief state and knowledge.

---

### Part B: PEAS Framework & Metric Sabotage

#### Question 3: Fixing Naïve Metrics (Vacuum World)

**Context:** Performance measures must judge changes in external environment results rather than internal agent busywork to avoid score exploitation.

##### 3.1 Where should a performance metric measure changes?
- A performance metric must measure changes in the **external environment state** (e.g. the percentage of time the floor is clean, total food collected, energy conserved) rather than internal agent states or action execution counters (e.g. number of clean actions taken or motor steps).

##### 3.2 What is the classic vacuum world exploit behavior?
- If the performance metric rewards the agent per "suck" / "clean" action, a naïve reflex agent will exploit the metric by intentionally dumping dirt back onto a clean cell and cleaning it repeatedly, or moving back and forth endlessly between cells to farm points while leaving the rest of the environment dirty.

---

#### Question 4: Pharmacy Inventory PEAS Breakdown

**Context Specification:** The pharmacy system runs on a warehouse PC connected to a barcode laser scanner at checkout (input port), an HTTPS REST API link to suppliers, an email notification service for customer pickup alerts, and a pharmacist touch-terminal.

##### 4.1 Identify two distinct software/hardware Actuators (A) from the context description.
1. **HTTPS REST API link to suppliers:** Sends automated digital purchase orders and re-stocking HTTP payloads to external supplier web services.
2. **Email notification service:** Sends automated pickup ready alerts / messages to customer email addresses.

##### 4.2 Identify two distinct Sensors (S) from the context description.
1. **Barcode laser scanner at checkout:** Reads barcode optics/inputs to detect item sales and trigger stock level deductions.
2. **Pharmacist touch-terminal:** Captures touch/keyboard inputs from human pharmacists for stock check-ins, overrides, and manual adjustments.

---

### Part C: The 7 Environmental Complexity Dimensions

#### Question 5: Granular Crypto Trading Bot Classification

**Context Specification:** The bot streams public order books via WebSockets and sends API payloads. It operates in a multi-bot market where public ticker depth is visible, but private whale wallets and latency spikes are hidden.

##### 5.1 Is the trading environment fully or partially observable based on hidden whale data?
- **Partially Observable:** While public ticker depth and order books are visible via WebSocket streams, private whale wallet balances, pending off-chain over-the-counter (OTC) trades, hidden algorithmic orders, and future network latency spikes remain unobservable.

##### 5.2 Is it single-agent or multi-agent (competitive/cooperative)?
- **Multi-Agent (Competitive / Mixed):** The bot operates alongside numerous automated high-frequency trading (HFT) bots, institutional algorithms, retail traders, and market makers competing for order book depth, liquidity, and price advantage.

##### 5.3 Is the market static or dynamic? Continuous or discrete?
- **Dynamic:** The market order book state changes continuously in real-time while the agent is deliberating or processing past order data.
- **Continuous:** Both time (continuous sub-millisecond execution) and domain values (prices and order amounts) are continuous variables.
