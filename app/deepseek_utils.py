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

def run_deepseek(input_code: str, target_language: str) -> str:
    """
    使用 DeepSeek 将代码转换为目标语言。

    参数:
        input_code (str): 输入的代码。
        target_language (str): 目标语言。

    返回:
        str: 转换后的代码。
    """

    # 系统提示内容
    system_content = f"""
    你是一位严格的代码审查与转换专家。你的任务是：

    1. **精确识别代码语言：** 准确判断用户输入的代码所使用的编程语言。
        * **若无法识别：** 请回复“**无法识别输入的代码语言。**”并结束。
    2. **执行极其严格的代码语法检查：** 对输入的代码进行**逐字逐句的细致分析**，包括但不限于：
    * **括号匹配：** 确保所有括号（圆括号、方括号、花括号）都正确匹配。
    * **引号匹配：** 确保所有引号（单引号、双引号）都正确匹配。
    * **语法规则：** 严格按照该语言的语法规则进行检查，包括关键字、变量声明、语句结构等。
    * **符号使用：** 检查所有符号（分号、逗号、冒号等）的使用是否正确。
    3. **错误处理：**
    * **若发现任何语法错误：** 立即指出错误的**具体位置（行号、字符位置）**，并给出**明确且详细**的修复建议，并回复“**代码存在语法错误，已停止转换。**”并结束。
    * **若代码完全正确：** 立即将代码转换为 {target_language} 语言，并仅输出转换后的代码，**禁止输出任何解释性或说明性文字。**

    请严格遵守以下规则：

    仅输出代码：在代码格式正确的情况下，只输出转换后的代码，不包含任何其他文字。
    严格审查：对代码的每一个细节进行严格审查，确保转换后的代码完全符合目标语言的规范。
    准确转换：确保转换后的代码在逻辑上与原始代码完全等价。
    """

    # 初始化 OpenAI 客户端
    client = OpenAI(
        api_key=api_key, 
        base_url=api_url,
    )

    try:
         # 调用 API
        response = client.chat.completions.create(
            model="deepseek-reasoner",
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