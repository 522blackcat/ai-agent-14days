# Day 06 Python 面试题



课程主题：Memory、MCP 与多 Agent



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
