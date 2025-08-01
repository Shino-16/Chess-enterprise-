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
    'knight': 300,
    'bishop': 350,
    'rook': 500,
    'queen': 900,
    'king': 2000000000  # King is invaluable, but we use a large number for evaluation
}
piece_tables = {
    'pawn': PAWN_TABLE,
    'knight': KNIGHT_TABLE,
    'bishop': BISHOP_TABLE,
    'rook': ROOK_TABLE,
    'queen': QUEEN_TABLE,
    'king': KING_TABLE
}

def is_king_in_check(own_pieces, own_locations, enemy_pieces, enemy_locations, check_options):
    if 'king' not in own_pieces:
        return False
    king_idx = own_pieces.index('king')
    king_pos = own_locations[king_idx]
    # Get all possible enemy moves
    all_options = check_options(enemy_pieces, enemy_locations, 'white' if own_pieces is not enemy_pieces else 'black')
    enemy_moves = []
    for piece_moves in all_options:
        enemy_moves.extend(piece_moves)
    return king_pos in enemy_moves

def evaluate_board(white_pieces, white_locations, black_pieces, black_locations, check_options=None, move_history=None):
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
    if check_options is not None:
        white_mobility = sum(len(moves) for moves in check_options(white_pieces, white_locations, 'white'))
        black_mobility = sum(len(moves) for moves in check_options(black_pieces, black_locations, 'black'))
        score += 5 * (white_mobility - black_mobility)  # weight can be tuned

    # Pawn structure: doubled pawns & passed pawns
    score += pawn_structure_eval(white_pieces, white_locations, black_pieces, black_locations)

    # King safety (basic): penalty if king is exposed (few friendly pawns around)
    score += king_safety_eval(white_pieces, white_locations, black_pieces, black_locations)

    # Threats: bonus for attacking higher-value piece
    score += threats_eval(white_pieces, white_locations, black_pieces, black_locations)

    # Extra: penalize being in check, so the AI will prioritize escaping check
    if check_options is not None:
        if is_king_in_check(white_pieces, white_locations, black_pieces, black_locations, check_options):
            score -= 50000  # Large penalty for being in check, adjust as needed
        if is_king_in_check(black_pieces, black_locations, white_pieces, white_locations, check_options):
            score += 50000

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

