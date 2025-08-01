if turn_step >= 2:  # Assuming turn_step 2 is for AI's turn
    ai_move = ai.get_best_move(white_pieces, white_locations, black_pieces, black_locations)
    # Update the game state with the AI's move
    black_locations[ai_move[0]] = ai_move[1]  # Move the piece
    # Check for captures, etc.
    turn_step = 0  # Switch back to player's turn