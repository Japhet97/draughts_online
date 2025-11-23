from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User, Game, GameStatus, GameMode
from app.schemas.schemas import GameCreate, GameResponse, GameMove
from app.api.endpoints.auth import get_current_user
from app.services.game_service import GameService
from typing import List

router = APIRouter()


@router.post("/create", response_model=GameResponse)
def create_game(
    game_data: GameCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new game (vs AI or waiting for player)."""
    # Validate bet amount
    from app.core.config import settings
    if game_data.bet_amount < settings.MIN_BET_AMOUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Minimum bet amount is {settings.MIN_BET_AMOUNT}"
        )
    
    if game_data.bet_amount > settings.MAX_BET_AMOUNT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum bet amount is {settings.MAX_BET_AMOUNT}"
        )
    
    if current_user.balance < game_data.bet_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )
    
    # Create game based on mode
    if game_data.mode == GameMode.VS_AI:
        if not game_data.ai_difficulty:
            game_data.ai_difficulty = "expert"
        
        game = GameService.create_game_vs_ai(
            db, 
            current_user.id, 
            game_data.bet_amount,
            game_data.ai_difficulty
        )
    else:
        # Create a waiting game for player vs player
        game = Game(
            player1_id=current_user.id,
            mode=GameMode.VS_PLAYER,
            bet_amount=game_data.bet_amount,
            status=GameStatus.WAITING,
            player1_rating_before=current_user.rating
        )
        current_user.balance -= game_data.bet_amount
        db.add(game)
        db.commit()
        db.refresh(game)
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create game"
        )
    
    return game


@router.post("/move")
def make_move(
    move_data: GameMove,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Make a move in a game."""
    success, error, board_state = GameService.make_move(
        db,
        move_data.game_id,
        current_user.id,
        move_data.from_position,
        move_data.to_position
    )
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error
        )
    
    return {
        "success": True,
        "board_state": board_state,
        "message": "Move made successfully"
    }


@router.get("/active", response_model=List[GameResponse])
def get_active_games(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's active games."""
    games = db.query(Game).filter(
        ((Game.player1_id == current_user.id) | (Game.player2_id == current_user.id)),
        Game.status == GameStatus.IN_PROGRESS
    ).all()
    
    return games


@router.get("/history", response_model=List[GameResponse])
def get_game_history(
    limit: int = 50,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get user's game history."""
    games = db.query(Game).filter(
        ((Game.player1_id == current_user.id) | (Game.player2_id == current_user.id)),
        Game.status == GameStatus.COMPLETED
    ).order_by(Game.completed_at.desc()).limit(limit).all()
    
    return games


@router.get("/waiting", response_model=List[GameResponse])
def get_waiting_games(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get games waiting for an opponent."""
    games = db.query(Game).filter(
        Game.status == GameStatus.WAITING,
        Game.player1_id != current_user.id
    ).all()
    
    return games


@router.get("/{game_id}", response_model=GameResponse)
def get_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get specific game details."""
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    # Check if user is part of this game
    if game.player1_id != current_user.id and game.player2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not part of this game"
        )
    
    return game


@router.post("/{game_id}/join")
def join_game(
    game_id: int,
    counter_offer: float = None,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Join a waiting game."""
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    if game.status != GameStatus.WAITING:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is not waiting for players"
        )
    
    if game.player1_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot join your own game"
        )
    
    # Use counter offer or original bet
    bet_amount = counter_offer if counter_offer else game.bet_amount
    
    if current_user.balance < bet_amount:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Insufficient balance"
        )
    
    # Join the game
    game.player2_id = current_user.id
    game.player2_rating_before = current_user.rating
    game.status = GameStatus.IN_PROGRESS
    game.current_turn = game.player1_id
    
    # Initialize board
    from app.games.draughts_engine import DraughtsEngine
    engine = DraughtsEngine()
    game.board_state = engine.get_board_state()
    
    # Deduct bet from player 2
    current_user.balance -= bet_amount
    
    db.commit()
    db.refresh(game)
    
    return {"message": "Successfully joined game", "game": game}


@router.post("/{game_id}/forfeit")
def forfeit_game(
    game_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Forfeit a game."""
    game = db.query(Game).filter(Game.id == game_id).first()
    
    if not game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Game not found"
        )
    
    if game.player1_id != current_user.id and game.player2_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not part of this game"
        )
    
    if game.status != GameStatus.IN_PROGRESS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Game is not in progress"
        )
    
    # Determine winner (opponent)
    winner = 2 if current_user.id == game.player1_id else 1
    GameService.end_game(db, game, winner)
    
    return {"message": "Game forfeited"}
