# Day 03：Python 与 AI Agent 高级面试



建议先独立回答，再查看参考答案与追问答案。



## Python 高级面试



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




## AI Agent 高级面试



## Agent 1：为什么复杂 Agent 需要状态机？

**参考答案：**状态机将任务状态、执行路径和恢复点显式化，便于测试、审计、中断恢复和故障定位；但会增加状态设计与迁移成本。

**面试官追问：**状态 Schema 变更后，旧 Checkpoint 如何兼容？

**追问参考答案：**为 Checkpoint 定义版本号，采用兼容性读取、状态迁移函数或按版本分支恢复。上线前使用真实旧状态做恢复测试；对于无法迁移的状态，明确失败与人工处理策略。


## Agent 2：异步函数中调用阻塞 SDK 会怎样？

**参考答案：**阻塞调用占用事件循环线程，使其他协程无法及时运行。应优先使用异步 SDK，或将确实阻塞的调用放入受控线程池。

**面试官追问：**如何限制线程池并发与排队长度？

**追问参考答案：**使用 Semaphore 限制进入线程池的任务数，配置有界队列和超时，避免无限堆积。线程池本身不能强制停止已经运行的任意同步函数，因此外部 SDK 也必须设置超时。




## 我的面试复盘



个人回答请记录在同目录的 `answers.md`，不要直接修改本文件，以免下次补全时被覆盖。
