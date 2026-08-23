# 总体架构

```
浏览器(响应式 SPA)
      │ HTTPS
   nginx (静态文件 + /api 反代)
      │
  FastAPI backend ── SQLite (WAL)
      │ submissions 表 status=pending
      │
  judge worker (独立进程/容器, 可用 docker CLI)
      └─→ docker run --rm --network none --read-only \
              --memory 256m --cpus 0.5 一次性容器逐用例评测
```

- 单体仓库三部分：`backend/`（FastAPI）、`backend/judge/`（判题 worker + 镜像）、`frontend/`（Vue SPA）。
- 判题 worker 与 backend 共用同一个 SQLite 文件和 `app.models`，通过轮询 `submissions` 表解耦，不引入消息队列。
- 认证：JWT 存 HttpOnly Cookie（SameSite=Lax），注册/登录后所有 `/api` 可用。
- 题库种子：`backend/app/seed/problems/<slug>/` 目录（meta.toml + statement.md + tests/ + reference.py），`loader.py` 幂等导入。
- 校招看板为简单 CRUD；大模型八股只是一个外链清单（小林笔记），不做内容。
- 详细契约见同目录 `backend-api.md`、`judge.md`、`frontend.md`、`seed-format.md`。
