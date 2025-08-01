def minimax(board, depth, is_maximizing):
    if depth == 0 or game_over(board):
        return evaluate_board(board)

    if is_maximizing:
        max_eval = float('-inf')
        for move in get_all_possible_moves(board, 'white'):
            evaluation = minimax(make_move(board, move), depth - 1, False)
            max_eval = max(max_eval, evaluation)
        return max_eval
    else:
        min_eval = float('inf')
        for move in get_all_possible_moves(board, 'black'):
            evaluation = minimax(make_move(board, move), depth - 1, True)
            min_eval = min(min_eval, evaluation)
        return min_eval