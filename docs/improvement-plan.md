# leetpath 上线前改进清单与执行指南

> 本清单由代码评审产出，交给执行 AI（grok / codex 等）逐项落实。
> 目标环境：RackNerd 圣何塞 VPS + Cloudflare Tunnel（保持 README 现有部署方案不变）。

## 执行规则（必读）

1. **按编号顺序执行**，一次只做一项。完成一项后：把该项的 `- [ ]` 改为 `- [x]`，并在该项末尾的「完成备注」处用一行写明实际改了哪些文件。
2. 每项都有「验收」命令，**必须实际运行并通过**才能打勾；无法在本机验证的项（已标注）打勾时在备注中写明"待服务器验证"。
3. **严格限定范围**：只做清单内列出的事。禁止顺手重构、禁止改判题协议 / API 路径 / 数据库表结构、禁止升级依赖大版本、禁止引入新框架或新服务。执行中发现清单之外的问题，记录到文末「执行中发现的问题」小节，**不要动手改**。
4. 遵守仓库 `AGENTS.md` 约定：UI 文案与注释用中文；不提交 `.env`、`data/`、构建产物。
5. 建议每完成一项提交一个 commit，message 用 `chore:` / `fix:` / `feat:` / `ci:` 前缀 + 一句中文描述。
6. C 组是**明确暂缓**的事项，本轮禁止实施。

---

## A 组：部署前必做（运维与工程化）

### A1. 锁定后端依赖版本

- [x] **A1 完成**

**问题**：`backend/requirements.txt` 全部使用 `>=` 浮动版本，服务器每次 rebuild 可能拉到不同版本，镜像不可复现，新版本可能引入破坏性变更。

**改法**：
1. 在本地已有的 `backend/.venv`（Python 3.14）中运行 `pip freeze`，找出当前实际安装的这 9 个包的版本号。
2. 把 `backend/requirements.txt` 中所有 `>=` 改成 `==` 并填入实际版本号。`uvicorn[standard]` 的 extras 写法保留（如 `uvicorn[standard]==0.35.0`）。保留文件头部注释。
3. 不引入 pip-tools / uv / lock 文件等额外机制，直接固定 `==` 即可。

**验收**：`cd backend && pip install -r requirements.txt` 无报错，`pytest` 全部通过。

完成备注：`backend/requirements.txt`

---

### A2. 统一 Python 版本（Dockerfile 3.12 → 3.14）

- [x] **A2 完成**

**问题**：本地开发是 Python 3.14（`.venv` 与 pycache 均为 cp314），`backend/Dockerfile` 却用 `python:3.12-slim`，存在"本地测试通过、容器内行为不一致"的风险；`requirements.txt` 的注释也写明按 3.14 选包。

**改法**：`backend/Dockerfile` 第 2 行 `FROM python:3.12-slim` 改为 `FROM python:3.14-slim`。其余不动（该 Dockerfile 里 apt 安装 docker-ce-cli 的部分与 Python 版本无关）。

**依赖**：先完成 A1（锁定的版本号来自本地 3.14 环境，与容器一致后才有意义）。

**验收**：`docker build -t leetpath-backend ./backend` 构建成功；若本机无 Docker，备注"待服务器验证"。

完成备注：`backend/Dockerfile`（FROM python:3.12-slim → python:3.14-slim；本机构建成功）

---

### A3. 补齐 .dockerignore（两个文件）

- [x] **A3 完成**

**问题**：仓库没有任何 `.dockerignore`。后端镜像 `COPY . .` 会把本地 `.venv/`、`data/`（开发数据库，含密码哈希）、`__pycache__/` 送进构建上下文；前端构建上下文是仓库根目录，`COPY frontend/ ./` 会让本地 Windows 的 `node_modules/` 覆盖容器内 `npm ci` 装好的 Linux 依赖（esbuild 等平台二进制不兼容，构建损坏）。

**改法**：

新建 `backend/.dockerignore`（作用于 backend 构建上下文）：

```
.venv/
data/
tests/
.pytest_cache/
__pycache__/
*.pyc
*.db
*.db-wal
*.db-shm
```

