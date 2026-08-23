# leetpath

响应式个人刷题站：力扣热题 100 + 面经高频手撕题库，Python3/C++ 在线评测（Docker 沙箱），草稿入库多端同步，首页校招看板，大模型八股外链小林笔记。

## 技术栈

- 后端：FastAPI + SQLAlchemy 2.x + SQLite(WAL)，JWT cookie 认证（bcrypt）
- 前端：Vue 3 + Vite + TypeScript + CodeMirror 6 + marked/dompurify，手写响应式 CSS（断点 768px/1024px）
- 判题：独立 worker 进程轮询 SQLite，每次提交起一次性 Docker 容器（`--network none --read-only`）
- 部署：docker-compose（nginx 静态+反代 / backend / judge worker）

## 目录

- `backend/app/` — FastAPI 应用（models/routers/auth/seed loader）
- `backend/judge/` — 判题 worker 与判题镜像 Dockerfile
- `backend/tests/` — pytest
- `frontend/src/` — SPA
- `docs/spec/` — 各模块规格（实现前必读）
- `docs/seed/hot100-manifest.md` — 热题 100 清单

## 常用命令

```bash
# 后端开发
cd backend && pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
pytest

# 种子数据导入 / 校验
python -m app.seed.loader
python scripts/validate_seed.py   # 在仓库根目录运行

# 判题镜像
docker build -t leetpath-judge-python -f judge/Dockerfile.python judge
docker build -t leetpath-judge-cpp    -f judge/Dockerfile.cpp judge

# 判题 worker
python -m judge.worker

# 前端
cd frontend && npm install && npm run dev   # /api 代理到 8000
npm run build
```

## 约定

- 判题协议为 ACM 模式（stdin/stdout），测试用例比对忽略行尾空白与末尾空行
- 提交状态：pending / judging / AC / WA / TLE / MLE / CE / RE / IE
- 所有 API 在 `/api` 前缀下，除 `/api/auth/*` 外均需登录
- 题面、注释、UI 文案用中文；代码标识符用英文
- 不要提交 `.env`、`data/`、种子数据以外的产物
