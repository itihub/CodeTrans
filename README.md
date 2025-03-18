## CodeTrans

### 环境初始化
项目使用Pipenv管理依赖
```
pipenv shell
pipenv install fastapi uvicorn sqlalchemy pymysql deepseek
pipenv install python-dotenv openai
```


### 大模型密钥配置
需要在项目根目录下创建deepseek.env文件，在该文件定义密钥。例如:```OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx8888```


### 项目运行
在app目录下执行
```uvicorn main:app --reload```