# Enhanced move ordering for better alpha-beta pruning
def order_moves(pieces, locations, color, enemy_pieces, enemy_locations, check_options):
    options = check_options(pieces, locations, color)
    moves_with_scores = []
    
    for i, piece_moves in enumerate(options):
        piece = pieces[i]
        for move in piece_moves:
            score = 0
            
            # 1. HIGHEST PRIORITY: Pawn Promotions
            if piece == 'pawn':
                if (color == 'white' and move[1] == 7) or (color == 'black' and move[1] == 0):
                    score += 9000  # Promote to queen
            
            # 2. HIGH PRIORITY: Captures (MVV-LVA)
            if move in enemy_locations:
                victim_index = enemy_locations.index(move)
                victim_piece = enemy_pieces[victim_index]
                victim_value = piece_values.get(victim_piece, 0)
                attacker_value = piece_values.get(piece, 0)
                # Most Valuable Victim - Least Valuable Attacker
                score += 8000 + victim_value - attacker_value
            
            # 3. MEDIUM PRIORITY: Center Control (especially for knights and bishops)
            center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
            extended_center = [(2, 2), (2, 3), (2, 4), (2, 5), 
                             (3, 2), (3, 5), (4, 2), (4, 5),
                             (5, 2), (5, 3), (5, 4), (5, 5)]
            
            if move in center_squares:
                if piece in ['knight', 'bishop']:
                    score += 60
                elif piece == 'pawn':
                    score += 40
                else:
                    score += 30
            elif move in extended_center:
                if piece in ['knight', 'bishop']:
                    score += 30
                elif piece == 'pawn':
                    score += 20
                else:
                    score += 15
            
            # 4. PIECE DEVELOPMENT BONUSES
            current_pos = locations[i]
            
            # Knight development from back rank
            if piece == 'knight':
                if (color == 'white' and current_pos[1] == 0) or (color == 'black' and current_pos[1] == 7):
                    if 2 <= move[0] <= 5:  # Developing toward center
                        score += 40
            
            # Bishop development
            if piece == 'bishop':
                if (color == 'white' and current_pos[1] == 0) or (color == 'black' and current_pos[1] == 7):
                    if 2 <= move[0] <= 5 and 2 <= move[1] <= 5:
                        score += 35
            
            # Castling (king moves 2 squares)
            if piece == 'king':
                if abs(move[0] - current_pos[0]) == 2:
                    score += 50  # Castling bonus
            
            # 5. PAWN STRUCTURE BONUSES
            if piece == 'pawn':
                # Pawn to 6th/7th rank (near promotion)
                if (color == 'white' and move[1] >= 5) or (color == 'black' and move[1] <= 2):
                    score += 25
                
                # Pawn advances (moving forward)
                if (color == 'white' and move[1] > current_pos[1]) or (color == 'black' and move[1] < current_pos[1]):
                    score += 10
            
            # 6. PIECE ACTIVITY BONUSES
            # Rook to open files (simplified check)
            if piece == 'rook':
                # Prefer files with fewer pawns
                friendly_pawns_on_file = sum(1 for j, pos in enumerate(locations) 
                                           if pieces[j] == 'pawn' and pos[0] == move[0])
                enemy_pawns_on_file = sum(1 for j, pos in enumerate(enemy_locations) 
                                        if enemy_pieces[j] == 'pawn' and pos[0] == move[0])
                
                if friendly_pawns_on_file == 0 and enemy_pawns_on_file == 0:
                    score += 25  # Open file
                elif friendly_pawns_on_file == 0:
                    score += 15  # Semi-open file
            
            # Queen development penalty (don't develop queen too early)
            if piece == 'queen':
                early_game = len([p for p in pieces if p in ['knight', 'bishop']]) > 3
                if early_game:
                    if (color == 'white' and move[1] > 2) or (color == 'black' and move[1] < 5):
                        score -= 20  # Penalty for early queen development
            
            # 7. KING SAFETY
            if piece == 'king':
                # Penalty for king moves in opening/middlegame
                total_pieces = len(pieces) + len(enemy_pieces)
                if total_pieces > 20:  # Opening/Middlegame
                    score -= 15
            
            moves_with_scores.append((score, i, move))
    
    # Sort by score (highest first) and return move tuples
    moves_with_scores.sort(reverse=True)
    return [(i, move) for score, i, move in moves_with_scores]

