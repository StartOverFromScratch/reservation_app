# init_db.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base  # ← Reservation, Equipment, Category などのモデル定義を含むファイルをインポート

DATABASE_URL = "sqlite:///./database.db"

# SQLAlchemyエンジン作成
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# セッション作成用
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """SQLAlchemyモデル定義に基づいてDBを初期化"""
    Base.metadata.create_all(bind=engine)
    print("✅ Database tables created successfully (via SQLAlchemy).")

if __name__ == "__main__":
    init_db()