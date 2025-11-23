from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum


# User Schemas
class UserBase(BaseModel):
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    phone_number: Optional[str] = None


class UserCreate(UserBase):
    password: str = Field(..., min_length=6)


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(UserBase):
    id: int
    rating: int
    total_games: int
    games_won: int
    games_lost: int
    games_drawn: int
    balance: float
    is_online: bool
    created_at: datetime
    
    class Config:
        from_attributes = True


class UserStats(BaseModel):
    username: str
    rating: int
    total_games: int
    games_won: int
    games_lost: int
    games_drawn: int
    win_rate: float
    
    class Config:
        from_attributes = True


# Game Schemas
class GameModeEnum(str, Enum):
    VS_AI = "vs_ai"
    VS_PLAYER = "vs_player"


class GameStatusEnum(str, Enum):
    WAITING = "waiting"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"


class GameCreate(BaseModel):
    mode: GameModeEnum
    bet_amount: float = Field(..., gt=0)
    ai_difficulty: Optional[str] = None


class GameMove(BaseModel):
    game_id: int
    from_position: tuple[int, int]
    to_position: tuple[int, int]


class GameResponse(BaseModel):
    id: int
    mode: GameModeEnum
    bet_amount: float
    status: GameStatusEnum
    player1_id: int
    player2_id: Optional[int]
    current_turn: Optional[int]
    board_state: Optional[dict]
    created_at: datetime
    
    class Config:
        from_attributes = True


# Transaction Schemas
class TransactionTypeEnum(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAWAL = "withdrawal"
    GAME_WIN = "game_win"
    GAME_LOSS = "game_loss"
    COMMISSION = "commission"


class DepositRequest(BaseModel):
    amount: float = Field(..., gt=0)
    payment_method: str = "paychangu"


class WithdrawalRequest(BaseModel):
    amount: float = Field(..., gt=0)
    withdrawal_method: str


class TransactionResponse(BaseModel):
    id: int
    type: TransactionTypeEnum
    amount: float
    balance_before: float
    balance_after: float
    payment_status: str
    created_at: datetime
    description: Optional[str]
    transaction_metadata: Optional[dict] = None
    
    class Config:
        from_attributes = True


# Challenge Schemas
class ChallengeCreate(BaseModel):
    bet_amount: float = Field(..., gt=0)
    message: Optional[str] = None


class ChallengeResponse(BaseModel):
    id: int
    challenger_id: int
    challenger_username: Optional[str]
    bet_amount: float
    counter_offer_amount: Optional[float]
    status: str
    message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True


class ChallengeAccept(BaseModel):
    challenge_id: int
    counter_offer: Optional[float] = None


# Token Schema
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse


# Payment Callback
class PaymentCallback(BaseModel):
    transaction_id: str
    status: str
    amount: float
    reference: str
    transaction_metadata: Optional[dict] = None
