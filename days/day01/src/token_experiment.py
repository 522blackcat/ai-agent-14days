
"""Day 01：比较中文、英文和 JSON 的 Token 消耗。"""

import json

# 复用当前仓库的模型客户端，不重新创建另一套配置
from agent import create_client


def main():
    client, model = create_client()

    # 三种输入表达相同的任务：让模型计算 12 + 30
    samples = {
        "中文": "请计算 12 加 30，只回答数字。",
        "英文": "Calculate 12 plus 30. Reply with the number only.",
        "JSON": json.dumps(
            {
                "task": "calculate",
                "a": 12,
                "b": 30,
                "reply": "number_only",
            },
            ensure_ascii=False,
        ),
    }

    print(f"当前模型：{model}")
    print("-" * 75)
    print(
        f"{'格式':<8} {'输入Token':>12} "
        f"{'输出Token':>12} {'总Token':>12} {'模型回答'}"
    )
    print("-" * 75)

    for name, prompt in samples.items():
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "你是计算助手，只回答最终数字，不解释。",
                },
                {
                    "role": "user",
                    "content": prompt,
                },
            ],
            temperature=0,
        )

        # OpenAI 兼容接口返回的 Token 用量
        usage = response.usage

        input_tokens = usage.prompt_tokens if usage else None
        output_tokens = usage.completion_tokens if usage else None
        total_tokens = usage.total_tokens if usage else None

        answer = response.choices[0].message.content or ""

        print(
            f"{name:<8} {str(input_tokens):>12} "
            f"{str(output_tokens):>12} "
            f"{str(total_tokens):>12} {answer.strip()}"
        )


if __name__ == "__main__":
    main()
