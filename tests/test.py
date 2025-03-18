from openai import OpenAI
import requests
import json

api_key = "sk-0acc8ce112d24300965793a97c79e114"
api_url = "https://api.deepseek.com"  # 请替换为实际的 API 端点

f_string_template = """
给我讲一个关于{name}的{what}故事。
"""

client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
response = client.chat.completions.create(
    model="deepseek-chat",
    messages=[
        {"role": "system", "content": "你是一个代码转化助手，你从不说自己是一个大模型或AI助手。你会根据下面提供的上下文内容来识别代码语言的类型并检查代码语法是否正确，如果代码语法错误请直接说出代码的错误位置和修复建议，如果代码格式正确请按目标语言进行转换。\n上下文内容\b{context}\n目标语言\b{code_language}\n"},
        {"role": "user", "content": "{input}"},
    ],
    stream=False
)

print(response.choices[0].message.content)




# headers = {
#     "Authorization": f"Bearer {api_key}",
#     "Content-Type": "application/json",
# }

# data = {
#     "prompt": "请给我讲一个笑话。",
#     # 其他可能的参数，例如模型名称、温度等
# }

# try:
#     response = requests.post(api_url, headers=headers, data=json.dumps(data))
#     response.raise_for_status()  # 检查请求是否成功

#     result = response.json()
#     print(result["choices"][0]["text"])  # 输出模型生成的文本

# except requests.exceptions.RequestException as e:
#     print(f"请求错误：{e}")
# except (KeyError, IndexError) as e:
#   print(f"解析错误：{e}, response: {response.text}")