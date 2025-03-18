from fastapi import FastAPI, HTTPException, Request, Response, Cookie
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from database import Base, engine, SessionLocal  # 引入抽离的数据库模块
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import uuid
import deepseek  # 假设 deepseek 是一个代码转换工具库

# 初始化 FastAPI 应用
app = FastAPI()

# 数据库模型
class CodeConversion(Base):
    __tablename__ = "code_conversions"
    # 主键
    id = Column(Integer, primary_key=True, index=True)
    # 用户唯一标识
    user_id = Column(String(36), default=lambda: str(uuid.uuid4()), nullable=False)
    # 输入的代码
    input_code = Column(Text, nullable=False)
    # 目标语言
    target_language = Column(String(50), nullable=False)
    # 转换后的代码
    output_code = Column(Text, nullable=False)
    # 创建时间
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    # 修改时间
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 请求体模型
class CodeConversionRequest(BaseModel):
    code: str
    language: str

# 响应体模型
class CodeConversionResponse(BaseModel):
    converted_code: str

# 中间件或路由处理
@app.middleware("http")
async def add_session_id(request: Request, call_next):
    # 检查是否有 session_id
    session_id = request.cookies.get("session_id")
    if not session_id:
        # 如果没有 session_id，则生成一个新的 UUID
        session_id = str(uuid.uuid4())
        response = await call_next(request)
        response.set_cookie(key="session_id", value=session_id, httponly=True)
        return response
    # 如果已有 session_id，直接继续处理请求
    response = await call_next(request)
    return response

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 接口实现
@app.post("/api/convert", response_model=CodeConversionResponse)
async def convert_code(request: CodeConversionRequest, db: SessionLocal = next(get_db()), session_id: str = Cookie(None)):
    # 验证输入
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="输入代码不能为空！")
    if request.language not in ["python", "javascript", "java", "csharp", "cpp"]:
        raise HTTPException(status_code=400, detail="不支持的目标语言！")

    try:
        # 使用 DeepSeek 进行代码转换
        converted_code = deepseek.convert(request.code, request.language)

        # 将转换结果存储到数据库
        db_record = CodeConversion(
            user_id=session_id,
            input_code=request.code,
            target_language=request.language,
            output_code=converted_code
        )
        db.add(db_record)
        db.commit()

        # 返回转换结果
        return CodeConversionResponse(converted_code=converted_code)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"代码转换失败：{str(e)}")