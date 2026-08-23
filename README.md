# leetpath

响应式个人刷题站：力扣热题 100 + 面经高频手撕题库，Python3 / C++ 在线评测（Docker 沙箱），草稿入库多端同步，首页校招看板，大模型八股外链小林笔记。

题面与评测为 ACM 模式（stdin / stdout）。本仓库仅供个人学习使用。

## 功能

- 热题 100 与面经手撕：题面 Markdown、样例与隐藏用例、按难度 / 来源 / 标签筛选
- 在线评测：Python3 与 C++，状态 `pending / judging / AC / WA / TLE / MLE / CE / RE / IE`
- 代码草稿入库，登录后多端同步
- 校招看板：岗位、批次、截止日、投递链接（管理员 CRUD）
- 八股外链：小林笔记（含大模型面试栏目）
- 响应式 SPA：桌面双栏刷题，移动端 Tab

## 技术栈

- 后端：FastAPI + SQLAlchemy 2.x + SQLite（WAL），JWT HttpOnly Cookie（bcrypt）
- 前端：Vue 3 + Vite + TypeScript + CodeMirror 6 + marked / dompurify，手写 CSS（断点 768px / 1024px）
- 判题：独立 worker 轮询 SQLite，每次提交起一次性 Docker 容器（`--network none --read-only`）
- 部署：docker compose（nginx 静态 + `/api` 反代 / backend / judge worker）

## 本地开发

需要 Python ≥ 3.12、Node.js 22+。判题另需本机 Docker。

### 后端

```bash
cd backend
python -m venv .venv
# Windows: .venv\Scripts\activate
# Unix:    source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

第一个注册用户自动成为管理员。开发期 CORS 放行 `http://localhost:5173`。

```bash
cd backend && pytest
```

### 前端

```bash
cd frontend
npm install
npm run dev
```

开发服务器在 5173，`/api` 代理到 `http://localhost:8000`。

### 种子导入 / 校验

```bash
# 导入题库（在 backend/ 目录）
python -m app.seed.loader

# 校验参考解与用例（仓库根目录）
python scripts/validate_seed.py
python scripts/validate_seed.py two-sum
```

也可登录管理员账号后调用 `POST /api/admin/seed/reload`，或在前端「管理」页重新导入。

### 判题 worker

先在本机构建评测镜像，再于 `backend/` 下启动 worker（与 API 共用同一个 SQLite）：

```bash
cd backend
docker build -t leetpath-judge-python -f judge/Dockerfile.python judge
docker build -t leetpath-judge-cpp    -f judge/Dockerfile.cpp judge
python -m judge.worker
```

`DATABASE_URL` 需与后端一致（默认 `sqlite:///data/leetpath.db`，相对 `backend/`）。

## Docker 部署

宿主机需要 Docker 与 Compose。judge 容器挂载 `/var/run/docker.sock`，在宿主 daemon 上启动一次性评测容器，因此**判题镜像必须打到宿主机**，而不是只存在于某个容器里。

1. 复制环境变量并填写密钥：

   ```bash
   cp .env.example .env
   # 编辑 SECRET_KEY；生产且走 HTTPS 时把 COOKIE_SECURE 改为 true
   ```

2. 构建判题镜像（profile `judge-images`，不会随 `up` 启动）：

   ```bash
   docker compose build judge-python judge-cpp
   ```

3. 启动 API、worker 与前端（80 端口）：

   ```bash
   docker compose up -d --build
   ```

4. 导入题库（镜像内已含种子目录，空 volume 首次需导入）：

   ```bash
   docker compose exec backend python -m app.seed.loader
   ```

5. 浏览器打开 `http://localhost`，注册账号后即可刷题。

常用命令：`docker compose logs -f`、`docker compose down`。数据在 named volume `leetpath-data`（对应容器内 `/app/data`，与 `DATABASE_URL=sqlite:///data/leetpath.db` 一致）。

## 目录结构

```
.
├── backend/
│   ├── app/                 # FastAPI：models / routers / auth / seed
│   ├── judge/               # worker 与判题镜像 Dockerfile
│   ├── tests/
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/                 # Vue SPA
│   └── Dockerfile
├── deploy/nginx.conf        # 静态站点 + /api 反代
├── docs/spec/               # 模块规格
├── docs/seed/               # 热题 100 清单
├── scripts/validate_seed.py
├── docker-compose.yml
└── .env.example
```

## 添加新题 / 面经题

每题一个目录 `backend/app/seed/problems/<slug>/`（`meta.toml` + `statement.md` + `tests/` + `reference.py`），`source` 取 `hot100` 或 `mianjing`。格式与 I/O 约定见 [docs/spec/seed-format.md](docs/spec/seed-format.md)。写完后在仓库根目录执行 `python scripts/validate_seed.py <slug>`，再 `python -m app.seed.loader`（或管理页「重新导入种子」）。

## 安全注意事项

- **docker.sock**：judge 服务把宿主 Docker 套接字挂进容器，等价于该容器可操控宿主机 Docker（通常即 root）。只用于自己信任的个人部署，不要暴露给不可信网络或多人共享主机。
- **题库版权**：题面与用例仅限个人学习，请勿公开传播或用于商业用途。
- **密钥**：不要提交 `.env`。生产环境必须替换 `SECRET_KEY`，并在 HTTPS 下启用 `COOKIE_SECURE=true`。
