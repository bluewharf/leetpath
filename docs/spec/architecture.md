# 总体架构

```
浏览器(响应式 SPA)
      │ HTTPS + 可选 Cloudflare Access
Cloudflare Edge ── 出站 Tunnel ── nginx (静态文件 + /api 反代，无宿主端口)
                                      │ internal network
                                 FastAPI backend ── SQLite (WAL)
      │ submissions 表 status=pending
      │
  judge worker (独立进程/容器, 可用 docker CLI)
      └─→ docker run --network none --read-only --user 65534:65534 \
              --cap-drop ALL --memory 256m --cpus 0.5 一次性容器逐用例评测
```

- 单体仓库三部分：`backend/`（FastAPI）、`backend/judge/`（判题 worker + 镜像）、`frontend/`（Vue SPA）。
- 判题 worker 与 backend 共用同一个 SQLite 文件和 `app.models`，通过轮询 `submissions` 表解耦，不引入消息队列。
- 生产入口仅为 Cloudflare Tunnel，frontend/backend 不映射宿主端口；不满足强密钥、Secure Cookie 和 HTTPS Origin 时后端拒绝启动。
- 认证：JWT 存 HttpOnly Cookie（SameSite=Lax + Secure），管理员由 CLI 初始化，普通用户凭单次邀请码注册；写请求额外校验 Origin。
- backup 服务使用 SQLite Online Backup API 将一致快照写入独立卷；仍需异机复制和恢复演练。
- 题库种子：`backend/app/seed/problems/<slug>/` 目录（meta.toml + statement.md + tests/ + reference.py），`loader.py` 幂等导入。
- 校招看板为简单 CRUD；大模型八股只是一个外链清单（小林笔记），不做内容。
- 详细契约见同目录 `backend-api.md`、`judge.md`、`frontend.md`、`seed-format.md`。
