from fastapi import FastAPI, HTTPException, Request, Response, Cookie, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import sessionmaker, Session
from database import Base, engine, SessionLocal  # 引入抽离的数据库模块
import uuid
import os
import logging
from deepseek_utils import run_deepseek

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 初始化 FastAPI 应用
app = FastAPI()

origins = [
    "http://localhost:8001",
]

# 添加 CORS 中间件
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # 允许所有来源（生产环境中建议指定具体的域名）
    allow_credentials=True,  # 允许发送 Cookie
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有请求头
)

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")


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
    # created_at = Column(DateTime, server_default=func.now(), nullable=False)
    # # 修改时间
    # updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False)
    

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 请求体模型
class CodeConversionRequest(BaseModel):
    code: str
    language: str

# 响应体模型
class CodeConversionResponse(BaseModel):
    data: str

# 中间件或路由处理
@app.middleware("http")
async def add_session_id(request: Request, call_next):
    # 检查是否有 session_id
    session_id = request.cookies.get("session_id")
    if not session_id:
        # 如果没有 session_id，则生成一个新的 UUID
        session_id = str(uuid.uuid4())
      
    # 调用后续处理
    response = await call_next(request)

    # 在最终响应时设置 session_id 到 Cookie 中
    if not request.cookies.get("session_id"):
        # response.set_cookie(key="session_id", value=session_id, httponly=True, max_age=3600)
        response.set_cookie(key="session_id", value=session_id, httponly=True)

    return response


# 托管 index.html
@app.get("/", response_class=HTMLResponse)
async def index():
    # file_path = os.path.join(os.path.dirname(__file__), "static", "index.html")
    # print(f"Serving file from: {file_path}")  # 打印文件路径
    # with open(file_path, "r", encoding="utf-8") as file:
    #     html_content = file.read()
    # return HTMLResponse(content=html_content)
    return HTMLResponse(content=open(file="static/index.html", encoding="utf-8").read())
    # return "index.html"

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# 接口实现
@app.post("/api/convert", response_model=CodeConversionResponse)
async def convert_code(request: CodeConversionRequest, db: Session = Depends(get_db), session_id: str = Cookie(None)):
    # 验证输入
    if not request.code.strip():
        raise HTTPException(status_code=400, detail="输入代码不能为空！")
    if request.language not in ["python", "javascript", "java", "csharp", "cpp"]:
        raise HTTPException(status_code=400, detail="不支持的目标语言！")

    try:
        # 使用 DeepSeek 进行代码转换
        converted_code = run_deepseek(request.code, request.language)

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
        return CodeConversionResponse(data=converted_code)
    except Exception as e:
        logger.error(e)
        raise HTTPException(status_code=500, detail=f"代码转换失败：{str(e)}")

# Pydantic 模型
class CodeConversionDTO(BaseModel):
    id: int
    input_code: str
    target_language: str
    output_code: str

    model_config = {'from_attributes': True}

@app.get("/api/records", response_model=list[CodeConversionDTO])
async def get_records(db: Session = Depends(get_db)):
    # 查询所有数据
    data = db.query(CodeConversion).all()
    return [CodeConversionDTO.model_validate(item) for item in data]

print(app.routes)