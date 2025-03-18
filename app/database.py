from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# MySQL数据库配置
# DATABASE_URL = "mysql+pymysql://username:password@localhost:3306/codetrans"

# 数据库配置：使用 SQLite 内嵌数据库
DATABASE_URL = "sqlite:///./codetrans.db"


# 创建数据库引擎
engine = create_engine(DATABASE_URL)

# 创建数据库会话
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()