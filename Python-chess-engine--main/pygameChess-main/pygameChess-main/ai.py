import copy
import numpy as np

# Piece-square tables for positional evaluation
PAWN_TABLE = np.array([
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5, 10, 10,-20,-20, 10, 10,  5],
    [ 5, -5,-10,  0,  0,-10, -5,  5],
    [ 0,  0,  0, 20, 20,  0,  0,  0],
    [ 5,  5, 10, 25, 25, 10,  5,  5],
    [10, 10, 20, 30, 30, 20, 10, 10],
    [50, 50, 50, 50, 50, 50, 50, 50],
    [ 0,  0,  0,  0,  0,  0,  0,  0]
])
KNIGHT_TABLE = np.array([
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20,   0,   5,   5,   0, -20, -40],
    [-30,   5,  10,  15,  15,  10,   5, -30],
    [-30,   0,  15,  20,  20,  15,   0, -30],
    [-30,   5,  15,  20,  20,  15,   0, -30],
    [-30,   0,  10,  15,  15,  10,   0, -30],
    [-40, -20,   0,   0,   0,   0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
])
BISHOP_TABLE = np.array([
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10,   5,   0,   0,   0,   0,   5, -10],
    [-10,  10,  10,  10,  10,  10,  10, -10],
    [-10,   0,  10,  10,  10,  10,   0, -10],
    [-10,   5,   5,  10,  10,   5,   5, -10],
    [-10,   0,   5,  10,  10,   5,   0, -10],
    [-10,   0,   0,   0,   0,   0,   0, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
])
ROOK_TABLE = np.array([
    [ 0,  0,  0,  5,  5,  0,  0,  0],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 5, 10, 10, 10, 10, 10, 10,  5],
    [ 0,  0,  0,  0,  0,  0,  0,  0]
])
QUEEN_TABLE = np.array([
    [-20, -10, -10, -5, -5, -10, -10, -20],
    [-10,   0,   5,  0,  0,   0,   0, -10],
    [-10,   5,   5,  5,  5,   5,   0, -10],
    [  0,   0,   5,  5,  5,   5,   0,  -5],
    [ -5,   0,   5,  5,  5,   5,   0,  -5],
    [-10,   0,   5,  5,  5,   5,   0, -10],
    [-10,   0,   0,  0,  0,   0,   0, -10],
    [-20, -10, -10, -5, -5, -10, -10, -20]
])
KING_TABLE = np.array([
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [ 20,  20,   0,   0,   0,   0,  20,  20],
    [ 20,  30,  10,   0,   0,  10,  30,  20]
])

piece_values = {
    'pawn': 100,
    'knight': 320,
    'bishop': 330,
    'rook': 500,
    'queen': 900,
    'king': 20000
}
piece_tables = {
    'pawn': PAWN_TABLE,
    'knight': KNIGHT_TABLE,
    'bishop': BISHOP_TABLE,
    'rook': ROOK_TABLE,
    'queen': QUEEN_TABLE,
    'king': KING_TABLE
}

def evaluate_board(white_pieces, white_locations, black_pieces, black_locations, move_generator=None, move_history=None):
    score = 0
    for i, piece in enumerate(white_pieces):
        score += piece_values.get(piece, 0)
        if piece in piece_tables:
            x, y = white_locations[i]
            # For white, flip the y-axis to match table orientation
            score += piece_tables[piece][7 - y][x]
    for i, piece in enumerate(black_pieces):
        score -= piece_values.get(piece, 0)
        if piece in piece_tables:
            x, y = black_locations[i]
            # For black, use table as-is
            score -= piece_tables[piece][y][x]

    # Mobility (number of moves)
    if move_generator is not None:
        white_mobility = sum(len(moves) for moves in move_generator(white_pieces, white_locations, 'white'))
        black_mobility = sum(len(moves) for moves in move_generator(black_pieces, black_locations, 'black'))
        score += 5 * (white_mobility - black_mobility)  # weight can be tuned

    # Pawn structure: doubled pawns & passed pawns
    score += pawn_structure_eval(white_pieces, white_locations, black_pieces, black_locations)

    # King safety (basic): penalty if king is exposed (few friendly pawns around)
    score += king_safety_eval(white_pieces, white_locations, black_pieces, black_locations)

    # Threats: bonus for attacking higher-value piece
    score += threats_eval(white_pieces, white_locations, black_pieces, black_locations)

    return score

def pawn_structure_eval(white_pieces, white_locations, black_pieces, black_locations):
    score = 0
    # Doubled pawns penalty
    for color, pieces, locs, sign in [
        ('white', white_pieces, white_locations, 1),
        ('black', black_pieces, black_locations, -1)
    ]:
        pawns = [x for i,x in enumerate(locs) if pieces[i] == 'pawn']
        files = [x[0] for x in pawns]
        for f in set(files):
            count = files.count(f)
            if count > 1:
                score -= sign * 15 * (count - 1)  # penalty per extra pawn

        # Passed pawns bonus (very basic)
        for px, py in pawns:
            if color == 'white':
                is_passed = not any(bx == px and by < py for bx, by in [black_locations[i] for i, p in enumerate(black_pieces) if p == 'pawn'])
                if is_passed:
                    score += 20
            else:
                is_passed = not any(wx == px and wy > py for wx, wy in [white_locations[i] for i, p in enumerate(white_pieces) if p == 'pawn'])
                if is_passed:
                    score -= 20
    return score

