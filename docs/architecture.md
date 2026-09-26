# 毕业项目：企业级智能知识库与任务执行平台

## 目标

实现支持真实模型调用、混合检索、工具执行、MCP、
状态持久化、安全审批和质量评估的 Agent 平台。

## 推荐模块

- `project/app/`：FastAPI、请求模型与流式接口
- `project/agent/`：LangGraph 状态图与路由
- `project/rag/`：文档解析、Embedding、Qdrant、BM25 与 Reranker
- `project/tools/`：工具注册、权限与 MCP
- `project/memory/`：会话状态与长期记忆
- `project/evaluation/`：检索、答案和工具执行评估
- `project/infrastructure/`：配置、存储、日志与监控

## 生产验收原则

1. 模型输出不是可信业务输入。
2. 权限必须在服务端校验。
3. 写入工具需要考虑幂等和审计。
4. 检索需要来源信息和租户隔离。
5. 关键链路必须有超时、指标和可复现测试。
