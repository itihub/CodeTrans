# 使用官方 Python 3.9 镜像作为基础镜像
FROM python:3.9-slim

# 设置工作目录
WORKDIR /app

# 复制 requirements.txt 文件到容器中
COPY requirements.txt /app/

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码到容器中
COPY app /app/app
COPY scripts /app/scripts
COPY templates /app/templates

# 复制环境文件到容器中
COPY deepseek.env /app/

# 暴露应用运行的端口
EXPOSE 8000

# 设置环境变量
ENV ENV_FILE_PATH=/app/deepseek.env

# 启动命令
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]