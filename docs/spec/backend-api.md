# 后端规格（FastAPI）

## 技术约束

- Python ≥ 3.12；依赖固定写在 `backend/requirements.txt`：
  `fastapi`、`uvicorn[standard]`、`sqlalchemy>=2.0`、`pydantic>=2`、`pydantic-settings`、`PyJWT`、`bcrypt`；测试用 `pytest`、`httpx`。
- 不使用 passlib（直接用 bcrypt）。TOML 解析用标准库 `tomllib`。
- SQLAlchemy 2.x 风格（`Mapped[]` / `mapped_column`），SQLite 开 WAL：`PRAGMA journal_mode=WAL`。
- 配置走环境变量（pydantic-settings），字段：
  - `SECRET_KEY`（默认 `dev-secret-change-me`，生产必须覆盖）
  - `DATABASE_URL`（默认 `sqlite:///data/leetpath.db`，相对 backend 目录；启动时自动建目录）
  - `TOKEN_TTL_DAYS`（默认 7）
  - `COOKIE_NAME`（默认 `leetpath_token`）
  - `COOKIE_SECURE`（默认 false）
- 入口 `app/main.py`：`FastAPI(title="leetpath")`，挂所有 router（前缀 `/api`），启动时 `Base.metadata.create_all`。开发期 CORS 放行 `http://localhost:5173`（allow_credentials=True）。
- 除 `/api/auth/*` 外的所有接口要求登录（依赖注入解析 cookie 中的 JWT，失败 401）。

## 数据模型（`app/models.py`）

- `User`: id, username(唯一索引, 3-32), email(可空), password_hash, is_admin(bool, 默认 False), created_at
- `Problem`: id, slug(唯一索引), title, difficulty(`easy|medium|hard`), source(`hot100|mianjing`), tags(JSON list[str]), statement_md(Text), time_limit_ms(默认 5000), memory_limit_mb(默认 256), is_published(bool 默认 True), created_at
- `Testcase`: id, problem_id(FK, 索引), ordinal(int), input(Text), expected_output(Text), is_sample(bool)；UniqueConstraint(problem_id, ordinal)
- `Submission`: id, user_id(FK, 索引), problem_id(FK), language(`python3|cpp`), code(Text), status(默认 `pending`, 索引), detail(JSON, 可空), compile_output(Text, 可空), runtime_ms(int, 可空), created_at(索引)
- `Draft`: 联合主键(user_id, problem_id, language)；code(Text), updated_at
- `Job`: id, company, position, batch(可空, 如 `2026秋招`), open_at(Date, 可空), deadline_at(Date, 可空, 索引), jd_text(Text, 可空), apply_url(可空), status(默认 `open`, 另有 `closed`), created_at

提交状态枚举：`pending | judging | AC | WA | TLE | MLE | CE | RE | IE`。

## 认证（`app/auth.py` + `app/routers/auth.py`）

- bcrypt 哈希；JWT（HS256，payload: sub=user_id, exp）；登录成功写 HttpOnly Cookie（SameSite=Lax，secure 取 COOKIE_SECURE，path=/）。
- `POST /api/auth/register` body `{username, password, email?}`：username 只允许 `[a-zA-Z0-9_]{3,32}`，password ≥ 8 位。用户名已存在 → 409。**第一个注册的用户自动 is_admin=True**。成功 201，返回用户 JSON 并种 cookie。
- `POST /api/auth/login` `{username, password}`：成功 200 + cookie；失败 401（`用户名或密码错误`）。
- `POST /api/auth/logout`：清 cookie，204。
- `GET /api/auth/me`：`{id, username, email, is_admin}`；未登录 401。
- 用户 JSON 一律不含 password_hash。

## 路由

### `app/routers/problems.py`

- `GET /api/problems?difficulty=&source=&tag=&q=` → `[{id, slug, title, difficulty, source, tags, my_status}]`，只含 `is_published=True`。`my_status`：`solved`（有 AC 提交）/ `attempted`（有提交无 AC）/ `null`。q 匹配 title/slug 子串（大小写不敏感）。
- `GET /api/problems/{slug}` → 详情：`{id, slug, title, difficulty, source, tags, statement_md, time_limit_ms, memory_limit_mb, samples: [{ordinal, input, expected_output}]}`（samples 只含 is_sample=True，按 ordinal 排序）。404 不存在或未发布。

### `app/routers/submissions.py`

- `POST /api/submissions` body `{problem_slug, language, code}`：language ∈ {python3, cpp}，code ≤ 64KB。该用户 pending/judging 提交 ≥ 5 → 429。成功 202 → `{id, status: "pending"}`。
- `GET /api/submissions/{id}` → 仅本人或管理员：`{id, problem_slug, problem_title, language, code, status, runtime_ms, compile_output, detail, created_at}`。detail 结构见 `judge.md`。
- `GET /api/submissions?problem_slug=&limit=50` → 我的提交列表（不含 code，新→旧）。

### `app/routers/drafts.py`

- `GET /api/drafts/{slug}?language=python3` → `{code, updated_at, is_default}`；无草稿时返回该语言默认模板（is_default=true）。模板：
  - python3: `import sys\n\n\ndef main():\n    data = sys.stdin.read().split()\n    # TODO: 解析输入并求解\n    ...\n\n\nif __name__ == "__main__":\n    main()\n`
  - cpp: `#include <bits/stdc++.h>\nusing namespace std;\n\nint main() {\n    ios::sync_with_stdio(false);\n    cin.tie(nullptr);\n    // TODO\n    return 0;\n}\n`
- `PUT /api/drafts/{slug}` body `{language, code}` → upsert，返回 `{updated_at}`。code ≤ 64KB。

### `app/routers/jobs.py`

- `GET /api/jobs` → 全部，按 deadline_at 升序（NULL 最后），返回完整字段 + `days_left`（可空）。
- 管理员：`POST /api/jobs`、`PUT /api/jobs/{id}`、`DELETE /api/jobs/{id}`（204）。非管理员 403。

### `app/routers/links.py`

- `GET /api/links` → 读取 `app/data/links.json`（仓库内置，字段 `[{category, title, url, note?}]`），内容为小林笔记（xiaolincoding.com）各栏目外链，含"大模型面试"分类。target=_blank 由前端处理。

### 管理员题目维护（`app/routers/admin.py`，全部要求 is_admin，否则 403）

- `POST /api/admin/seed/reload` → 同步执行 seed loader，返回 `{imported: n}`。
- `PUT /api/admin/problems/{id}` body `{is_published}` → 上下架。
- `GET /api/admin/problems` → 含未发布的完整列表。

## 种子加载（`app/seed/loader.py`）

- 扫描 `app/seed/problems/*/`，解析 `meta.toml`（tomllib）+ `statement.md` + `tests/NNN.in|NNN.out`。格式详见 `seed-format.md`。
- 按 slug upsert：存在则更新字段并**删除旧 testcases 后重建**；不存在则插入。`python -m app.seed.loader` 可独立运行，也供 admin 路由调用。打印导入数量。
- meta.toml 中 `samples = [1, 2]` 指定哪些用例公开。

## 测试（`backend/tests/`）

pytest + FastAPI TestClient，用临时目录 SQLite（conftest 里 monkeypatch DATABASE_URL）。覆盖：注册/登录/me/登出、第一个用户是管理员、题目列表与详情（先跑 loader 导入 1 个 fixture 题目）、草稿读写与默认值、提交创建（状态 pending）、提交限流、jobs CRUD 权限、links。判题流程不在 pytest 范围。

## 运行

```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```
