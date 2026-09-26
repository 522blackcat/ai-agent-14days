# Day 01 学习笔记

## 今天学到的三个核心知识点
### 1、llm调用

使用本地docker部署的ollama中的qwen3:1.7b模型进行配置，token是llm的最小词单元，对比于不同的语言格式，token的词数明显不同

格式       |    输入Token   |   输出Token   |    总Token | 模型回答 |
|---|---:|---:|---:|---|
中文       |         41   |       174    |      215  |  42 |
英文       |         42    |      170     |     212   | 42 |
JSON      |       54      |   519        |   573    | 360 |

可以使用OpenAi返回对象中的usage参数，其中
- usage.prompt_tokens是输入token
- usage.completion_tokens 是输出token
- usage.total_tokens 是总token
### function calling
模型自己决定要使用什么工具，我只负责生成TOOL_SCHEMAS，将工具白名单传输给llm选择，llm执行时判断需不需要执行工具，在tool_calls中，如果不需要，
则返回内容即content，如果需要，则调用工具，将工具执行完成的结添加到message中，继续下一次的llm调用
## 真实运行结果
```text
实际模型： qwen3:1.7b
实际接口： http://localhost:11434/v1/
当前工作目录： D:\product\ai-agent-14days\days\day01\src
第0次模型运行： ChatCompletionMessage(content='', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=[ChatCompletionMessageFunctionToolCall(id='call_5iko68gk', function=Function(arguments='{"a":123.5,"b":876.5}', name='add_numbers'), type='function', index=0)], reasoning='好的，用户让我计算123.5加876.5等于多少。首先，我需要确认他们是否需要使用提供的工具来解决这个问题。根据提供的工具列表，有一个名为add_numbers的函数，用于计算两个数字的和。用户的问题是关于两个小数的加法，所以应该适用这个工具。\n\n接下来，我需要检查参数是否正确。用户提供的两个数字是123.5和876.5，都是有效的数值类型，符合函数的要求。函数的参数是一个对象，包含a和b两个属性，类型都是number。因此，直接调用这个函数应该没问题。\n\n然后，我需要确保按照规则调用工具。根据指示，可以调用一个或多个函数，这里只用一个函数即可。所以，生成一个工具调用的JSON对象，名称是add_numbers，参数是{"a": 123.5, "b": 876.5}。\n\n最后，确认没有编造工具的执行结果，严格按照函数的定义来执行。因此，正确的工具调用应该是正确的，结果应该是1000.0。不需要额外的操作，直接返回结果。\n')
第1次模型运行： ChatCompletionMessage(content='123.5 + 876.5 = 1000.0', refusal=None, role='assistant', annotations=None, audio=None, function_call=None, tool_calls=None, reasoning='好的，用户让我计算123.5加876.5的结果。首先，我需要确认他们是否需要使用提供的工具。根据工具列表，有一个add_numbers函数，专门用来计算两个数字的和。用户的问题很直接，两个数都是小数，应该没问题。\n\n接下来，我检查参数是否正确。用户提供的a是123.5，b是876.5，都是有效的数值类型，符合函数的要求。所以直接调用这个函数应该没问题。然后，我需要生成一个工具调用的JSON对象，名称是add_numbers，参数是{"a": 123.5, "b": 876.5}。\n\n调用后，工具返回的结果是1000.0。这说明计算正确。用户可能只需要这个结果，所以我要确保以清晰的方式呈现答案。可能需要简单地回复“1000.0”或者解释过程。但根据之前的示例，可能只需要给出结果。不过用户的问题是直接的计算，所以直接给出结果即可。\n')
123.5 + 876.5 = 1000.0
```
## 遇到的错误与解决过程
LLM模型访问502,我本地开启了vpn代理，llm模型中访问不到
解决方案：我在模型创建时添加http_client参数，增加trust_env=False
这个 HTTP 客户端不要自动读取系统环境中的代理等网络配置。
## 生产环境技术取舍

## 需要再次复习的内容
