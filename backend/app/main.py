from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.database import engine, Base
from app.api.endpoints import auth, games, payments

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Online Draughts Gaming Platform with Real Money Betting"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=r"^http://localhost(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["Authentication"])
app.include_router(games.router, prefix="/api/v1/games", tags=["Games"])
app.include_router(payments.router, prefix="/api/v1/payments", tags=["Payments"])


@app.get("/")
def root():
    """Root endpoint."""
    return {
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "status": "online",
        "message": "Welcome to Draughts Online Gaming Platform!"
    }


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
