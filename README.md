## CodeTrans

### 概述
CodeTrans 是一个基于 FastAPI 的代码转换工具，旨在通过集成大语言模型（如 OpenAI、DeepSeek）实现代码的跨语言转换。用户可以输入代码并选择目标语言，系统会自动完成代码的转换并返回结果。


### 功能描述
1. **智能代码转换**  
   - 支持多种编程语言之间的代码转换，包括 Python、JavaScript、Java、C#、C++ 等。

2. **智能语法校验**  
   在转换前对输入代码进行严格的语法检查，确保代码格式准确无误。

3. **转换记录管理**  
   将用户的代码转换记录存储到数据库中，支持查询历史记录。

4. **用户管理**  
   - **即刻体验，无需登录**：无需繁琐注册，立即享受完整功能。
   - **个性化记录，安全无忧**：通过安全Cookie技术，为您专属记录每一次操作，保障数据独立性。
   - **灵活查询，记录可追溯**：随时查询您的操作记录，记录有效期可自定义（默认7天）。

5. **Web 界面**  
   提供简洁直观的 Web 界面，用户可以通过浏览器直接使用代码转换功能。

6. **API 支持**  
   提供 RESTful API，方便开发者集成到现有系统和工作流程中。

### 开发指南

#### 环境初始化
项目支持两种依赖管理方式：Pipenv 和 requirements.txt。根据你的需求选择一种方式进行环境初始化

##### 使用 Pipenv
1. 确保已安装 Pipenv：
```pip install pipenv```
2. 激活虚拟环境：
```pipenv shell```
3. 安装依赖：
```pipenv install```

##### 使用 requirements.txt
1. 创建虚拟环境（可选）：
```python -m venv venv```
2. 激活虚拟环境：
    + Windows:
    ```.\venv\Scripts\activate```
    + Linux/macOS:
    ```source venv/bin/activate```
3. 安装依赖：
```pip install -r requirements.txt```

#### 配置大模型密钥
在项目根目录下创建 `deepseek.env` 文件，并配置 OpenAI API 的密钥和相关信息。例如：
```env
OPENAI_API_URL=https://api.deepseek.com/v1
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx8888
MODEL=deepseek-reasoner
```

#### 数据库初始化
项目默认使用 SQLite 数据库。若需使用其他数据库（如 MySQL），请修改 `app/database.py` 中的 `DATABASE_URL` 配置，并执行以下命令初始化数据库表：
```bash
python -m app.database
```

#### 本地运行
1. 激活虚拟环境（如果尚未激活）。
2. 进入 `app` 目录，运行以下命令启动项目：
```bash
uvicorn main:app --reload
```
启动后，访问 `http://127.0.0.1:8000` 即可使用 Web 界面。

#### API 文档
项目启动后，可通过以下地址访问自动生成的 API 文档：
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

#### 使用 Docker 和 Docker Compose 部署
项目支持通过 Docker 和 Docker Compose 部署，以下是详细步骤。
##### 使用 Docker
1. 构建 Docker 镜像：
   ```bash
   docker build -t codetrans .
   ```
2. 运行容器：
   ```bash
   docker run -d -p 8000:8000 --name codetrans codetrans
   ```
##### 使用 Docker Compose
1. 构建 Docker 镜像
    在项目根目录运行以下命令：
    ```bash
    docker-compose build
    ```
2. 启动服务
    ```bash
    docker-compose up
    ```
3. 停止服务
    ```bash
    docker-compose down
    ```

### 文件结构
```
.
├── app/                     # 主应用代码
│   ├── __init__.py          # 应用初始化
│   ├── database.py          # 数据库配置
│   ├── deepseek_utils.py    # DeepSeek 工具函数
│   ├── main.py              # FastAPI 主入口
│   ├── static/              # 静态文件
│   └── templates/           # Jinja2 模板
├── scripts/                 # 数据库脚本
│   └── schema.sql           # 数据库表结构
├── tests/                   # 测试代码
│   └── deepseek_test.py     # DeepSeek 测试
├── Dockerfile               # Docker 配置
├── Pipfile                  # Pipenv 配置
├── Pipfile.lock             # Pipenv 锁定文件
├── README.md                # 项目说明
└── requirements.txt         # 依赖列表
```

### 贡献指南
欢迎贡献代码！请遵循以下步骤：
1. Fork 本仓库。
2. 创建新分支：`git checkout -b feature/your-feature-name`。
3. 提交代码：`git commit -m "Add your feature"`。
4. 推送到远程分支：`git push origin feature/your-feature-name`。
5. 提交 Pull Request。

### 联系方式
如有任何问题或建议，请通过 [issues](https://github.com/itihub/CodeTrans/issues) 提交。