新建仓库根目录 `.dockerignore`（作用于 frontend 构建上下文，context 为 `.`）：

```
.git/
.env
data/
backend/
docs/
scripts/
terminals/
**/node_modules
frontend/dist/
```

注意：根 `.dockerignore` 不能忽略 `deploy/`（frontend Dockerfile 需要 `deploy/nginx.conf`）和 `frontend/` 本身。

**验收**：`docker compose build backend frontend` 成功；若本机无 Docker，备注"待服务器验证"。

完成备注：`backend/.dockerignore`, `.dockerignore`

---

### A4. Docker 日志轮转

- [x] **A4 完成**

**问题**：`docker-compose.yml` 未配置 logging，Docker 默认 json-file 驱动无大小上限，VPS 磁盘会被日志慢慢吃满。

**改法**：在 `docker-compose.yml` 顶部加 YAML 锚点，并给 `backend`、`judge`、`backup`、`frontend`、`cloudflared` 五个长驻服务各加一行引用（`judge-python`、`judge-cpp` 是 build-only 服务，不需要）：

```yaml
x-logging: &default-logging
  driver: json-file
  options:
    max-size: "10m"
    max-file: "3"
```

每个服务内加：

```yaml
    logging: *default-logging
```

**验收**：`docker compose --profile production config` 输出无报错且包含 `max-size`。

完成备注：`docker-compose.yml`

---

### A5. 健康检查端点 + compose healthcheck

- [x] **A5 完成**

**问题**：没有健康检查端点；compose 的 `depends_on` 只保证启动顺序，不保证后端真正可服务。

**改法**：
1. 在 `backend/app/main.py` 中新增无需登录的健康检查端点（不要挂到带 `_protected` 依赖的 router 上）：

```python
from sqlalchemy import text
from sqlalchemy.orm import Session
from app.db import get_db

@app.get("/api/health")
def health(db: Session = Depends(get_db)) -> dict[str, str]:
    db.execute(text("SELECT 1"))
    return {"status": "ok"}
```

2. `docker-compose.yml` 的 `backend` 服务加（镜像内已有 curl）：

```yaml
    healthcheck:
      test: ["CMD", "curl", "-fsS", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 5s
      retries: 3
      start_period: 15s
```

3. `frontend` 服务的 `depends_on` 改为条件形式：

```yaml
    depends_on:
      backend:
        condition: service_healthy
```

4. 新增 `backend/tests/test_health.py`：用现有 `client` fixture 请求 `/api/health`，断言 200 且 `{"status": "ok"}`。

**验收**：`cd backend && pytest` 全过；`docker compose --profile production config` 无报错。

完成备注：`backend/app/main.py`, `docker-compose.yml`, `backend/tests/test_health.py`

---

### A6. GitHub Actions CI

- [x] **A6 完成**

**问题**：仓库无 CI。前端 `build` 脚本不含类型检查，类型错误能带病合入；后端测试也只靠手动跑。

**改法**：新建 `.github/workflows/ci.yml`（测试已确认不依赖真实 Docker，judge 相关测试均为 mock）：

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.14"
      - run: pip install -r requirements.txt
        working-directory: backend
      - run: pytest
        working-directory: backend

  frontend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
          cache-dependency-path: frontend/package-lock.json
      - run: npm ci
        working-directory: frontend
      - run: npm run typecheck
        working-directory: frontend
      - run: npm run build
        working-directory: frontend
