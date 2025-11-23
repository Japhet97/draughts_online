import sys
print("Python path:", sys.executable)
print("Testing imports...")

try:
    print("1. Importing FastAPI...")
    from fastapi import FastAPI
    print("   ✓ FastAPI OK")
    
    print("2. Importing pydantic_settings...")
    from pydantic_settings import BaseSettings
    print("   ✓ pydantic_settings OK")
    
    print("3. Importing SQLAlchemy...")
    from sqlalchemy import create_engine
    print("   ✓ SQLAlchemy OK")
    
    print("4. Loading config...")
    from app.core.config import settings
    print("   ✓ Config loaded")
    print(f"   DATABASE_URL: {settings.DATABASE_URL}")
    print(f"   SECRET_KEY: {settings.SECRET_KEY[:10]}...")
    
    print("5. Loading database...")
    from app.db.database import engine, Base
    print("   ✓ Database OK")
    
    print("6. Creating tables...")
    Base.metadata.create_all(bind=engine)
    print("   ✓ Tables created")
    
    print("7. Loading main app...")
    from app.main import app
    print("   ✓ App loaded successfully!")
    
    print("\n✅ All imports successful! Starting server...")
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
    
except Exception as e:
    print(f"\n❌ ERROR: {type(e).__name__}")
    print(f"   {str(e)}")
    import traceback
    traceback.print_exc()
    input("\nPress Enter to exit...")
