import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. 获取环境变量中的数据库 URL
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. 根据是否在云端 (是否有 DATABASE_URL) 来决定配置
if DATABASE_URL:
    # === 生产环境 (PostgreSQL) ===
    
    # Render 提供的 URL 通常以 postgres:// 开头，但 SQLAlchemy 需要 postgresql://
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)
    
    # ⚠️ 关键修复：PostgreSQL 连接绝对不能有 check_same_thread 参数
    engine = create_engine(DATABASE_URL)

else:
    # === 本地开发 (SQLite) ===
    SQLALCHEMY_DATABASE_URL = "sqlite:///./lovemenu.db"
    
    # SQLite 必须要有 check_same_thread 参数
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )

# 3. 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. 声明基类
Base = declarative_base()

# 5. 依赖注入函数
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 6. 初始化数据库函数
def init_db():
    # 在这里导入模型，确保它们被注册到 Base.metadata
    from . import models
    Base.metadata.create_all(bind=engine)