def king_safety_eval(white_pieces, white_locations, black_pieces, black_locations):
    score = 0
    # Simple: count friendly pawns near king
    for pieces, locs, sign in [
        (white_pieces, white_locations, 1),
        (black_pieces, black_locations, -1)
    ]:
        if 'king' in pieces:
            kidx = pieces.index('king')
            kx, ky = locs[kidx]
            pawns_near = 0
            for dx in [-1, 0, 1]:
                for dy in [-1, 0, 1]:
                    if dx == 0 and dy == 0: continue
                    tx, ty = kx+dx, ky+dy
                    if 0 <= tx <= 7 and 0 <= ty <= 7:
                        if (tx, ty) in [locs[i] for i, p in enumerate(pieces) if p == 'pawn']:
                            pawns_near += 1
            if pawns_near < 2:
                score -= sign * 30  # penalty for exposed king
    return score

def threats_eval(white_pieces, white_locations, black_pieces, black_locations):
    score = 0
    # Simple: if a piece is attacking an enemy piece of higher value, score bonus
    for (atk_pieces, atk_locs, def_pieces, def_locs, sign) in [
        (white_pieces, white_locations, black_pieces, black_locations, 1),
        (black_pieces, black_locations, white_pieces, white_locations, -1)
    ]:
        for i, (piece, loc) in enumerate(zip(atk_pieces, atk_locs)):
            # Attack squares for this piece (reuse your check_options logic if possible)
            # For speed, just use basic piece movement, not actual legal move gen
            targets = []
            if piece == 'pawn':
                dx = [1, -1]
                if sign == 1:
                    for d in dx:
                        targets.append((loc[0]+d, loc[1]+1))
                else:
                    for d in dx:
                        targets.append((loc[0]+d, loc[1]-1))
            elif piece == 'knight':
                for (dx,dy) in [(1,2),(1,-2),(2,1),(2,-1),(-1,2),(-1,-2),(-2,1),(-2,-1)]:
                    targets.append((loc[0]+dx, loc[1]+dy))
            elif piece == 'bishop':
                for d in range(1,8):
                    targets += [(loc[0]+d, loc[1]+d), (loc[0]-d, loc[1]+d), (loc[0]+d, loc[1]-d), (loc[0]-d, loc[1]-d)]
            elif piece == 'rook':
                for d in range(1,8):
                    targets += [(loc[0]+d, loc[1]), (loc[0]-d, loc[1]), (loc[0], loc[1]+d), (loc[0], loc[1]-d)]
            elif piece == 'queen':
                for d in range(1,8):
                    targets += [(loc[0]+d, loc[1]+d), (loc[0]-d, loc[1]+d), (loc[0]+d, loc[1]-d), (loc[0]-d, loc[1]-d)]
                    targets += [(loc[0]+d, loc[1]), (loc[0]-d, loc[1]), (loc[0], loc[1]+d), (loc[0], loc[1]-d)]
            elif piece == 'king':
                for dx in [-1,0,1]:
                    for dy in [-1,0,1]:
                        if dx == 0 and dy == 0: continue
                        targets.append((loc[0]+dx, loc[1]+dy))
            # Only board squares
            targets = [(x,y) for (x,y) in targets if 0<=x<=7 and 0<=y<=7]
            for t in targets:
                if t in def_locs:
                    j = def_locs.index(t)
                    if piece_values.get(piece,0) < piece_values.get(def_pieces[j],0):
                        score += sign * 10  # reward for attacking higher-value piece
    return score

def minimax(white_pieces, white_locations, black_pieces, black_locations, depth, maximizing, check_options, alpha=float('-inf'), beta=float('inf')):
    if depth == 0:
        return evaluate_board(white_pieces, white_locations, black_pieces, black_locations, check_options), None

    # Move ordering: prioritize captures first
    def order_moves(pieces, locations, color, enemy_pieces, enemy_locations):
        options = check_options(pieces, locations, color)
        moves = []
        for i, piece_moves in enumerate(options):
            for move in piece_moves:
                if move in enemy_locations:
                    moves.insert(0, (i, move))  # captures at front
                else:
                    moves.append((i, move))
        return moves

    if maximizing:
        max_eval = float('-inf')
        best_move = None
        moves = order_moves(white_pieces, white_locations, 'white', black_pieces, black_locations)
        for i, move in moves:
            wp, wl = copy.deepcopy(white_pieces), copy.deepcopy(white_locations)
            bp, bl = copy.deepcopy(black_pieces), copy.deepcopy(black_locations)
            wl[i] = move
            if move in bl:
                captured = bl.index(move)
                bp.pop(captured)
                bl.pop(captured)
            eval, _ = minimax(wp, wl, bp, bl, depth-1, False, check_options, alpha, beta)
            if eval > max_eval:
                max_eval = eval
                best_move = (i, move)
            alpha = max(alpha, eval)
            if beta <= alpha:
                break
        return max_eval, best_move
    else:
        min_eval = float('inf')
        best_move = None
        moves = order_moves(black_pieces, black_locations, 'black', white_pieces, white_locations)
        for i, move in moves:
            wp, wl = copy.deepcopy(white_pieces), copy.deepcopy(white_locations)
            bp, bl = copy.deepcopy(black_pieces), copy.deepcopy(black_locations)
            bl[i] = move
            if move in wl:
                captured = wl.index(move)
                wp.pop(captured)
                wl.pop(captured)
            eval, _ = minimax(wp, wl, bp, bl, depth-1, True, check_options, alpha, beta)
            if eval < min_eval:
                min_eval = eval
                best_move = (i, move)
            beta = min(beta, eval)
            if beta <= alpha:
                break
        return min_eval, best_move