from dotenv import load_dotenv
from openai import OpenAI
from jinja2 import Environment, FileSystemLoader
import os
import logging

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 获取环境文件路径，优先从 ENV_FILE_PATH 环境变量中读取
env_file_path = os.getenv("ENV_FILE_PATH", "../deepseek.env")

load_dotenv(env_file_path)
api_key = os.getenv("OPENAI_API_KEY")
api_url = os.getenv("OPENAI_API_URL")
model = os.getenv("MODEL")

# 检查 API Key 是否存在
if not api_key:
    raise ValueError("未找到 OPENAI_API_KEY，请检查 .env 文件是否正确配置。")


# 配置 Jinja2 模板加载器
template_loader = FileSystemLoader(searchpath="../templates")
template_env = Environment(loader=template_loader)


def run_deepseek(input_code: str, target_language: str) -> str:
    """
    使用 DeepSeek 将代码转换为目标语言。

    参数:
        input_code (str): 输入的代码。
        target_language (str): 目标语言。

    返回:
        str: 转换后的代码。
    """

    # 加载并渲染系统提示模板
    template = template_env.get_template("system_prompt.jinja2")
    system_content = template.render(target_language=target_language)

    # 初始化 OpenAI 客户端
    client = OpenAI(
        api_key=api_key, 
        base_url=api_url,
    )

    try:
         # 调用 API
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_content},
                {"role": "user", "content": input_code},
            ],
            temperature=0,
            stream=False
        )
        return response.choices[0].message.content
    except Exception as e:
        # 捕获异常并抛出
        raise RuntimeError(f"DeepSeek 转换失败: {e}")