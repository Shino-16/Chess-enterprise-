# two player chess in python with Pygame!
# part one, set up variables images and game loop

import pygame
import os

Ai_DEPTH = 3  # depth of AI search tree, not used in this part
pygame.init()
WIDTH = 1000
HEIGHT = 900
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('Two-Player Pygame Chess!')
font = pygame.font.Font('freesansbold.ttf', 20)
medium_font = pygame.font.Font('freesansbold.ttf', 40)
big_font = pygame.font.Font('freesansbold.ttf', 50)
timer = pygame.time.Clock()
fps = 60
# game variables and images
white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                   (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                   (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
captured_pieces_white = []
captured_pieces_black = []
# En passant target squares (None means no en passant available)
black_ep = None
white_ep = None
# 0 - whites turn no selection: 1-whites turn piece selected: 2- black turn no selection, 3 - black turn piece selected
turn_step = 0
selection = 100
valid_moves = []
# load in game piece images (queen, king, rook, bishop, knight, pawn) x 2
script_dir = os.path.dirname(os.path.abspath(__file__))
assets_path = os.path.join(script_dir, 'assets', 'images')

black_queen = pygame.image.load(os.path.join(assets_path, 'black queen.png'))
black_queen = pygame.transform.scale(black_queen, (80, 80))
black_queen_small = pygame.transform.scale(black_queen, (45, 45))
black_king = pygame.image.load(os.path.join(assets_path, 'black king.png'))
black_king = pygame.transform.scale(black_king, (80, 80))
black_king_small = pygame.transform.scale(black_king, (45, 45))
black_rook = pygame.image.load(os.path.join(assets_path, 'black rook.png'))
black_rook = pygame.transform.scale(black_rook, (80, 80))
black_rook_small = pygame.transform.scale(black_rook, (45, 45))
black_bishop = pygame.image.load(os.path.join(assets_path, 'black bishop.png'))
black_bishop = pygame.transform.scale(black_bishop, (80, 80))
black_bishop_small = pygame.transform.scale(black_bishop, (45, 45))
black_knight = pygame.image.load(os.path.join(assets_path, 'black knight.png'))
black_knight = pygame.transform.scale(black_knight, (80, 80))
black_knight_small = pygame.transform.scale(black_knight, (45, 45))
black_pawn = pygame.image.load(os.path.join(assets_path, 'black pawn.png'))
black_pawn = pygame.transform.scale(black_pawn, (65, 65))
black_pawn_small = pygame.transform.scale(black_pawn, (45, 45))
white_queen = pygame.image.load(os.path.join(assets_path, 'white queen.png'))
white_queen = pygame.transform.scale(white_queen, (80, 80))
white_queen_small = pygame.transform.scale(white_queen, (45, 45))
white_king = pygame.image.load(os.path.join(assets_path, 'white king.png'))
white_king = pygame.transform.scale(white_king, (80, 80))
white_king_small = pygame.transform.scale(white_king, (45, 45))
white_rook = pygame.image.load(os.path.join(assets_path, 'white rook.png'))
white_rook = pygame.transform.scale(white_rook, (80, 80))
white_rook_small = pygame.transform.scale(white_rook, (45, 45))
white_bishop = pygame.image.load(os.path.join(assets_path, 'white bishop.png'))
white_bishop = pygame.transform.scale(white_bishop, (80, 80))
white_bishop_small = pygame.transform.scale(white_bishop, (45, 45))
white_knight = pygame.image.load(os.path.join(assets_path, 'white knight.png'))
white_knight = pygame.transform.scale(white_knight, (80, 80))
white_knight_small = pygame.transform.scale(white_knight, (45, 45))
white_pawn = pygame.image.load(os.path.join(assets_path, 'white pawn.png'))
white_pawn = pygame.transform.scale(white_pawn, (65, 65))
white_pawn_small = pygame.transform.scale(white_pawn, (45, 45))
white_images = [white_pawn, white_queen, white_king, white_knight, white_rook, white_bishop]
small_white_images = [white_pawn_small, white_queen_small, white_king_small, white_knight_small,
                      white_rook_small, white_bishop_small]
black_images = [black_pawn, black_queen, black_king, black_knight, black_rook, black_bishop]
small_black_images = [black_pawn_small, black_queen_small, black_king_small, black_knight_small,
                      black_rook_small, black_bishop_small]
piece_list = ['pawn', 'queen', 'king', 'knight', 'rook', 'bishop']
# check variables/ flashing counter
counter = 0
winner = ''
game_over = False


# draw main game board
def draw_board():
    # Enhanced board colors - classic wood/marble style
    light_square = (240, 217, 181)  # Light wood color
    dark_square = (181, 136, 99)    # Dark wood color
    
    for i in range(32):
        column = i % 4
        row = i // 4
        if row % 2 == 0:
            pygame.draw.rect(screen, light_square, [600 - (column * 200), row * 100, 100, 100])
        else:
            pygame.draw.rect(screen, light_square, [700 - (column * 200), row * 100, 100, 100])
    
    # Add subtle border effects to squares
    for i in range(8):
        for j in range(8):
            square_color = light_square if (i + j) % 2 == 0 else dark_square
            pygame.draw.rect(screen, square_color, [i * 100, j * 100, 100, 100])
            
            # Add subtle 3D effect
            highlight_color = tuple(min(255, c + 20) for c in square_color)
            shadow_color = tuple(max(0, c - 20) for c in square_color)
            
            # Top and left borders (highlight)
            pygame.draw.line(screen, highlight_color, (i * 100, j * 100), ((i + 1) * 100 - 1, j * 100), 1)
            pygame.draw.line(screen, highlight_color, (i * 100, j * 100), (i * 100, (j + 1) * 100 - 1), 1)
            
            # Bottom and right borders (shadow)
            pygame.draw.line(screen, shadow_color, (i * 100, (j + 1) * 100 - 1), ((i + 1) * 100 - 1, (j + 1) * 100 - 1), 1)
            pygame.draw.line(screen, shadow_color, ((i + 1) * 100 - 1, j * 100), ((i + 1) * 100 - 1, (j + 1) * 100 - 1), 1)
    
    # Enhanced UI panels
    pygame.draw.rect(screen, (45, 45, 45), [0, 800, WIDTH, 100])  # Darker status bar
    pygame.draw.rect(screen, (255, 215, 0), [0, 800, WIDTH, 100], 3)  # Gold border
    pygame.draw.rect(screen, (60, 60, 60), [800, 0, 200, HEIGHT])  # Darker side panel
    pygame.draw.rect(screen, (255, 215, 0), [800, 0, 200, HEIGHT], 3)  # Gold border
    
    # Enhanced status text with better styling
    status_text = ['White: Select a Piece to Move!', 'White: Select a Destination!',
                   'Black: Select a Piece to Move!', 'Black: Select a Destination!']
    
    # Add background for status text
    text_surface = big_font.render(status_text[turn_step], True, (255, 255, 255))
    text_bg = pygame.Surface((text_surface.get_width() + 20, text_surface.get_height() + 10))
    text_bg.fill((0, 0, 0))
    text_bg.set_alpha(100)
    screen.blit(text_bg, (10, 815))
    screen.blit(text_surface, (20, 820))
    
    # Enhanced grid lines
    for i in range(9):
        pygame.draw.line(screen, (139, 69, 19), (0, 100 * i), (800, 100 * i), 2)  # Brown grid
        pygame.draw.line(screen, (139, 69, 19), (100 * i, 0), (100 * i, 800), 2)
    
    # Enhanced forfeit button
    forfeit_rect = pygame.Rect(810, 820, 180, 40)
    pygame.draw.rect(screen, (139, 0, 0), forfeit_rect)  # Dark red background
    pygame.draw.rect(screen, (255, 255, 255), forfeit_rect, 2)  # White border
    forfeit_text = medium_font.render('FORFEIT', True, (255, 255, 255))
    screen.blit(forfeit_text, (810 + (180 - forfeit_text.get_width()) // 2, 830))


# draw pieces onto board
def draw_pieces():
    for i in range(len(white_pieces)):
        index = piece_list.index(white_pieces[i])
        if white_pieces[i] == 'pawn':
            # Enhanced pawn positioning with better graphics
            screen.blit(white_pawn, (white_locations[i][0] * 100 + 22, white_locations[i][1] * 100 + 30))
        else:
            screen.blit(white_images[index], (white_locations[i][0] * 100 + 10, white_locations[i][1] * 100 + 10))
        
        # Add glow effect for selected white piece
        if turn_step < 2 and i == selection:
            glow_color = (255, 255, 0, 100)  # Yellow glow
            glow_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (50, 50), 45)
            screen.blit(glow_surface, (white_locations[i][0] * 100, white_locations[i][1] * 100))
            
            # Add pulsing border effect
            pulse_width = int(3 + 2 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
            pygame.draw.rect(screen, (255, 215, 0), 
                           [white_locations[i][0] * 100, white_locations[i][1] * 100, 100, 100], pulse_width)

    for i in range(len(black_pieces)):
        index = piece_list.index(black_pieces[i])
        if black_pieces[i] == 'pawn':
            screen.blit(black_pawn, (black_locations[i][0] * 100 + 22, black_locations[i][1] * 100 + 30))
        else:
            screen.blit(black_images[index], (black_locations[i][0] * 100 + 10, black_locations[i][1] * 100 + 10))
        
        # Add glow effect for selected black piece
        if turn_step >= 2 and i == selection:
            glow_color = (255, 0, 0, 100)  # Red glow
            glow_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, glow_color, (50, 50), 45)
            screen.blit(glow_surface, (black_locations[i][0] * 100, black_locations[i][1] * 100))
            
            # Add pulsing border effect
            pulse_width = int(3 + 2 * abs(pygame.time.get_ticks() % 1000 - 500) / 500)
            pygame.draw.rect(screen, (255, 100, 100), 
                           [black_locations[i][0] * 100, black_locations[i][1] * 100, 100, 100], pulse_width)
# function to check all pieces valid options on board
def check_options(pieces, locations, turn):
    moves_list = []
    all_moves_list = []
    for i in range((len(pieces))):
        location = locations[i]
        piece = pieces[i]
        if piece == 'pawn':
            moves_list = check_pawn(location, turn)
        elif piece == 'rook':
            moves_list = check_rook(location, turn)
        elif piece == 'knight':
            moves_list = check_knight(location, turn)
        elif piece == 'bishop':
            moves_list = check_bishop(location, turn)
        elif piece == 'queen':
            moves_list = check_queen(location, turn)
        elif piece == 'king':
            moves_list = check_king(location, turn)
        all_moves_list.append(moves_list)
    return all_moves_list


# check king valid moves
def check_king(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for kings, they can go one square any direction
    targets = [(1, 0), (1, 1), (1, -1), (-1, 0), (-1, 1), (-1, -1), (0, 1), (0, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check queen valid moves
def check_queen(position, color):
    moves_list = check_bishop(position, color)
    second_list = check_rook(position, color)
    for i in range(len(second_list)):
        moves_list.append(second_list[i])
    return moves_list


# check bishop moves
def check_bishop(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # up-right, up-left, down-right, down-left
        path = True
        chain = 1
        if i == 0:
            x = 1
            y = -1
        elif i == 1:
            x = -1
            y = -1
        elif i == 2:
            x = 1
            y = 1
        else:
            x = -1
            y = 1
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check rook moves
def check_rook(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    for i in range(4):  # down, up, right, left
        path = True
        chain = 1
        if i == 0:
            x = 0
            y = 1
        elif i == 1:
            x = 0
            y = -1
        elif i == 2:
            x = 1
            y = 0
        else:
            x = -1
            y = 0
        while path:
            if (position[0] + (chain * x), position[1] + (chain * y)) not in friends_list and \
                    0 <= position[0] + (chain * x) <= 7 and 0 <= position[1] + (chain * y) <= 7:
                moves_list.append((position[0] + (chain * x), position[1] + (chain * y)))
                if (position[0] + (chain * x), position[1] + (chain * y)) in enemies_list:
                    path = False
                chain += 1
            else:
                path = False
    return moves_list


# check valid pawn moves
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
        if (position[0], position[1] + 2) not in white_locations and \
                (position[0], position[1] + 2) not in black_locations and position[1] == 1:
            moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
        if (position[0], position[1] - 2) not in white_locations and \
                (position[0], position[1] - 2) not in black_locations and position[1] == 6:
            moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list

# check valid pawn moves (EN PASSANT INCLUDED)
def check_pawn(position, color):
    moves_list = []
    if color == 'white':
        if (position[0], position[1] + 1) not in white_locations and \
                (position[0], position[1] + 1) not in black_locations and position[1] < 7:
            moves_list.append((position[0], position[1] + 1))
            if (position[0], position[1] + 2) not in white_locations and \
                    (position[0], position[1] + 2) not in black_locations and position[1] == 1:
                moves_list.append((position[0], position[1] + 2))
        if (position[0] + 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) in black_locations:
            moves_list.append((position[0] - 1, position[1] + 1))
        # En passant
        if (position[0] + 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] + 1, position[1] + 1))
        if (position[0] - 1, position[1] + 1) == black_ep:
            moves_list.append((position[0] - 1, position[1] + 1))
    else:
        if (position[0], position[1] - 1) not in white_locations and \
                (position[0], position[1] - 1) not in black_locations and position[1] > 0:
            moves_list.append((position[0], position[1] - 1))
            if (position[0], position[1] - 2) not in white_locations and \
                    (position[0], position[1] - 2) not in black_locations and position[1] == 6:
                moves_list.append((position[0], position[1] - 2))
        if (position[0] + 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) in white_locations:
            moves_list.append((position[0] - 1, position[1] - 1))
        # En passant
        if (position[0] + 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] + 1, position[1] - 1))
        if (position[0] - 1, position[1] - 1) == white_ep:
            moves_list.append((position[0] - 1, position[1] - 1))
    return moves_list


# check valid knight moves
def check_knight(position, color):
    moves_list = []
    if color == 'white':
        enemies_list = black_locations
        friends_list = white_locations
    else:
        friends_list = black_locations
        enemies_list = white_locations
    # 8 squares to check for knights, they can go two squares in one direction and one in another
    targets = [(1, 2), (1, -2), (2, 1), (2, -1), (-1, 2), (-1, -2), (-2, 1), (-2, -1)]
    for i in range(8):
        target = (position[0] + targets[i][0], position[1] + targets[i][1])
        if target not in friends_list and 0 <= target[0] <= 7 and 0 <= target[1] <= 7:
            moves_list.append(target)
    return moves_list


# check for valid moves for just selected piece
def check_valid_moves():
    if turn_step < 2:
        options_list = white_options
    else:
        options_list = black_options
    valid_options = options_list[selection]
    return valid_options


# draw valid moves on screen
def draw_valid(moves):
    if turn_step < 2:
        color = (0, 255, 0, 80)  # Transparent green for white moves
        border_color = (0, 200, 0)
    else:
        color = (255, 100, 100, 80)  # Transparent red for black moves
        border_color = (200, 0, 0)
    
    for i in range(len(moves)):
        # Create transparent overlay for valid moves
        move_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        pygame.draw.rect(move_surface, color, (0, 0, 100, 100))
        
        # Add animated border effect
        time_factor = (pygame.time.get_ticks() % 2000) / 2000  # 2-second cycle
        border_width = int(2 + 3 * abs(time_factor - 0.5) * 2)
        
        screen.blit(move_surface, (moves[i][0] * 100, moves[i][1] * 100))
        pygame.draw.rect(screen, border_color, 
                        [moves[i][0] * 100, moves[i][1] * 100, 100, 100], border_width)
        
        # Add center dot to indicate possible move
        center_x = moves[i][0] * 100 + 50
        center_y = moves[i][1] * 100 + 50
        pygame.draw.circle(screen, border_color, (center_x, center_y), 8)
        pygame.draw.circle(screen, (255, 255, 255), (center_x, center_y), 6)


# draw captured pieces on side of screen
def draw_captured():
    for i in range(len(captured_pieces_white)):
        captured_piece = captured_pieces_white[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_black_images[index], (825, 5 + 50 * i))
    for i in range(len(captured_pieces_black)):
        captured_piece = captured_pieces_black[i]
        index = piece_list.index(captured_piece)
        screen.blit(small_white_images[index], (925, 5 + 50 * i))


# draw a flashing square around king if in check
def draw_check():
    if turn_step < 2:
        if 'king' in white_pieces:
            king_index = white_pieces.index('king')
            king_location = white_locations[king_index]
            for i in range(len(black_options)):
                if king_location in black_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark red', [white_locations[king_index][0] * 100 + 1,
                                                              white_locations[king_index][1] * 100 + 1, 100, 100], 5)
    else:
        if 'king' in black_pieces:
            king_index = black_pieces.index('king')
            king_location = black_locations[king_index]
            for i in range(len(white_options)):
                if king_location in white_options[i]:
                    if counter < 15:
                        pygame.draw.rect(screen, 'dark blue', [black_locations[king_index][0] * 100 + 1,
                                                               black_locations[king_index][1] * 100 + 1, 100, 100], 5)


def draw_game_over():
    pygame.draw.rect(screen, 'black', [200, 200, 400, 70])
    screen.blit(font.render(f'{winner} won the game!', True, 'white'), (210, 210))
    screen.blit(font.render(f'Press ENTER to Restart!', True, 'white'), (210, 240))


def draw_menu(selected):
    # Create a gradient background instead of solid black
    for y in range(HEIGHT):
        # Create a gradient from dark blue to dark gray
        color_value = int(20 + (y / HEIGHT) * 40)  # From 20 to 60
        color = (color_value, color_value, min(80, color_value + 20))  # Blue tint
        pygame.draw.line(screen, color, (0, y), (WIDTH, y))
    
    # Add a subtle chess pattern overlay
    for i in range(0, WIDTH, 100):
        for j in range(0, HEIGHT, 100):
            if (i // 100 + j // 100) % 2 == 0:
                overlay = pygame.Surface((100, 100))
                overlay.set_alpha(15)  # Very transparent
                overlay.fill((255, 255, 255))
                screen.blit(overlay, (i, j))
    
    # Enhanced title with shadow effect
    title_shadow = big_font.render("Pygame Chess", True, (50, 50, 50))  # Dark shadow
    title = big_font.render("Pygame Chess", True, (255, 215, 0))  # Gold color
    screen.blit(title_shadow, (WIDTH // 2 - title.get_width() // 2 + 3, 203))  # Shadow offset
    screen.blit(title, (WIDTH // 2 - title.get_width() // 2, 200))
    
    # Enhanced menu options with background boxes
    pvp_color = (220, 20, 60) if selected == 0 else (200, 200, 200)  # Crimson or light gray
    pve_color = (220, 20, 60) if selected == 1 else (200, 200, 200)
    
    # Draw background boxes for menu items
    pvp_rect = pygame.Rect(WIDTH // 2 - 200, 340, 400, 50)
    pve_rect = pygame.Rect(WIDTH // 2 - 200, 410, 400, 50)
    
    if selected == 0:
        pygame.draw.rect(screen, (40, 40, 40), pvp_rect)
        pygame.draw.rect(screen, pvp_color, pvp_rect, 3)
    else:
        pygame.draw.rect(screen, (30, 30, 30), pvp_rect)
        
    if selected == 1:
        pygame.draw.rect(screen, (40, 40, 40), pve_rect)
        pygame.draw.rect(screen, pve_color, pve_rect, 3)
    else:
        pygame.draw.rect(screen, (30, 30, 30), pve_rect)
    
    pvp_text = medium_font.render("1. Player vs Player", True, pvp_color)
    pve_text = medium_font.render("2. Player vs AI", True, pve_color)
    
    screen.blit(pvp_text, (WIDTH // 2 - pvp_text.get_width() // 2, 350))
    screen.blit(pve_text, (WIDTH // 2 - pve_text.get_width() // 2, 420))
    
    # Add instructions
    instruction_font = pygame.font.Font('freesansbold.ttf', 16)
    instructions = [
        "Use ↑/↓ or W/S to navigate",
        "Press ENTER or SPACE to select"
    ]
    for i, instruction in enumerate(instructions):
        text = instruction_font.render(instruction, True, (150, 150, 150))
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 500 + i * 25))
    
    pygame.display.flip()


def menu_loop():
    selected = 0
    while True:
        draw_menu(selected)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    selected = (selected - 1) % 2
                if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    selected = (selected + 1) % 2
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    return "pvp" if selected == 0 else "pve"


# Call this before your main game loop
game_mode = menu_loop()

# Only run the current game loop if PvP is selected
if game_mode == "pvp":
    # main game loop
    black_options = check_options(black_pieces, black_locations, 'black')
    white_options = check_options(white_pieces, white_locations, 'white')
    run = True
    while run:
        timer.tick(fps)
        if counter < 30:
            counter += 1
        else:
            counter = 0
        screen.fill('dark gray')
        draw_board()
        draw_pieces()
        draw_captured()
        draw_check()
        if selection != 100:
            valid_moves = check_valid_moves()
            draw_valid(valid_moves)
        # event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over:
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)
                if turn_step <= 1:
                    if click_coords == (8, 8) or click_coords == (9, 8):
                        winner = 'black'
                    if click_coords in white_locations:
                        selection = white_locations.index(click_coords)
                        if turn_step == 0:
                            turn_step = 1
                    if click_coords in valid_moves and selection != 100:
                        white_locations[selection] = click_coords
                        if click_coords in black_locations:
                            black_piece = black_locations.index(click_coords)
                            captured_pieces_white.append(black_pieces[black_piece])
                            if black_pieces[black_piece] == 'king':
                                winner = 'white'
                            black_pieces.pop(black_piece)
                            black_locations.pop(black_piece)
                        # --- Pawn promotion for white ---
                        if white_pieces[selection] == 'pawn' and white_locations[selection][1] == 7:
                            white_pieces[selection] = 'queen'
                        if white_pieces[selection] == 'pawn' and white_locations[selection] == black_ep:
                            ep_capture = (black_ep[0], black_ep[1] - 1)
                            if ep_capture in black_locations:
                                idx = black_locations.index(ep_capture)
                                captured_pieces_white.append(black_pieces[idx])
                                black_pieces.pop(idx)
                                black_locations.pop(idx)
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 2
                        selection = 100
                        valid_moves = []
                if turn_step > 1:
                    if click_coords == (8, 8) or click_coords == (9, 8):
                        winner = 'white'
                    if click_coords in black_locations:
                        selection = black_locations.index(click_coords)
                        if turn_step == 2:
                            turn_step = 3
                    if click_coords in valid_moves and selection != 100:
                        black_locations[selection] = click_coords
                        if click_coords in white_locations:
                            white_piece = white_locations.index(click_coords)
                            captured_pieces_black.append(white_pieces[white_piece])
                            if white_pieces[white_piece] == 'king':
                                winner = 'black'
                            white_pieces.pop(white_piece)
                            white_locations.pop(white_piece)
                        # --- Pawn promotion for black ---
                        if black_pieces[selection] == 'pawn' and black_locations[selection][1] == 0:
                            black_pieces[selection] = 'queen'
                        if black_pieces[selection] == 'pawn' and black_locations[selection] == white_ep:
                            ep_capture = (white_ep[0], white_ep[1] + 1)
                            if ep_capture in white_locations:
                                idx = white_locations.index(ep_capture)
                                captured_pieces_black.append(white_pieces[idx])
                                white_pieces.pop(idx)
                                white_locations.pop(idx)
                        black_options = check_options(black_pieces, black_locations, 'black')
                        white_options = check_options(white_pieces, white_locations, 'white')
                        turn_step = 0
                        selection = 100
                        valid_moves = []
            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    game_over = False
                    winner = ''
                    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                       (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                       (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    captured_pieces_white = []
                    captured_pieces_black = []
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

        if winner != '':
            game_over = True
            draw_game_over()

        pygame.display.flip()
    pygame.quit()
elif game_mode == "pve":
    from ai import minimax  # Make sure ai.py is in the same folder

    black_options = check_options(black_pieces, black_locations, 'black')
    white_options = check_options(white_pieces, white_locations, 'white')
    run = True
    while run:
        timer.tick(fps)
        if counter < 30:
            counter += 1
        else:
            counter = 0
        screen.fill('dark gray')
        draw_board()
        draw_pieces()
        draw_captured()
        draw_check()
        if selection != 100:
            valid_moves = check_valid_moves()
            draw_valid(valid_moves)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            # Human (white) move
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and not game_over and turn_step <= 1:
                x_coord = event.pos[0] // 100
                y_coord = event.pos[1] // 100
                click_coords = (x_coord, y_coord)
                if click_coords == (8, 8) or click_coords == (9, 8):
                    winner = 'black'
                if click_coords in white_locations:
                    selection = white_locations.index(click_coords)
                    if turn_step == 0:
                        turn_step = 1
                if click_coords in valid_moves and selection != 100:
                    white_locations[selection] = click_coords
                    if click_coords in black_locations:
                        black_piece = black_locations.index(click_coords)
                        captured_pieces_white.append(black_pieces[black_piece])
                        if black_pieces[black_piece] == 'king':
                            winner = 'white'
                        black_pieces.pop(black_piece)
                        black_locations.pop(black_piece)
                    # --- Pawn promotion for white ---
                    if white_pieces[selection] == 'pawn' and white_locations[selection][1] == 7:
                        white_pieces[selection] = 'queen'
                    if white_pieces[selection] == 'pawn' and white_locations[selection] == black_ep:
                        ep_capture = (black_ep[0], black_ep[1] - 1)
                        if ep_capture in black_locations:
                            idx = black_locations.index(ep_capture)
                            captured_pieces_white.append(black_pieces[idx])
                            black_pieces.pop(idx)
                            black_locations.pop(idx)
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')
                    turn_step = 2
                    selection = 100
                    valid_moves = []

            if event.type == pygame.KEYDOWN and game_over:
                if event.key == pygame.K_RETURN:
                    game_over = False
                    winner = ''
                    white_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    white_locations = [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0), (6, 0), (7, 0),
                                       (0, 1), (1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1), (7, 1)]
                    black_pieces = ['rook', 'knight', 'bishop', 'king', 'queen', 'bishop', 'knight', 'rook',
                                    'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn', 'pawn']
                    black_locations = [(0, 7), (1, 7), (2, 7), (3, 7), (4, 7), (5, 7), (6, 7), (7, 7),
                                       (0, 6), (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6), (7, 6)]
                    captured_pieces_white = []
                    captured_pieces_black = []
                    turn_step = 0
                    selection = 100
                    valid_moves = []
                    black_options = check_options(black_pieces, black_locations, 'black')
                    white_options = check_options(white_pieces, white_locations, 'white')

        # AI (black) move
        if not game_over and turn_step > 1 and winner == '':
            _, move = minimax(white_pieces, white_locations, black_pieces, black_locations, Ai_DEPTH, False, check_options)
            if move and isinstance(move, tuple) and len(move) == 2:
                piece_index, new_location = move
                black_locations[piece_index] = new_location
                # --- Pawn promotion for black (AI) ---
                if black_pieces[piece_index] == 'pawn' and black_locations[piece_index][1] == 0:
                    black_pieces[piece_index] = 'queen'
                if new_location in white_locations:
                    white_piece = white_locations.index(new_location)
                    captured_pieces_black.append(white_pieces[white_piece])
                    if white_pieces[white_piece] == 'king':
                        winner = 'black'
                    white_pieces.pop(white_piece)
                    white_locations.pop(white_piece)
                black_options = check_options(black_pieces, black_locations, 'black')
                white_options = check_options(white_pieces, white_locations, 'white')
                turn_step = 0
                selection = 100
                valid_moves = []
            else:
                # No valid moves: check if black is in check (checkmate) or not (stalemate)
                if 'king' in black_pieces:
                    king_index = black_pieces.index('king')
                    king_location = black_locations[king_index]
                    in_check = False
                    for moves in white_options:
                        if king_location in moves:
                            in_check = True
                            break
                    if in_check:
                        winner = 'white'  # checkmate
                    else:
                        winner = 'draw'   # stalemate
                else:
                    winner = 'white'  # king captured

        if winner != '':
            game_over = True
            draw_game_over()

        pygame.display.flip()
    pygame.quit()
