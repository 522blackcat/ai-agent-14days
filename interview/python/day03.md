# Day 03 Python 面试题



课程主题：LangGraph、状态机与 asyncio



## Python 1：GIL 对线程有什么影响？

**参考答案：**在常见 CPython 构建中，GIL 限制同一解释器内多个线程同时执行Python 字节码，但 I/O 等待和释放 GIL 的扩展代码仍可受益于线程。CPU 密集型任务通常需要进程或适当的原生扩展。

**面试官追问：**asyncio、线程池和进程池分别适合哪些任务？

**追问参考答案：**asyncio 适合大量等待网络或磁盘的 I/O 任务；线程池适合需要兼容同步阻塞库的 I/O 工作；进程池适合纯 Python CPU 密集任务。还要考虑进程间序列化开销和外部服务的并发限制。


## Python 2：asyncio 的取消如何传播？

**参考答案：**取消任务通常通过 CancelledError 传播。协程应在 finally 中清理资源，不要无意吞掉取消异常；TaskGroup 可以管理结构化并发。

**面试官追问：**如何为多个并发工具设置统一超时？

**追问参考答案：**使用 asyncio.TaskGroup 管理任务，配合 asyncio.timeout 设置总超时，使用 Semaphore 限制并发。单个工具还应设置自己的网络超时；取消时在 finally 中释放资源。

**代码示例：**

```python
import asyncio

async def call_tool(name: str, semaphore: asyncio.Semaphore):
    async with semaphore:
        await asyncio.sleep(0.1)
        return name

async def main():
    semaphore = asyncio.Semaphore(3)

    async with asyncio.timeout(5):
        async with asyncio.TaskGroup() as group:
            tasks = [
                group.create_task(call_tool(str(i), semaphore))
                for i in range(10)
            ]

    return [task.result() for task in tasks]

print(asyncio.run(main()))
```
