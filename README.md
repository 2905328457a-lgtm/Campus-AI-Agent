## 🚀 开发路线图 (Roadmap)

- [x] **Phase 1: 核心逻辑跑通** 
  - 基于 LangChain 实现校园文档的加载、切片与 Chroma 向量化。
  - 完成 Prompt 优化，有效控制大模型幻觉（不编造未收录内容）。
  - 使用 Streamlit 实现基础 Web 交互验证。

- [ ] **Phase 2: 后端工程化重构 (当前进度)**
  - 引入 FastAPI 框架，将 RAG 逻辑封装为标准化 RESTful API。
  - 实现基于 Pydantic 的请求数据校验。

- [ ] **Phase 3: 容器化与云端部署 (Planning)**
  - 编写 Dockerfile 实现环境隔离。
  - 部署至 Linux 云服务器，提供稳定的公网访问接口。
