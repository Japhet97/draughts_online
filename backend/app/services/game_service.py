from sqlalchemy.orm import Session
from typing import Optional, Tuple
from app.models.models import Game, User, Transaction, GameMode, GameStatus, TransactionType
from app.games.draughts_engine import DraughtsEngine
from app.games.draughts_ai import DraughtsAI
from app.core.config import settings
import uuid


class GameService:
    """Service for managing game logic and state."""
    
    @staticmethod
    def calculate_commission(amount: float) -> float:
        """Calculate commission on winnings."""
        return amount * settings.COMMISSION_RATE
    
    @staticmethod
    def calculate_elo_change(winner_rating: int, loser_rating: int, k_factor: int = 32) -> Tuple[int, int]:
        """
        Calculate ELO rating changes for both players.
        Returns (winner_new_rating, loser_new_rating)
        """
        # Expected scores
        expected_winner = 1 / (1 + 10 ** ((loser_rating - winner_rating) / 400))
        expected_loser = 1 / (1 + 10 ** ((winner_rating - loser_rating) / 400))
        
        # New ratings
        winner_new = int(winner_rating + k_factor * (1 - expected_winner))
        loser_new = int(loser_rating + k_factor * (0 - expected_loser))
        
        return winner_new, loser_new
    
    @staticmethod
    def create_game_vs_ai(
        db: Session, 
        user_id: int, 
        bet_amount: float, 
        ai_difficulty: str = "expert"
    ) -> Optional[Game]:
        """Create a new game against AI."""
        user = db.query(User).filter(User.id == user_id).first()
        
        if not user:
            return None
        
        # Check if user has sufficient balance
        if user.balance < bet_amount:
            return None
        
        # Deduct bet amount from user balance
        user.balance -= bet_amount
        
        # Create game
        game = Game(
            player1_id=user_id,
            player2_id=None,  # AI opponent
            mode=GameMode.VS_AI,
            ai_difficulty=ai_difficulty,
            bet_amount=bet_amount,
            status=GameStatus.IN_PROGRESS,
            player1_rating_before=user.rating,
            current_turn=user_id
        )
        
        # Initialize game board
        engine = DraughtsEngine()
        game.board_state = engine.get_board_state()
        
        db.add(game)
        db.commit()
        db.refresh(game)
        
        return game
    
    @staticmethod
    def create_game_vs_player(
        db: Session, 
        player1_id: int, 
        player2_id: int, 
        bet_amount: float
    ) -> Optional[Game]:
        """Create a new game between two players."""
        player1 = db.query(User).filter(User.id == player1_id).first()
        player2 = db.query(User).filter(User.id == player2_id).first()
        
        if not player1 or not player2:
            return None
        
        # Check if both players have sufficient balance
        if player1.balance < bet_amount or player2.balance < bet_amount:
            return None
        
        # Deduct bet amounts
        player1.balance -= bet_amount
        player2.balance -= bet_amount
        
        # Create game
        game = Game(
            player1_id=player1_id,
            player2_id=player2_id,
            mode=GameMode.VS_PLAYER,
            bet_amount=bet_amount,
            status=GameStatus.IN_PROGRESS,
            player1_rating_before=player1.rating,
            player2_rating_before=player2.rating,
            current_turn=player1_id
        )
        
        # Initialize game board
        engine = DraughtsEngine()
        game.board_state = engine.get_board_state()
        
        db.add(game)
        db.commit()
        db.refresh(game)
        
        return game
    
    @staticmethod
    def make_move(
        db: Session, 
        game_id: int, 
        user_id: int, 
        from_pos: Tuple[int, int], 
        to_pos: Tuple[int, int]
    ) -> Tuple[bool, Optional[str], Optional[dict]]:
        """
        Make a move in a game.
        Returns (success, error_message, updated_board_state)
        """
        game = db.query(Game).filter(Game.id == game_id).first()
        
        if not game:
            return False, "Game not found", None
        
        if game.status != GameStatus.IN_PROGRESS:
            return False, "Game is not in progress", None
        
        if game.current_turn != user_id:
            return False, "Not your turn", None
        
        # Load game engine
        engine = DraughtsEngine()
        engine.set_board_state(game.board_state)
        
        # Make the move
        if not engine.make_move(from_pos, to_pos):
            return False, "Invalid move", None
        
        # Update game state
        game.board_state = engine.get_board_state()
        game.move_history = engine.move_history
        
        # Check if game is over
        is_over, winner = engine.is_game_over()
        
        if is_over:
            GameService.end_game(db, game, winner)
        else:
            # Update current turn
            if game.mode == GameMode.VS_AI:
                # AI makes a move
                ai = DraughtsAI(game.ai_difficulty)
                ai.make_move(engine)
                game.board_state = engine.get_board_state()
                game.move_history = engine.move_history
                
                # Check again if game is over after AI move
                is_over, winner = engine.is_game_over()
                if is_over:
                    GameService.end_game(db, game, winner)
                else:
                    game.current_turn = user_id
            else:
                # Switch to other player
                game.current_turn = game.player2_id if game.current_turn == game.player1_id else game.player1_id
        
        db.commit()
        db.refresh(game)
        
        return True, None, game.board_state
    
    @staticmethod
    def end_game(db: Session, game: Game, winner: Optional[int]):
        """End a game and distribute winnings."""
        game.status = GameStatus.COMPLETED
        
        if winner is None:
            # Draw - return bets to players
            game.is_draw = True
            player1 = db.query(User).filter(User.id == game.player1_id).first()
            player1.balance += game.bet_amount
            
            if game.player2_id:
                player2 = db.query(User).filter(User.id == game.player2_id).first()
                player2.balance += game.bet_amount
            
        else:
            # Someone won
            game.winner_id = game.player1_id if winner == 1 else game.player2_id
            
            total_pot = game.bet_amount * 2 if game.mode == GameMode.VS_PLAYER else game.bet_amount
            commission = GameService.calculate_commission(total_pot)
            winnings = total_pot - commission
            
            game.commission_amount = commission
            
            # Update winner's balance
            winner_user = db.query(User).filter(User.id == game.winner_id).first()
            winner_user.balance += winnings
            winner_user.games_won += 1
            
            # Create transaction for winner
            Transaction(
                user_id=game.winner_id,
                type=TransactionType.GAME_WIN,
                amount=winnings,
                balance_before=winner_user.balance - winnings,
                balance_after=winner_user.balance,
                game_id=game.id,
                payment_reference=f"GAME_WIN_{game.id}_{uuid.uuid4().hex[:8]}",
                payment_status="completed",
                description=f"Won game #{game.id}"
            )
            
            # Update loser stats
            if game.mode == GameMode.VS_PLAYER:
                loser_id = game.player2_id if game.winner_id == game.player1_id else game.player1_id
                loser_user = db.query(User).filter(User.id == loser_id).first()
                loser_user.games_lost += 1
                
                # Update ELO ratings
                winner_new_rating, loser_new_rating = GameService.calculate_elo_change(
                    winner_user.rating, loser_user.rating
                )
                
                game.player1_rating_after = winner_new_rating if game.winner_id == game.player1_id else loser_new_rating
                game.player2_rating_after = loser_new_rating if game.winner_id == game.player1_id else winner_new_rating
                
                winner_user.rating = winner_new_rating
                loser_user.rating = loser_new_rating
            else:
                # AI opponent
                player1 = db.query(User).filter(User.id == game.player1_id).first()
                if game.winner_id == game.player1_id:
                    player1.games_won += 1
                else:
                    player1.games_lost += 1
        
        # Update total games
        player1 = db.query(User).filter(User.id == game.player1_id).first()
        player1.total_games += 1
        
        if game.player2_id:
            player2 = db.query(User).filter(User.id == game.player2_id).first()
            player2.total_games += 1
        
        db.commit()