def minimax(white_pieces, white_locations, black_pieces, black_locations, depth, maximizing, check_options, alpha=float('-inf'), beta=float('inf')):
    if depth == 0:
        return evaluate_board(white_pieces, white_locations, black_pieces, black_locations, check_options), None
        options = check_options(pieces, locations, color)
        moves_with_scores = []
        
        for i, piece_moves in enumerate(options):
            piece = pieces[i]
            for move in piece_moves:
                score = 0
                
                # 1. HIGHEST PRIORITY: Pawn Promotions
                if piece == 'pawn':
                    if (color == 'white' and move[1] == 7) or (color == 'black' and move[1] == 0):
                        score += 9000  # Promote to queen
                
                # 2. HIGH PRIORITY: Captures (MVV-LVA)
                if move in enemy_locations:
                    victim_index = enemy_locations.index(move)
                    victim_piece = enemy_pieces[victim_index]
                    victim_value = piece_values.get(victim_piece, 0)
                    attacker_value = piece_values.get(piece, 0)
                    # Most Valuable Victim - Least Valuable Attacker
                    score += 8000 + victim_value - attacker_value
                
                # 3. MEDIUM PRIORITY: Center Control (especially for knights and bishops)
                center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
                extended_center = [(2, 2), (2, 3), (2, 4), (2, 5), 
                                 (3, 2), (3, 5), (4, 2), (4, 5),
                                 (5, 2), (5, 3), (5, 4), (5, 5)]
                
                if move in center_squares:
                    if piece in ['knight', 'bishop']:
                        score += 60
                    elif piece == 'pawn':
                        score += 40
                    else:
                        score += 30
                elif move in extended_center:
                    if piece in ['knight', 'bishop']:
                        score += 30
                    elif piece == 'pawn':
                        score += 20
                    else:
                        score += 15
                
                # 4. PIECE DEVELOPMENT BONUSES
                current_pos = locations[i]
                
                # Knight development from back rank
                if piece == 'knight':
                    if (color == 'white' and current_pos[1] == 0) or (color == 'black' and current_pos[1] == 7):
                        if 2 <= move[0] <= 5:  # Developing toward center
                            score += 40
                
                # Bishop development
                if piece == 'bishop':
                    if (color == 'white' and current_pos[1] == 0) or (color == 'black' and current_pos[1] == 7):
                        if 2 <= move[0] <= 5 and 2 <= move[1] <= 5:
                            score += 35
                
                # Castling (king moves 2 squares)
                if piece == 'king':
                    if abs(move[0] - current_pos[0]) == 2:
                        score += 50  # Castling bonus
                
                # 5. PAWN STRUCTURE BONUSES
                if piece == 'pawn':
                    # Pawn to 6th/7th rank (near promotion)
                    if (color == 'white' and move[1] >= 5) or (color == 'black' and move[1] <= 2):
                        score += 25
                    
                    # Pawn advances (moving forward)
                    if (color == 'white' and move[1] > current_pos[1]) or (color == 'black' and move[1] < current_pos[1]):
                        score += 10
                
                # 6. PIECE ACTIVITY BONUSES
                # Rook to open files (simplified check)
                if piece == 'rook':
                    # Prefer files with fewer pawns
                    friendly_pawns_on_file = sum(1 for j, pos in enumerate(locations) 
                                               if pieces[j] == 'pawn' and pos[0] == move[0])
                    enemy_pawns_on_file = sum(1 for j, pos in enumerate(enemy_locations) 
                                            if enemy_pieces[j] == 'pawn' and pos[0] == move[0])
                    
                    if friendly_pawns_on_file == 0 and enemy_pawns_on_file == 0:
                        score += 25  # Open file
                    elif friendly_pawns_on_file == 0:
                        score += 15  # Semi-open file
                
                # Queen development penalty (don't develop queen too early)
                if piece == 'queen':
                    early_game = len([p for p in pieces if p in ['knight', 'bishop']]) > 3
                    if early_game:
                        if (color == 'white' and move[1] > 2) or (color == 'black' and move[1] < 5):
                            score -= 20  # Penalty for early queen development
                
                # 7. KING SAFETY
                if piece == 'king':
                    # Penalty for king moves in opening/middlegame
                    total_pieces = len(pieces) + len(enemy_pieces)
                    if total_pieces > 20:  # Opening/Middlegame
                        score -= 15
                
                moves_with_scores.append((score, i, move))
        
        # Sort by score (highest first) and return move tuples
        moves_with_scores.sort(reverse=True)
        return [(i, move) for score, i, move in moves_with_scores]

    if maximizing:
        max_eval = float('-inf')
        best_move = None
        moves = order_moves(white_pieces, white_locations, 'white', black_pieces, black_locations, check_options)
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
        moves = order_moves(black_pieces, black_locations, 'black', white_pieces, white_locations, check_options)
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

# Main AI function called by the game
def getBestMove(white_pieces, white_locations, black_pieces, black_locations, check_options, depth=3):
    """
    Get the best move for black (AI) using enhanced minimax with move ordering.
    Returns (piece_index, move) tuple.
    """
    try:
        score, best_move = minimax(white_pieces, white_locations, black_pieces, black_locations, 
                                 depth, False, check_options)
        
        if best_move is None:
            # Fallback: find any legal move using enhanced ordering
            moves = order_moves(black_pieces, black_locations, 'black', white_pieces, white_locations, check_options)
            if moves:
                return moves[0]  # Return the best ordered move
            else:
                # Emergency fallback
                options = check_options(black_pieces, black_locations, 'black')
                for i, piece_moves in enumerate(options):
                    if piece_moves:
                        return i, piece_moves[0]
        
        return best_move
        
    except Exception as e:
        print(f"AI Error: {e}")
        # Emergency fallback: any legal move
        options = check_options(black_pieces, black_locations, 'black')
        for i, piece_moves in enumerate(options):
            if piece_moves:
                return i, piece_moves[0]
        return 0, (0, 0)  # Should never happen in a legal position