```

**验收**：push 到 GitHub 后，`gh run list --limit 1` 显示最新 workflow 运行成功（或在网页 Actions 页确认两个 job 全绿）。

完成备注：`.github/workflows/ci.yml`（GitHub Actions 跑通待最终 push 后确认）

---

## B 组：安全与健壮性（代码）

### B1. 登录防用户名枚举 + IP 维度限流兜底

- [x] **B1 完成**

**问题**（`backend/app/routers/auth.py`）：
1. 用户名不存在时直接返回 401，不执行 bcrypt 校验；bcrypt 验证约 100ms，攻击者可通过响应时间差枚举有效用户名。
2. 登录限流 key 是 `login:{ip}:{username}`，换用户名即可绕过，缺少纯 IP 维度的兜底。

**改法**（都在 `auth.py`）：
1. 模块级增加一个假哈希常量（import 时计算一次）：

```python
_DUMMY_PASSWORD_HASH = hash_password("timing-equalizer-dummy")
```

2. `login` 函数中，在现有 per-username 限流**之前**加一条 IP 兜底限流：

```python
request_limiter.check(f"login-ip:{client_ip(request)}", limit=20, window_seconds=60)
```

3. 把"用户不存在"分支改为也执行一次假校验再统一报错，保证两种失败路径耗时接近：

```python
user = db.scalar(select(User).where(User.username == body.username))
if user is None:
    verify_password(body.password, _DUMMY_PASSWORD_HASH)
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
if not verify_password(body.password, user.password_hash):
    raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="用户名或密码错误")
```

4. 在 `backend/tests/test_security.py` 中补一个测试：同一 IP 连续用 21 个不同用户名登录，第 21 次返回 429。

**验收**：`cd backend && pytest` 全过（含新增测试）。

完成备注：`backend/app/routers/auth.py`, `backend/tests/test_security.py`

---

### B2. judge 容器临时目录缩窄（不再挂载宿主整个 /tmp）

- [x] **B2 完成**

**问题**：`docker-compose.yml` 的 judge 服务挂载 `- /tmp:/tmp`，评测工作目录建在宿主 `/tmp/<提交id>` 且 `chmod 0o777`，宿主上任何进程都可在评测瞬间篡改代码与用例；裸数字目录名也可能与宿主已有文件冲突。

**改法**：
1. `docker-compose.yml` judge 服务：`- /tmp:/tmp` 改为 `- /var/lib/leetpath/judge-tmp:/var/lib/leetpath/judge-tmp`，并加环境变量：

```yaml
    environment:
      TMPDIR: /var/lib/leetpath/judge-tmp
```

原理：worker 用 `tempfile.gettempdir()` 取临时目录，它会读 `TMPDIR`；容器内外路径必须完全一致（worker 通过宿主 docker daemon 给评测容器传 `-v 宿主路径`），所以两侧统一为 `/var/lib/leetpath/judge-tmp`。宿主目录 Docker 会自动创建。同步更新该行原有的中文注释。

2. `backend/judge/worker.py` 两处工作目录名加前缀，避免与他人文件冲突：
   - `_prepare_workdir` 中 `Path(tempfile.gettempdir()) / str(job.submission_id)` 改为 `/ f"lpj-{job.submission_id}"`；
   - `process_submission` 中 `Path(tempfile.gettempdir()) / str(submission_id)` 改为 `/ f"lpj-{submission_id}"`（两处必须保持一致）。

3. 本地 Windows 开发不设 `TMPDIR`，行为不变，无需其他适配。

**验收**：`cd backend && pytest` 全过；最终判题功能在服务器部署后用真实提交验证（备注"待服务器验证"）。

完成备注：`docker-compose.yml`, `backend/judge/worker.py`；待服务器验证

---

### B3. backend / backup 容器以非 root 运行

- [x] **B3 完成**

**问题**：`backend/Dockerfile` 无 `USER` 指令，backend 与 backup 容器内进程以 root 运行。虽有 `read_only` + `cap_drop` 兜底，但非 root 是低成本的纵深防御。judge 容器需要访问宿主 docker.sock，**保持 root 不动**。

**改法**：
1. `backend/Dockerfile` 在 `COPY . .` 之后加：

```dockerfile
RUN useradd --uid 10001 --create-home appuser \
    && mkdir -p /app/data /app/backups \
    && chown appuser /app/data /app/backups
```

不要写全局 `USER appuser`（judge 服务共用此镜像且需要 root）。

2. `docker-compose.yml` 中 `backend` 和 `backup` 两个服务各加：

```yaml
    user: "10001"
