# Day 02 Python 面试题



课程主题：ReAct、工具系统与执行边界



## Python 1：迭代器和生成器有什么区别？

**参考答案：**迭代器实现 __iter__ 和 __next__ 协议；生成器函数使用 yield，调用后返回生成器对象，并在迭代过程中保留执行状态。

**面试官追问：**生成器如何通过 yield from 组合子生成器？

**追问参考答案：**yield from 会把子生成器的迭代值传递给外层调用方，也会转发 send、throw 等交互，并可接收子生成器的返回值。适合组合多个迭代流程，但需要注意异常传播。

**代码示例：**

```python
def child():
    yield 1
    yield 2
    return "完成"

def parent():
    result = yield from child()
    print(result)

assert list(parent()) == [1, 2]
```


## Python 2：上下文管理器如何工作？

**参考答案：**with 调用对象的 __enter__ 和 __exit__，用于保证资源清理。contextlib.contextmanager 可以使用生成器定义上下文管理器。

**面试官追问：**__exit__ 返回 True 对异常传播有什么影响？

**追问参考答案：**__exit__ 返回真值表示异常已被处理，with 语句通常不会继续传播该异常。一般资源管理器应返回 False 或 None，避免意外吞掉业务异常。
