# Day 04 Python 面试题



课程主题：RAG、Embedding、Chunking 与 Qdrant



## Python 1：dict 为什么通常能高效查找？

**参考答案：**dict 基于哈希表，通过键的哈希值定位存储位置。平均查找复杂度通常接近 O(1)，但哈希冲突、扩容和键的哈希质量会影响表现。

**面试官追问：**为什么可变 list 不能直接作为 dict 的键？

**追问参考答案：**list 是可变对象，通常不可哈希，因此不能直接作为 dict 键。字典键要求哈希值在其作为键期间保持稳定，并满足相等对象哈希相等。如果数据本身适合不可变表示，可考虑 tuple。


## Python 2：如何实现高效 Top-K？

**参考答案：**当 K 远小于数据量时，可以使用大小为 K 的最小堆，时间复杂度约为 O(N log K)，避免对全部结果排序。

**面试官追问：**海量检索结果如何在内存受限时求 Top-K？

**追问参考答案：**维护大小为 K 的最小堆，逐条处理输入，当新元素优于堆顶时替换堆顶。空间复杂度为 O(K)，时间复杂度约为 O(N log K)，适合流式数据。

**代码示例：**

```python
import heapq

def top_k(numbers, k):
    if k <= 0:
        return []
    return heapq.nlargest(k, numbers)

assert top_k([5, 1, 9, 3, 7], 3) == [9, 7, 5]
```
