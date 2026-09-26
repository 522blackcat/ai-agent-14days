# Day 01 Python 面试题



课程主题：LLM 原理、Function Calling 与最小 Agent



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
