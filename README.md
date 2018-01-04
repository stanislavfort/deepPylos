# deepPylos
Deep reinforcement learning for the board game <a href="https://en.wikipedia.org/wiki/Pylos_(board_game)">Pylos</a>

## Pylos
<a href="https://en.wikipedia.org/wiki/Pylos_(board_game)">Pylos</a> is a board game for two players. Players take turns and place stones on the board or on top of other stones. Special configurations of the board allow players to remove 0,1 or 2 of their own stones. The player whose stone ends up on the top wins.

## deepPylos
I will use deep reinforcement learning to train an agent for Pylos.

## Implemented so far:
* The game class that includes the <b>game mechanics</b>, handles (crude) board visualization, and can generate next moves from a board configuration. The board is internally represented as an integer.
* A test function that allows two agents to play the game against themselves.
* A random agent that chooses next step at random.
* A simple agent that evaluates the children of the current board and chooses the best.
* A minimax agent that can do minimax to an arbitrary depth and evaluates leaves using a simple evaluation function. It does not have a cache, alpha beta pruning, or iterative deepening yet.
