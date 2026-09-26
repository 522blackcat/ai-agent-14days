# Day 06：Python 与 AI Agent 高级面试



建议先独立回答，再查看参考答案与追问答案。



## Python 高级面试



## Python 1：HTTP 连接池为什么重要？

**参考答案：**连接池复用连接，减少重复建立连接的成本。需要设置连接数、空闲连接数、连接超时和读取超时，避免外部服务故障耗尽本地资源。

**面试官追问：**连接池满时应该等待、拒绝还是扩容？

**追问参考答案：**连接池满时首先执行有界等待，并设置获取连接的超时。持续过载时应限流或拒绝请求，而不是无限扩容。扩容需要同时考虑下游服务容量、文件描述符和成本。


## Python 2：同步 HTTP 与异步 HTTP 如何选择？

**参考答案：**同步客户端适合简单顺序调用；异步客户端适合大量 I/O 并发。异步并不自动提高单次请求速度，也不能解决远端服务限流。

**面试官追问：**如何为异步 HTTP 客户端设置并发信号量？

**追问参考答案：**使用 asyncio.Semaphore 包裹请求，并在共享的 httpx.AsyncClient 中配置连接池与超时。任务取消时应释放信号量；还需要针对远端 429 设置退避和限流策略。

**代码示例：**

```python
import asyncio
import httpx

async def fetch_all(urls: list[str]):
    semaphore = asyncio.Semaphore(5)

    timeout = httpx.Timeout(10.0)

    async with httpx.AsyncClient(timeout=timeout) as client:
        async def fetch(url: str):
            async with semaphore:
                response = await client.get(url)
                response.raise_for_status()
                return response.text

        return await asyncio.gather(
            *(fetch(url) for url in urls)
        )
```




## AI Agent 高级面试



## Agent 1：MCP 和 Function Calling 的关系是什么？

**参考答案：**Function Calling 是模型表达工具调用意图的机制；MCP 是模型应用与外部能力交互的协议。应用可以将 MCP 工具暴露给模型进行 Function Calling。

**面试官追问：**MCP Server 的工具如何做身份认证？

**追问参考答案：**根据传输方式和部署环境建立身份认证，在服务端对每个工具执行资源级授权，为高风险操作设置审批、速率限制和审计。不能只信任 MCP Client 提供的工具描述。


## Agent 2：什么时候不应该使用多 Agent？

**参考答案：**任务简单、职责难以划分或对延迟与成本要求严格时，单 Agent 或固定 Workflow 可能更合适。

**面试官追问：**如何评估多 Agent 相比单 Agent 是否真的改善效果？

**追问参考答案：**使用相同任务集比较成功率、质量、延迟、Token 成本、工具错误率和人工介入率。多 Agent 只有在收益足以覆盖协调成本时才值得采用。




## 我的面试复盘



个人回答请记录在同目录的 `answers.md`，不要直接修改本文件，以免下次补全时被覆盖。
