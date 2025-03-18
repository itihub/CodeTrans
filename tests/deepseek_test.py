from dotenv import load_dotenv
from openai import OpenAI
import os
import logging

load_dotenv("../deepseek.env")
api_key= os.environ.get("OPENAI_API_KEY")
api_url = "https://api.deepseek.com/v1"

# 检查 API Key 是否存在
if not api_key:
    raise ValueError("未找到 OPENAI_API_KEY，请检查 .env 文件是否正确配置。")

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 用户输入和目标语言
user_context = 'print("Hello, World!")'
code_language = "java"

# 系统提示内容
system_content = (
    f"你是一个代码转化助手，你只会检查代码语法是否正确，当代码语法错误时提出修改意见和将代码转为另一种语言的代码。"
    f"你会根据下面提供的用户的输入来识别代码语言的类型并检查代码语法是否正确，如果代码语法错误请直接说出代码的错误位置和修复建议，"
    f"如果代码格式正确则输出转换为 {code_language} 语言的代码。"
)
# system_content = f"你是一个代码转化助手，你只会检查代码语法是否正确，当代码语法错误时提出修改意见和将代码转为另一种语言的代码。你会根据下面提供的用户的输入来识别代码语言的类型并检查代码语法是否正确，如果代码语法错误请直接说出代码的错误位置和修复建议，如果代码格式正确则输出转换为{code_language}语言的代码。"

logger.info(user_context)
logger.info(system_content)

# 初始化 OpenAI 客户端
client = OpenAI(
    api_key=api_key, 
    base_url=api_url,
)

try:
    # 调用 API
    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "system", "content": system_content},
            {"role": "user", "content": user_context},
        ],
        temperature=0,
        stream=False
    )
    # 输出结果
    # print(response)
    print(response.choices[0].message.content)
except Exception as e:
    # 捕获异常并记录日志
    logger.error(f"调用 OpenAI API 时发生错误：{e}")
