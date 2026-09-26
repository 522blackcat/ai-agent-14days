# Day 01：Python 与 AI Agent 高级面试



建议先独立回答，再查看参考答案与追问答案。



## Python 高级面试



## Python 1：Python 函数参数究竟如何传递？

**参考答案：**Python 将对象引用绑定到函数的局部参数名。函数内部重新绑定参数名，不会修改调用方的变量绑定；但如果参数指向可变对象，原地修改会被调用方观察到。

**面试官追问：**为什么 list.append() 与 a = a + [1] 的行为可能不同？

**追问参考答案：**append() 原地修改原列表，因此持有该列表引用的调用方可以观察到变化。a = a + [1] 通常创建新列表，再将局部变量 a 重新绑定到新对象；调用方原来的变量仍指向旧列表。

**代码示例：**

```python
def mutate(items):
    items.append(1)       # 原地修改调用方传入的列表
    items = items + [2]   # 重新绑定局部变量
    return items

original = []
result = mutate(original)

assert original == [1]
assert result == [1, 2]
```


## Python 2：为什么可变默认参数危险？

**参考答案：**默认参数在函数定义时求值，而不是每次调用时求值。使用 [] 或 {} 作为默认值可能导致多次调用共享同一对象。通常使用 None 作为哨兵，在函数内部创建新对象。

**面试官追问：**dataclass 中如何使用 field(default_factory=list)？

**追问参考答案：**使用 field(default_factory=list)。default_factory 是可调用对象，每次创建 dataclass 实例时都会调用它，生成独立列表。

**代码示例：**

```python
from dataclasses import dataclass, field

def collect(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items

@dataclass
class Task:
    tags: list[str] = field(default_factory=list)

assert collect(1) == [1]
assert collect(2) == [2]
assert Task().tags is not Task().tags
```




## AI Agent 高级面试



## Agent 1：Function Calling 的完整执行链路是什么？

**参考答案：**用户消息和工具 Schema 发给模型；模型返回工具调用名称与参数；服务端校验并执行；将工具结果与调用 ID 关联后传回模型；模型继续推理或输出最终回答。工具执行权始终在应用程序。

**面试官追问：**模型生成了一个不存在的工具名称，系统应该怎么办？

**追问参考答案：**拒绝执行未知工具，记录受控错误，并将安全的错误结果返回模型，由模型重新选择工具或向用户说明无法完成。不能动态执行模型提供的函数名。


## Agent 2：Temperature 设置为 0 是否绝对确定？

**参考答案：**不能保证。模型服务实现、并行计算、模型版本、请求参数和工具结果等因素仍可能造成差异。关键业务需要结构化校验、测试和确定性代码兜底。

**面试官追问：**如何测试 Agent 的非确定性输出？

**追问参考答案：**固定测试输入、工具返回和评价标准；对结构化输出验证 Schema，对工具调用验证名称与参数，对开放式回答使用多次运行、规则评估和人工抽样。关键业务结果应由确定性程序校验。




## 我的面试复盘



个人回答请记录在同目录的 `answers.md`，不要直接修改本文件，以免下次补全时被覆盖。
