from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.db.database import get_db
from app.models.models import User
from app.schemas.schemas import UserCreate, UserLogin, UserResponse, Token, UserStats
from app.core.security import verify_password, get_password_hash, create_access_token
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from datetime import datetime

router = APIRouter()
security = HTTPBearer()


def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user."""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if payload is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )
    
    user = db.query(User).filter(User.id == int(user_id)).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )
    
    return user


@router.post("/register", response_model=Token)
def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user."""
    # Check if username exists
    if db.query(User).filter(User.username == user_data.username).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Check if email exists
    if db.query(User).filter(User.email == user_data.email).first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create user
    user = User(
        username=user_data.username,
        email=user_data.email,
        full_name=user_data.full_name,
        phone_number=user_data.phone_number,
        hashed_password=get_password_hash(user_data.password)
    )
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.post("/login", response_model=Token)
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user."""
    user = db.query(User).filter(User.username == credentials.username).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is inactive"
        )
    
    # Update last login
    user.last_login = datetime.utcnow()
    user.is_online = True
    db.commit()
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user.id)})
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user": user
    }


@router.get("/me", response_model=UserResponse)
def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return current_user


@router.post("/logout")
def logout(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Logout user."""
    current_user.is_online = False
    db.commit()
    return {"message": "Successfully logged out"}


@router.get("/leaderboard", response_model=list[UserStats])
def get_leaderboard(
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """Get top players by rating."""
    users = db.query(User).filter(User.total_games >= 5).order_by(User.rating.desc()).limit(limit).all()
    
    leaderboard = []
    for user in users:
        win_rate = (user.games_won / user.total_games * 100) if user.total_games > 0 else 0
        leaderboard.append(UserStats(
            username=user.username,
            rating=user.rating,
            total_games=user.total_games,
            games_won=user.games_won,
            games_lost=user.games_lost,
            games_drawn=user.games_drawn,
            win_rate=round(win_rate, 2)
        ))
    
    return leaderboard


@router.get("/online-players", response_model=list[UserResponse])
def get_online_players(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get list of online players."""
    online_users = db.query(User).filter(
        User.is_online == True,
        User.id != current_user.id
    ).all()
    
    return online_users
