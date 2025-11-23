from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey, Enum, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base
import enum


class UserRole(str, enum.Enum):
    PLAYER = "player"
    ADMIN = "admin"


class GameStatus(str, enum.Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class TransactionType(str, enum.Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    GAME_WIN = "game_win"
    GAME_LOSS = "game_loss"
    COMMISSION = "commission"


class GameMode(str, enum.Enum):
    VS_AI = "vs_ai"
    VS_PLAYER = "vs_player"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    phone_number = Column(String)
    
    # Gaming stats
    rating = Column(Integer, default=1000)
    total_games = Column(Integer, default=0)
    games_won = Column(Integer, default=0)
    games_lost = Column(Integer, default=0)
    games_drawn = Column(Integer, default=0)
    
    # Financial
    balance = Column(Float, default=0.0)
    total_deposited = Column(Float, default=0.0)
    total_withdrawn = Column(Float, default=0.0)
    
    # Account
    role = Column(Enum(UserRole), default=UserRole.PLAYER)
    is_active = Column(Boolean, default=True)
    is_online = Column(Boolean, default=False)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    last_login = Column(DateTime(timezone=True))
    
    # Relationships
    games_as_player1 = relationship("Game", foreign_keys="Game.player1_id", back_populates="player1")
    games_as_player2 = relationship("Game", foreign_keys="Game.player2_id", back_populates="player2")
    transactions = relationship("Transaction", back_populates="user")


class Game(Base):
    __tablename__ = "games"
    
    id = Column(Integer, primary_key=True, index=True)
    
    # Players
    player1_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    player2_id = Column(Integer, ForeignKey("users.id"), nullable=True)  # Null for AI games
    
    # Game details
    mode = Column(Enum(GameMode), nullable=False)
    ai_difficulty = Column(String, nullable=True)  # For AI games
    bet_amount = Column(Float, nullable=False)
    commission_amount = Column(Float, default=0.0)
    
    # Game state
    status = Column(Enum(GameStatus), default=GameStatus.WAITING)
    board_state = Column(JSON)  # Store current board position
    move_history = Column(JSON, default=[])
    current_turn = Column(Integer)  # Player ID whose turn it is
    
    # Time control (chess clock)
    time_control = Column(Integer, default=600)  # Total time in seconds (default 10 min)
    time_increment = Column(Integer, default=5)  # Increment per move in seconds
    player1_time_left = Column(Integer)  # Remaining time for player1 in seconds
    player2_time_left = Column(Integer)  # Remaining time for player2 in seconds
    last_move_time = Column(DateTime(timezone=True))  # When last move was made
    
    # Results
    winner_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    is_draw = Column(Boolean, default=False)
    
    # Ratings (snapshot at game start)
    player1_rating_before = Column(Integer)
    player2_rating_before = Column(Integer)
    player1_rating_after = Column(Integer)
    player2_rating_after = Column(Integer)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    
    # Relationships
    player1 = relationship("User", foreign_keys=[player1_id], back_populates="games_as_player1")
    player2 = relationship("User", foreign_keys=[player2_id], back_populates="games_as_player2")


class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Transaction details
    type = Column(Enum(TransactionType), nullable=False)
    amount = Column(Float, nullable=False)
    balance_before = Column(Float)
    balance_after = Column(Float)
    
    # Payment gateway details
    payment_reference = Column(String, unique=True, index=True)
    payment_method = Column(String)
    payment_status = Column(String, default="pending")
    
    # Game reference (if applicable)
    game_id = Column(Integer, ForeignKey("games.id"), nullable=True)
    
    # Metadata
    description = Column(String)
    transaction_metadata = Column(JSON)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="transactions")


class Challenge(Base):
    __tablename__ = "challenges"
    
    id = Column(Integer, primary_key=True, index=True)
    challenger_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    opponent_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    
    bet_amount = Column(Float, nullable=False)
    counter_offer_amount = Column(Float, nullable=True)
    
    status = Column(String, default="open")  # open, accepted, rejected, expired
    message = Column(String)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    expires_at = Column(DateTime(timezone=True))
    responded_at = Column(DateTime(timezone=True))
