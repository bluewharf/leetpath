# 排行榜 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 为 leetpath 增加可审计的算法题、八股和活跃时长日/周/总榜，并接入响应式前端。

**Architecture:** 后端以 `Submission.judged_at`、首次答对事件和受限学习会话作为事实源，`/api/leaderboard` 聚合榜单，`/api/activity/heartbeat` 接收活跃心跳。前端新增排行榜页面并在 App 根组件运行可见/聚焦计时器。

**Tech Stack:** FastAPI, SQLAlchemy 2, SQLite, pytest, Vue 3, TypeScript, Vite, CSS。

**Spec:** `docs/superpowers/specs/2026-08-25-leaderboard-design.md`

## Global Constraints

- 日界线和周界线固定使用 `Asia/Shanghai`。
- 题目榜按不同题目的首次 AC 统计；八股榜按不同题目的首次答对统计。
- 活跃时长单次心跳最多 60 秒、每日最多 8 小时。
- 所有 API 位于 `/api` 前缀且需要登录；界面文案使用中文。

---

### Task 1: 后端事实模型与迁移

**Files:**
- Modify: `backend/app/models.py`
- Modify: `backend/app/db.py`
- Modify: `backend/judge/worker.py`
- Test: `backend/tests/test_leaderboard.py`

- [x] 为 `Submission` 增加 nullable `judged_at`，新增 `QuizSolveEvent` 和 `StudySession` 模型及索引/唯一约束。
- [x] 为旧 SQLite 库在 `ensure_schema` 中补 `judged_at` 列。
- [x] 判题 worker 写最终状态时填充 `judged_at=utcnow()`。
- [ ] 先写模型/迁移/worker 的失败测试，确认旧库补列和 AC 完成时间写入行为。

### Task 2: 排行榜和心跳 API

**Files:**
- Create: `backend/app/routers/leaderboard.py`
- Create: `backend/app/services/leaderboard.py`
- Modify: `backend/app/routers/quiz.py`
- Modify: `backend/app/main.py`
- Test: `backend/tests/test_leaderboard.py`

- [x] 测试 `GET /api/leaderboard` 的参数校验、三种 board、today/week/all、去重、排序、我的排名和空榜。
- [x] 测试 `POST /api/activity/heartbeat` 的单次上限、每日上限、会话去重、非法 surface 和跨用户隔离。
- [x] 在答题首次正确时写入 `QuizSolveEvent`，重复正确不重复写入。
- [x] 实现服务层按 `Asia/Shanghai` 计算窗口并返回统一响应结构。
- [x] 注册受保护路由。

### Task 3: 前端契约、计时器和导航

**Files:**
- Modify: `frontend/src/types.ts`
- Modify: `frontend/src/router.ts`
- Modify: `frontend/src/App.vue`
- Modify: `frontend/src/styles.css`
- Test: `frontend` typecheck/build

- [x] 增加榜单和心跳类型、`/leaderboard` 路由及顶部/移动导航入口。
- [x] 在 App 根组件实现 30 秒可见且聚焦心跳，路由变化更新 surface，登出清理 timer。
- [x] 为页面状态定义桌面表格和移动紧凑布局样式。

### Task 4: 排行榜页面

**Files:**
- Create: `frontend/src/views/LeaderboardView.vue`
- Modify: `frontend/src/styles.css`

- [x] 实现 board/period 切换、前三名、排行表、我的排名、加载/空/错误状态。
- [x] 使用现有 API 和主题 token，保证键盘可操作、移动端不横向溢出。

### Task 5: 验证与回归

- [x] 运行 `cd backend; python -m pytest`。
- [x] 运行 `cd frontend; npm run typecheck; npm run build`。
- [ ] 启动开发服务，用浏览器检查 `/leaderboard` 的桌面/移动布局、切换、空榜和错误状态。（Playwright 浏览器下载被远端中断）
- [x] 检查 `git diff`，确认仅包含本功能相关文件。