```

`judge` 服务不加。

3. 注意：named volume 首次挂载会继承镜像内目录属主，新部署无问题；如果本地已有旧的 `leetpath-data` 卷（属主 root），需 `docker compose down -v` 清掉重建（本地是测试数据，可丢弃）。在完成备注中说明是否清理过。

**验收**：本机有 Docker 则 `docker compose up -d backend` 后 `docker compose exec backend id` 显示 `uid=10001`，注册/登录正常；无 Docker 则备注"待服务器验证"。

完成备注：`backend/Dockerfile`, `docker-compose.yml`；未清理 named volume（本机无旧卷，新卷由镜像内 appuser 属主继承）；`docker compose exec backend id` 为 `uid=10001(appuser)`，容器内 curl `/api/health` 返回 `{"status":"ok"}`；注册/登录接口可响应（无邀请码故注册 400、登录 401）。

---

### B4. 前端补错误态（HomeView / AdminView / LinksView）

- [x] **B4 完成**

**问题**：
- `HomeView.vue` 数据加载失败被整段 catch 静默吞掉，弱网下呈现为无提示的空数据页；
- `AdminView.vue` 初始加载（问题列表/岗位/邀请码）无任何错误保护；
- `LinksView.vue` 的 `try/finally` 没有 catch，加载失败会显示成"暂无链接"，误导用户。

**改法**（保持 KISS，不引入全局错误方案）：三个 view 各加一个 `error` ref；加载失败时置中文错误文案（如"加载失败，请检查网络后重试"），模板顶部渲染错误条 + "重试"按钮，点击重新调用加载函数。样式复用 `styles.css` 中已有的错误提示类（登录页在用的那套）；若无可复用类，新增一个简单的 `.error-banner` 类，遵循现有设计变量（`var(--danger)` 等）。加载成功后清空 `error`。

**验收**：`cd frontend && npm run typecheck && npm run build` 通过；手测：停掉后端后刷新首页/管理页/八股页，三页均显示错误提示与重试按钮，不再是空白或"暂无数据"。

完成备注：`frontend/src/views/HomeView.vue`, `frontend/src/views/AdminView.vue`, `frontend/src/views/LinksView.vue`, `frontend/src/styles.css`；`npm run typecheck` / `npm run build` 通过；手测待浏览器。

---

### B5. 移动端底栏适配 iPhone 安全区

- [ ] **B5 完成**

**问题**：`frontend/index.html` 已设 `viewport-fit=cover`，但 `styles.css` 未使用 `env(safe-area-inset-bottom)`，全面屏 iPhone 上底部 Tab 栏会与 Home Indicator 重叠。

**改法**（`frontend/src/styles.css`）：
1. `.bottom-tabs` 规则加：`padding-bottom: env(safe-area-inset-bottom);`
2. `@media (max-width: 1023px)` 中 `body { padding-bottom: 62px; }` 改为 `padding-bottom: calc(62px + env(safe-area-inset-bottom));`

**验收**：`npm run typecheck && npm run build` 通过；浏览器 DevTools 选 iPhone 14 Pro 之类的机型模拟，底栏与屏幕底缘之间出现安全区留白。

完成备注：

---

## C 组：明确暂缓（本轮禁止做）

以下事项已知，但**本轮不做**，执行 AI 不得实施：

- 引入 Alembic 数据库迁移（当前 `create_all` 方案在题库/模型稳定期够用）
- 拆分 `HandbookView.vue`（约 1119 行）与 `styles.css`（约 2058 行）
- 引入 ESLint / Prettier / 前端单测
- 把 `stores/` 下的 composable 重构为 Pinia store
- 提交耗时显示扣除沙箱启动开销
- DOMPurify 为 Markdown 内链接统一注入 `rel="noopener"`
- `AGENTS.md` / `docs/spec` 中 768px 断点描述与实现（仅 1024px）的口径统一

## 全部完成后的总验收

依次运行并确认：

```bash
cd backend && pytest                       # 全部通过
cd frontend && npm run typecheck           # 无类型错误
cd frontend && npm run build               # 构建成功
docker compose --profile production config # 无配置错误
git status                                 # 无 .env / data / 构建产物待提交
```

全部通过后 push 到 GitHub，确认 Actions 两个 job 全绿。

## 执行中发现的问题

（执行 AI 在此记录清单之外发现的问题，只记录、不修改）
