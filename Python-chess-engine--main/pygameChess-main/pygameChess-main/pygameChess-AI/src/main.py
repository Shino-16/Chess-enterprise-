if turn_step == 2:  # Assuming it's black's turn (AI)
    best_move = ai_move(black_pieces, black_locations, white_pieces, white_locations)
    # Execute the best move
    black_locations[selection] = best_move
    # Update game state, check for captures, etc.
    turn_step = 0  # Switch back to white's turn