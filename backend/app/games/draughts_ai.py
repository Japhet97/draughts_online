from typing import Tuple, Optional
import copy
import random
from app.games.draughts_engine import DraughtsEngine


class DraughtsAI:
    """
    AI opponent for Draughts using Minimax algorithm with alpha-beta pruning.
    """
    
    def __init__(self, difficulty: str = "expert"):
        self.difficulty = difficulty
        self.max_depth = self.get_depth_for_difficulty(difficulty)
    
    def get_depth_for_difficulty(self, difficulty: str) -> int:
        """Get search depth based on difficulty level."""
        depths = {
            "easy": 2,
            "medium": 4,
            "hard": 6,
            "expert": 8
        }
        return depths.get(difficulty, 6)
    
    def get_best_move(self, engine: DraughtsEngine) -> Optional[Tuple[Tuple[int, int], Tuple[int, int]]]:
        """
        Get the best move for the current player using Minimax with alpha-beta pruning.
        """
        player = engine.current_player
        best_move = None
        best_score = float('-inf')
        alpha = float('-inf')
        beta = float('inf')
        
        # Get all valid moves
        valid_moves = engine.get_all_valid_moves_for_player(player)
        
        if not valid_moves:
            return None
        
        # Add some randomness for lower difficulties
        if self.difficulty == "easy":
            # 30% chance to make a random move
            if random.random() < 0.3:
                return random.choice(valid_moves)
        elif self.difficulty == "medium":
            # 15% chance to make a random move
            if random.random() < 0.15:
                return random.choice(valid_moves)
        
        # Evaluate each move
        for from_pos, to_pos in valid_moves:
            # Make a copy of the engine to simulate the move
            temp_engine = copy.deepcopy(engine)
            temp_engine.make_move(from_pos, to_pos)
            
            # Evaluate this move
            score = self.minimax(temp_engine, self.max_depth - 1, alpha, beta, False, player)
            
            if score > best_score:
                best_score = score
                best_move = (from_pos, to_pos)
            
            alpha = max(alpha, best_score)
        
        return best_move
    
    def minimax(self, engine: DraughtsEngine, depth: int, alpha: float, beta: float, 
                is_maximizing: bool, original_player: int) -> float:
        """
        Minimax algorithm with alpha-beta pruning.
        """
        # Check if game is over
        is_over, winner = engine.is_game_over()
        if is_over:
            if winner == original_player:
                return 1000  # Win
            elif winner is None:
                return 0  # Draw
            else:
                return -1000  # Loss
        
        # Check depth limit
        if depth == 0:
            return engine.evaluate_board(original_player)
        
        if is_maximizing:
            max_eval = float('-inf')
            valid_moves = engine.get_all_valid_moves_for_player(engine.current_player)
            
            for from_pos, to_pos in valid_moves:
                temp_engine = copy.deepcopy(engine)
                temp_engine.make_move(from_pos, to_pos)
                
                eval_score = self.minimax(temp_engine, depth - 1, alpha, beta, False, original_player)
                max_eval = max(max_eval, eval_score)
                alpha = max(alpha, eval_score)
                
                if beta <= alpha:
                    break  # Beta cutoff
            
            return max_eval
        else:
            min_eval = float('inf')
            valid_moves = engine.get_all_valid_moves_for_player(engine.current_player)
            
            for from_pos, to_pos in valid_moves:
                temp_engine = copy.deepcopy(engine)
                temp_engine.make_move(from_pos, to_pos)
                
                eval_score = self.minimax(temp_engine, depth - 1, alpha, beta, True, original_player)
                min_eval = min(min_eval, eval_score)
                beta = min(beta, eval_score)
                
                if beta <= alpha:
                    break  # Alpha cutoff
            
            return min_eval
    
    def make_move(self, engine: DraughtsEngine) -> bool:
        """
        Make the AI's move on the board.
        Returns True if move was made, False otherwise.
        """
        best_move = self.get_best_move(engine)
        
        if best_move is None:
            return False
        
        from_pos, to_pos = best_move
        return engine.make_move(from_pos, to_pos)
