# AgenticGames

AgenticGames is a Python project where different AI agents compete against each other in board games. The project was mainly built to explore adversarial search algorithms like minimax with alpha-beta pruning and compare them against simpler strategies like random move selection.

## Games Included

- Tic-Tac-Toe
- Standard Connect Four
- Extended Connect Four with randomized board sizes and win conditions
- 3-player Connect Four
- Hidden-information multiplayer Connect Four

## Agents

### GameAgent
Uses:
- Minimax search
- Alpha-beta pruning
- Move ordering with center preference
- Depth limiting for larger game boards

### Random_Agent
Chooses a random valid move each turn.

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
