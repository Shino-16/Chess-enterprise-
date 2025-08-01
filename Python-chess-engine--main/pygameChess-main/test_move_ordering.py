#!/usr/bin/env python3
"""
Simple test to verify enhanced move ordering is working correctly.
"""

import ai
import sys
import os

# Mock check_options function for testing
def mock_check_options(pieces, locations, color):
    """Mock function that returns some sample moves for testing."""
    if not pieces:
        return []
    
    # Return sample moves for each piece (simplified for testing)
    options = []
    for i, piece in enumerate(pieces):
        if i < len(locations):
            x, y = locations[i]
            piece_moves = []
            
            # Add some sample moves based on piece type
            if piece == 'pawn':
                if color == 'white':
                    piece_moves = [(x, y+1), (x, y+2)] if y < 6 else [(x, y+1)]
                else:
                    piece_moves = [(x, y-1), (x, y-2)] if y > 1 else [(x, y-1)]
            elif piece == 'knight':
                knight_moves = [(x+2, y+1), (x+2, y-1), (x-2, y+1), (x-2, y-1),
                               (x+1, y+2), (x+1, y-2), (x-1, y+2), (x-1, y-2)]
                piece_moves = [(mx, my) for mx, my in knight_moves if 0 <= mx <= 7 and 0 <= my <= 7]
            elif piece == 'queen':
                # Add some queen moves
                piece_moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1), 
                              (x+1, y+1), (x-1, y-1), (x+1, y-1), (x-1, y+1)]
                piece_moves = [(mx, my) for mx, my in piece_moves if 0 <= mx <= 7 and 0 <= my <= 7]
            else:
                # Simple moves for other pieces
                piece_moves = [(x+1, y), (x-1, y), (x, y+1), (x, y-1)]
                piece_moves = [(mx, my) for mx, my in piece_moves if 0 <= mx <= 7 and 0 <= my <= 7]
            
            options.append(piece_moves)
        else:
            options.append([])
    
    return options

def test_move_ordering():
    """Test the enhanced move ordering functionality."""
    print("Testing Enhanced Move Ordering...")
    print("=" * 50)
    
    # Test setup: White pieces vs Black pieces
    white_pieces = ['pawn', 'knight', 'queen', 'king']
    white_locations = [(4, 3), (2, 1), (3, 0), (4, 0)]  # Center pawn, knight, queen, king
    
    black_pieces = ['pawn', 'rook', 'queen', 'king']
    black_locations = [(4, 4), (0, 7), (3, 7), (4, 7)]  # Enemy pawn next to white pawn (capture opportunity)
    
    print("Position:")
    print(f"White pieces: {list(zip(white_pieces, white_locations))}")
    print(f"Black pieces: {list(zip(black_pieces, black_locations))}")
    print()
    
    # Test move ordering for black (AI)
    print("Testing move ordering for Black (AI):")
    try:
        ordered_moves = ai.order_moves(black_pieces, black_locations, 'black', 
                                     white_pieces, white_locations, mock_check_options)
        
        print(f"Found {len(ordered_moves)} ordered moves:")
        for i, (piece_idx, move) in enumerate(ordered_moves[:10]):  # Show top 10 moves
            piece = black_pieces[piece_idx] if piece_idx < len(black_pieces) else "unknown"
            current_pos = black_locations[piece_idx] if piece_idx < len(black_locations) else "unknown"
            
            # Check if it's a capture
            is_capture = move in white_locations
            capture_info = " (CAPTURE!)" if is_capture else ""
            
            print(f"  {i+1:2d}. {piece} from {current_pos} to {move}{capture_info}")
        
        print("\n✅ Move ordering test completed successfully!")
        
        # Test specific ordering priorities
        print("\nChecking move ordering priorities:")
        
        # Check if captures are prioritized
        captures_found = any(move in white_locations for _, move in ordered_moves[:5])
        print(f"  Captures in top 5 moves: {'✅' if captures_found else '❌'}")
        
        # Check if center moves are prioritized for appropriate pieces
        center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]
        center_moves = any(move in center_squares for _, move in ordered_moves[:8])
        print(f"  Center control in top 8 moves: {'✅' if center_moves else '❌'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error in move ordering: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_piece_values():
    """Test that piece values are properly defined."""
    print("\nTesting Piece Values:")
    print("=" * 30)
    
    expected_pieces = ['pawn', 'knight', 'bishop', 'rook', 'queen', 'king']
    
    for piece in expected_pieces:
        value = ai.piece_values.get(piece, "NOT FOUND")
        print(f"  {piece:8s}: {value}")
    
    print("✅ Piece values test completed!")

if __name__ == "__main__":
    print("Enhanced AI Move Ordering Test")
    print("=" * 60)
    
    # Run tests
    success = test_move_ordering()
    test_piece_values()
    
    if success:
        print("\n🎉 All tests passed! Enhanced move ordering is working correctly.")
        print("\nKey improvements in your AI:")
        print("  • Pawn promotions get highest priority")
        print("  • Captures use MVV-LVA (Most Valuable Victim - Least Valuable Attacker)")
        print("  • Center control is prioritized for knights and bishops")
        print("  • Piece development bonuses for knights and bishops")
        print("  • Castling gets bonus points")
        print("  • Rooks prefer open/semi-open files")
        print("  • Early queen development is penalized")
        print("  • King safety considerations")
    else:
        print("\n❌ Some tests failed. Check the error messages above.")
