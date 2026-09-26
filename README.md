# AI Agent 14 Days

面向高级 Python 工程师的 14 天 AI Agent 学习、实战和面试课程。

**学习时间：**每天 4–5 小时。  
**目标：**掌握真实模型调用、RAG、LangGraph、MCP、多 Agent 和生产工程。

## 学习进度

<!-- PROGRESS_START -->
**完成天数：1/14**  
**完成率：7.1%**  
**完成任务：10/140**
<!-- PROGRESS_END -->

## 14 天课程

| 天数 | 课程 | 进度 |
|---|---|---|
| 01 | [LLM 原理、Function Calling 与最小 Agent](days/day01/day01.md) | ✅ 已完成 |
| 02 | [ReAct、工具系统与执行边界](days/day02/day02.md) | ⬜ 未开始 |
| 03 | [LangGraph、状态机与 asyncio](days/day03/day03.md) | ⬜ 未开始 |
| 04 | [RAG、Embedding、Chunking 与 Qdrant](days/day04/day04.md) | ⬜ 未开始 |
| 05 | [BM25、Hybrid Search、RRF 与 Reranker](days/day05/day05.md) | ⬜ 未开始 |
| 06 | [Memory、MCP 与多 Agent](days/day06/day06.md) | ⬜ 未开始 |
| 07 | [第一阶段集成与架构验收](days/day07/day07.md) | ⬜ 未开始 |
| 08 | [FastAPI、SSE 与持久化 Agent 服务](days/day08/day08.md) | ⬜ 未开始 |
| 09 | [安全、权限、事务与故障恢复](days/day09/day09.md) | ⬜ 未开始 |
| 10 | [RAG Evaluation 与可观测性](days/day10/day10.md) | ⬜ 未开始 |
| 11 | [模型路由、推理性能与成本优化](days/day11/day11.md) | ⬜ 未开始 |
| 12 | [Docker、CI/CD 与生产部署](days/day12/day12.md) | ⬜ 未开始 |
| 13 | [高级 Agent 系统设计](days/day13/day13.md) | ⬜ 未开始 |
| 14 | [毕业项目验收与高级模拟面试](days/day14/day14.md) | ⬜ 未开始 |

## 专项面试题库

- [Python 高级面试题库](interview/python/README.md)
- [AI Agent 高级面试题库](interview/agent/README.md)

每一天还包含独立的 `interview.md`、`answers.md` 和 `progress.md`。

## 快速开始

```bash
python -m pip install -r requirements.txt
cp .env.example .env
```

Windows PowerShell 可以使用：

```powershell
Copy-Item .env.example .env
```

编辑 `.env`，配置云端模型或 Ollama。

运行 Day 01 示例：

```bash
python days/day01/src/agent.py
```

运行测试：

```bash
python -m pytest days/day01/tests -q
```

完成当天任务后，勾选 `days/dayXX/progress.md`，再运行：

```bash
python scripts/update_progress.py
```

## 项目目录

- `days/`：14 天课程、代码、测试、笔记和学习进度
- `interview/python/`：Python 高级面试题库
- `interview/agent/`：Agent 高级面试题库
- `project/`：持续开发的毕业项目
- `docs/`：架构与项目设计
- `scripts/`：学习进度脚本

## 技术栈

Python、FastAPI、Pydantic、LangGraph、OpenAI API、Ollama、
Qdrant、BGE-M3、BM25、Reranker、MCP、PostgreSQL、Redis、
Docker、OpenTelemetry、pytest。

## 课程使用说明

课程按天推进。Day 01 提供真实模型调用与工具执行代码；
后续课程提供原理、设计要求、任务和面试题，工程实现需要按天完成，
并持续整合到 `project/`。

**不要把 `.env`、真实密钥、生产数据或敏感日志提交到 Git。**
