# pygameChess

A simple two-player and player-vs-AI chess game built with Python and Pygame.

## Features

- Classic chess rules (including pawn promotion and en passant)
- Play against another human or the computer (AI)
- AI uses minimax with alpha-beta pruning and positional evaluation
- Visual board and piece movement using Pygame
- Captured pieces display
- Basic endgame detection (checkmate, stalemate)

## Requirements

- Python 3.x
- Pygame (`pip install pygame`)
- Numpy (`pip install numpy`)

## How to Run

1. **Install dependencies:**
    ```
    pip install pygame numpy
    ```

2. **Run the game:**
    ```
    python main.py
    ```

3. **Controls:**
    - Click pieces and destination squares to move.
    - Press `Enter` to restart after a game ends.

## File Structure

- `main.py` — Main game loop and UI
- `ai.py` — AI logic (minimax, evaluation)
- `constants.py` — Game constants and settings
- `assets/images/` — Piece images

## Notes

- Pawn promotion is automatic to queen.
- En passant is supported.
- AI search depth can be changed in `main.py` via the `AI_DEPTH` variable.

## Credits

- Chess piece images: [your source or attribution here]
- Built with [Pygame](https://www.pygame.org/)

---

Enjoy

### 1. **Understand the Current Codebase**
   - Familiarize yourself with the existing code in `main.py` and `constants.py`. Understand how the game loop works, how pieces are drawn, and how user interactions are handled.
   - Identify where the AI logic will fit into the existing structure. The AI will need to make decisions about moves based on the current game state.

### 2. **Define AI Logic**
   - **Choose an AI Algorithm**: Decide on the algorithm you want to implement for your AI. Common choices include:
     - Minimax Algorithm: A recursive algorithm that explores all possible moves and their outcomes.
     - Alpha-Beta Pruning: An optimization of the Minimax algorithm that reduces the number of nodes evaluated.
     - Monte Carlo Tree Search (MCTS): A probabilistic approach that explores the most promising moves based on random simulations.
   - **Evaluate Board States**: Create a function to evaluate the board state. This function should return a score based on the material balance, piece positions, and other strategic factors.

### 3. **Integrate AI into the Game Loop**
   - Modify the game loop in `main.py` to allow the AI to make moves when it's its turn. You can check if the current turn is the AI's and then call the AI function to determine the best move.
   - Ensure that the AI's move is executed in the same way as a player's move, updating the board state and redrawing the pieces.

### 4. **Implement Move Generation**
   - Create a function to generate all possible moves for a given player. This function should consider the current board state and the rules of chess.
   - Use the move generation function in your AI logic to explore possible future states.

### 5. **Testing and Debugging**
   - Test the AI against itself or against a human player. Observe its behavior and make adjustments to the evaluation function and move generation as needed.
   - Debug any issues that arise during testing, ensuring that the AI makes legal moves and responds appropriately to player actions.

### 6. **Enhancements**
   - Once the basic AI is functioning, consider adding enhancements:
     - Difficulty Levels: Adjust the depth of the search or the evaluation function to create different difficulty levels.
     - Opening Book: Implement a database of opening moves to improve the AI's early game.
     - Endgame Tablebases: Use precomputed endgame positions to make optimal moves in the endgame.

### 7. **User Interface Improvements**
   - Consider adding visual indicators for the AI's moves, such as highlighting the selected piece and its destination.
   - Provide options for players to play against the AI, including difficulty settings.

### 8. **Documentation and Comments**
   - Document your code and add comments to explain the AI logic and any complex parts of the implementation. This will help you and others understand the code in the future.

### 9. **Future Features**
   - Think about additional features you might want to implement, such as saving and loading games, online multiplayer, or a graphical user interface for settings.

### Example AI Integration
Here’s a simple example of how you might integrate a basic AI move into your game loop:

```python
if turn_step == 2:  # Assuming 2 is black's turn
    ai_move = ai_decide_move(black_pieces, black_locations, white_pieces, white_locations)
    # Execute the AI move
    black_locations[ai_move[0]] = ai_move[1]  # Move the piece
    # Update game state
    black_options = check_options(black_pieces, black_locations, 'black')
    white_options = check_options(white_pieces, white_locations, 'white')
    turn_step = 0  # Switch turn to white
```

### Conclusion
By following these steps, you can effectively develop your AI chess engine project. Start with a simple implementation and gradually enhance it as you gain more experience and understanding of chess AI algorithms. Good luck!
