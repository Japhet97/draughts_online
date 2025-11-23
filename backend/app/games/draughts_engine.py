from typing import List, Tuple, Optional
import copy


class DraughtsEngine:
    """
    Complete Draughts/Checkers game engine with AI.
    8x8 board, standard international rules.
    """
    
    def __init__(self):
        self.board = self.initialize_board()
        self.current_player = 1  # 1 = Player 1 (bottom), 2 = Player 2 (top)
        self.move_history = []
        
    def initialize_board(self) -> List[List[int]]:
        """
        Initialize standard 8x8 draughts board.
        0 = empty, 1 = player1 piece, 2 = player2 piece
        -1 = player1 king, -2 = player2 king
        """
        board = [[0 for _ in range(8)] for _ in range(8)]
        
        # Player 2 pieces (top)
        for row in range(3):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 2
        
        # Player 1 pieces (bottom)
        for row in range(5, 8):
            for col in range(8):
                if (row + col) % 2 == 1:
                    board[row][col] = 1
        
        return board
    
    def get_board_state(self) -> dict:
        """Get current board state as dictionary."""
        return {
            "board": self.board,
            "current_player": self.current_player,
            "move_count": len(self.move_history)
        }
    
    def set_board_state(self, state: dict):
        """Set board state from dictionary."""
        self.board = state.get("board", self.initialize_board())
        self.current_player = state.get("current_player", 1)
        self.move_history = state.get("move_history", [])
    
    def is_valid_position(self, row: int, col: int) -> bool:
        """Check if position is within board bounds."""
        return 0 <= row < 8 and 0 <= col < 8
    
    def get_piece(self, row: int, col: int) -> int:
        """Get piece at position."""
        if self.is_valid_position(row, col):
            return self.board[row][col]
        return None
    
    def is_king(self, piece: int) -> bool:
        """Check if piece is a king."""
        return piece < 0
    
    def get_player_pieces(self, player: int) -> List[Tuple[int, int]]:
        """Get all pieces for a player."""
        pieces = []
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == player or piece == -player:
                    pieces.append((row, col))
        return pieces
    
    def get_valid_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all valid moves for a piece at given position."""
        piece = self.get_piece(row, col)
        if piece == 0 or abs(piece) != self.current_player:
            return []
        
        moves = []
        captures = self.get_capture_moves(row, col)
        
        if captures:
            return captures
        
        # Normal moves
        directions = []
        if piece == 1:  # Player 1 regular piece
            directions = [(-1, -1), (-1, 1)]
        elif piece == 2:  # Player 2 regular piece
            directions = [(1, -1), (1, 1)]
        else:  # King piece
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            new_row, new_col = row + dr, col + dc
            if self.is_valid_position(new_row, new_col) and self.board[new_row][new_col] == 0:
                moves.append((new_row, new_col))
        
        return moves
    
    def get_capture_moves(self, row: int, col: int) -> List[Tuple[int, int]]:
        """Get all capture moves for a piece."""
        piece = self.get_piece(row, col)
        if piece == 0:
            return []
        
        captures = []
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        # Regular pieces can only move in certain directions for captures
        if piece == 1:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        elif piece == 2:
            directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]
        
        for dr, dc in directions:
            middle_row, middle_col = row + dr, col + dc
            landing_row, landing_col = row + 2*dr, col + 2*dc
            
            if not self.is_valid_position(middle_row, middle_col):
                continue
            if not self.is_valid_position(landing_row, landing_col):
                continue
            
            middle_piece = self.board[middle_row][middle_col]
            landing_piece = self.board[landing_row][landing_col]
            
            # Check if we can capture
            if middle_piece != 0 and abs(middle_piece) != abs(piece):
                if landing_piece == 0:
                    captures.append((landing_row, landing_col))
        
        return captures
    
    def must_capture(self) -> bool:
        """Check if current player must make a capture."""
        pieces = self.get_player_pieces(self.current_player)
        for row, col in pieces:
            if self.get_capture_moves(row, col):
                return True
        return False
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> bool:
        """
        Make a move on the board.
        Returns True if move was successful, False otherwise.
        """
        from_row, from_col = from_pos
        to_row, to_col = to_pos
        
        # Validate positions
        if not self.is_valid_position(from_row, from_col):
            return False
        if not self.is_valid_position(to_row, to_col):
            return False
        
        piece = self.board[from_row][from_col]
        
        # Check if it's the correct player's piece
        if abs(piece) != self.current_player:
            return False
        
        # Check if destination is empty
        if self.board[to_row][to_col] != 0:
            return False
        
        # Check if move is valid
        valid_moves = self.get_valid_moves(from_row, from_col)
        if to_pos not in valid_moves:
            return False
        
        # Check if this is a capture move
        is_capture = abs(to_row - from_row) == 2
        
        if is_capture:
            # Remove captured piece
            middle_row = (from_row + to_row) // 2
            middle_col = (from_col + to_col) // 2
            self.board[middle_row][middle_col] = 0
        
        # Move the piece
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = 0
        
        # Check for king promotion
        if piece == 1 and to_row == 0:
            self.board[to_row][to_col] = -1
        elif piece == 2 and to_row == 7:
            self.board[to_row][to_col] = -2
        
        # Record move
        self.move_history.append({
            "from": from_pos,
            "to": to_pos,
            "player": self.current_player,
            "capture": is_capture
        })
        
        # Switch player
        self.current_player = 3 - self.current_player
        
        return True
    
    def is_game_over(self) -> Tuple[bool, Optional[int]]:
        """
        Check if game is over.
        Returns (is_over, winner) where winner is None for draw.
        """
        # Check if current player has any pieces
        player1_pieces = self.get_player_pieces(1)
        player2_pieces = self.get_player_pieces(2)
        
        if not player1_pieces:
            return (True, 2)
        if not player2_pieces:
            return (True, 1)
        
        # Check if current player has any valid moves
        has_moves = False
        for row, col in self.get_player_pieces(self.current_player):
            if self.get_valid_moves(row, col):
                has_moves = True
                break
        
        if not has_moves:
            return (True, 3 - self.current_player)
        
        return (False, None)
    
    def evaluate_board(self, player: int) -> float:
        """
        Evaluate board position for a player.
        Used by AI to determine best move.
        """
        score = 0
        
        for row in range(8):
            for col in range(8):
                piece = self.board[row][col]
                if piece == 0:
                    continue
                
                piece_value = 0
                if abs(piece) == player:
                    # Our piece
                    if self.is_king(piece):
                        piece_value = 5
                    else:
                        piece_value = 3
                        # Bonus for pieces closer to promotion
                        if player == 1:
                            piece_value += (7 - row) * 0.1
                        else:
                            piece_value += row * 0.1
                    
                    score += piece_value
                else:
                    # Opponent piece
                    if self.is_king(piece):
                        piece_value = 5
                    else:
                        piece_value = 3
                    
                    score -= piece_value
        
        return score
    
    def get_all_valid_moves_for_player(self, player: int) -> List[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """Get all valid moves for a player."""
        all_moves = []
        pieces = self.get_player_pieces(player)
        
        # Check if any captures are available
        captures = []
        for from_pos in pieces:
            capture_moves = self.get_capture_moves(from_pos[0], from_pos[1])
            for to_pos in capture_moves:
                captures.append((from_pos, to_pos))
        
        if captures:
            return captures
        
        # No captures, return all normal moves
        for from_pos in pieces:
            moves = self.get_valid_moves(from_pos[0], from_pos[1])
            for to_pos in moves:
                all_moves.append((from_pos, to_pos))
        
        return all_moves
