"""
Day 01：真实模型 Function Calling 示例。

运行：
    python days/day01/src/agent.py

环境变量：
    MODEL_PROVIDER=cloud 或 ollama

云端：
    OPENAI_API_KEY=...
    OPENAI_MODEL=...

Ollama：
    OLLAMA_BASE_URL=http://localhost:11434/v1
    OLLAMA_MODEL=支持工具调用的模型名称
"""

import json
import os
import httpx

from dotenv import load_dotenv
from openai import OpenAI, APIStatusError
from pydantic import BaseModel, ConfigDict, Field, ValidationError


load_dotenv()


class CalculatorArgs(BaseModel):
    """工具参数：拒绝未声明字段并限制数值范围。"""

    model_config = ConfigDict(extra="forbid")

    a: float = Field(ge=-1_000_000, le=1_000_000)
    b: float = Field(ge=-1_000_000, le=1_000_000)


def add_numbers(args: CalculatorArgs) -> dict:
    """真实执行的 Python 工具。"""

    return {"result": args.a + args.b}


TOOLS = {
    "add_numbers": {
        "schema": CalculatorArgs,
        "handler": add_numbers,
    }
}


TOOL_SCHEMAS = [
    {
        "type": "function",
        "function": {
            "name": "add_numbers",
            "description": "计算两个数字的和。",
            "parameters": CalculatorArgs.model_json_schema(),
        },
    }
]


def create_client():
    """根据环境变量创建真实模型客户端。"""

    provider = os.getenv("MODEL_PROVIDER", "cloud").lower()

    if provider == "ollama":
        client = OpenAI(
            api_key="ollama",
            base_url=os.getenv(
                "OLLAMA_BASE_URL",
                "http://localhost:11434/v1",
            ),
            timeout=30.0,
            max_retries=1,
            http_client=httpx.Client(
                trust_env=False,
                timeout=30.0,
            ),
        )
        model = os.getenv("OLLAMA_MODEL", "qwen3:8b")
        return client, model

    api_key = os.getenv("OPENAI_API_KEY")
    model = os.getenv("OPENAI_MODEL")

    if not api_key or not model:
        raise RuntimeError(
            "云端模式需要设置 OPENAI_API_KEY 和 OPENAI_MODEL。"
        )

    client = OpenAI(
        api_key=api_key,
        timeout=30.0,
        max_retries=1,
        http_client=httpx.Client(
            trust_env=False,
            timeout=30.0,
        ),
    )
    return client, model


def execute_tool(name: str, raw_arguments: str) -> dict:
    """工具执行边界：白名单 + JSON 解析 + 参数校验。"""

    registered = TOOLS.get(name)

    if registered is None:
        return {
            "ok": False,
            "error": "tool_not_allowed",
        }

    try:
        arguments = json.loads(raw_arguments)

        validated = registered["schema"].model_validate(
            arguments
        )

        result = registered["handler"](validated)

        return {
            "ok": True,
            "data": result,
        }

    except (json.JSONDecodeError, ValidationError) as exc:
        return {
            "ok": False,
            "error": "invalid_arguments",
            "detail": str(exc),
        }

    except Exception:
        # 不把内部堆栈和敏感信息直接返回模型。
        return {
            "ok": False,
            "error": "tool_execution_failed",
        }


def run_agent(question: str, max_rounds: int = 4) -> str:
    """限制模型与工具的最大交互轮次。"""

    client, model = create_client()
    print("实际模型：", model)
    print("实际接口：", client.base_url)
    print("当前工作目录：", os.getcwd())

    messages = [
        {
            "role": "system",
            "content": (
                "你是一个中文助手。需要计算时调用工具。"
                "不得编造工具执行结果。"
            ),
        },
        {
            "role": "user",
            "content": question,
        },
    ]

    for _ in range(max_rounds):

        response = client.chat.completions.create(
            model=model,
            messages=messages,
            tools=TOOL_SCHEMAS,
            tool_choice="auto",
        )

        message = response.choices[0].message

        messages.append(
            message.model_dump(exclude_none=True)
        )

        print(f"第{_}次模型运行： {message}")

        if not message.tool_calls:
            return message.content or "模型没有返回文本。"

        for tool_call in message.tool_calls:

            result = execute_tool(
                tool_call.function.name,
                tool_call.function.arguments,
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": json.dumps(
                        result,
                        ensure_ascii=False,
                    ),
                }
            )

    return "达到最大执行轮次，任务已终止。"


if __name__ == "__main__":

    try:
        print(run_agent("请计算 123.5 加 876.5 等于多少？", max_rounds=3))
    except APIStatusError as exc:
        print("HTTP 状态码：", exc.status_code)
        print("请求 ID：", exc.request_id)
        print("服务端响应：", exc.response.text)
        raise
