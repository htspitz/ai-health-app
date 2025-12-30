from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import DeclarativeBase,Mapped,mapped_column,sessionmaker
from datetime import datetime, timedelta, timezone
import sqlite3

#1. 接続設定（SQLiteを使用）
SQLALCHEMY_DATABASE_URL = "sqlite:///./health_app.db"

# 日本のタイムゾーン (+9時間) を定義
JST = timezone(timedelta(hours=+9))

#2. エンジンとセッションの作成
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False},
    # echo=True
)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

#3. ベースクラスの作成(これを使ってテーブルを定義する)
class Base(DeclarativeBase):
    pass

#4. テーブル定義
class HealthRecord(Base):
    __tablename__ = "records"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_name: Mapped[str] = mapped_column(default="User")
    input_text: Mapped[str] = mapped_column()
    ai_summary: Mapped[str] = mapped_column()
    created_at: Mapped[datetime] = mapped_column(default=lambda: datetime.now(JST))

# 5.初期化関数
Base.metadata.create_all(bind=engine)

#6. 保存用ヘルパー関数（SessionLocalを使う）
def save_record(user_name: str, input_text: str, ai_summary: str):
    db = SessionLocal()
    try:
        new_record = HealthRecord(
            user_name=user_name,
            input_text=input_text,
            ai_summary=ai_summary
        )
        db.add(new_record)
        db.commit()
        db.refresh(new_record)
        return new_record
    finally:
        db.close()

#7. 履歴取得用ヘルパー関数
def get_chat_history(limit: int = 5):
    db = SessionLocal()
    try:
        return db.query(HealthRecord).order_by(HealthRecord.created_at.desc()).limit(limit).all()
    finally:
        db.close()