# leetpath

响应式个人刷题站：力扣热题 100 + 面经高频手撕题库，Python3/C++ 在线评测（Docker 沙箱），草稿入库多端同步，首页校招看板，大模型八股外链小林笔记。

## 技术栈

- 后端：FastAPI + SQLAlchemy 2.x + SQLite(WAL)，JWT cookie 认证（bcrypt）
- 前端：Vue 3 + Vite + TypeScript + CodeMirror 6 + marked/dompurify，「档案刊物」设计系统（暖纸/墨色/朱橙点睛 + 发丝规线 + 微粒噪点，主断点 1023px，宽屏增强 1800px；主题六态：paper 档案朱橙(默认浅)/ink 深夜档案(默认暗)/slate 莫兰迪灰蓝/oat 燕麦拿铁/cyber 赛博霓虹/sepia 豆沙护眼，均定义在 base.css 变量块，paper/ink 大标题用衬线刊头）
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

# 发版（本地）：更新 VERSION 单源并打 git tag
scripts/release.sh 0.3.1 && git push && git push origin v0.3.1

# 升级（服务器）：拉代码、按 VERSION 构建带标签镜像、滚动重启并健康检查
scripts/upgrade.sh
# 回滚：git checkout v<旧版本> && scripts/upgrade.sh
```

## 约定

- 判题协议为 ACM 模式（stdin/stdout），测试用例比对忽略行尾空白与末尾空行；刷题页可切换力扣函数模式，由 worker 套读入 harness 后仍按 ACM 用例评测
- 提交状态：pending / judging / AC / WA / TLE / MLE / CE / RE / IE
- 所有 API 在 `/api` 前缀下，除 `/api/auth/*` 外均需登录
- 前端样式集中在 `frontend/src/styles/`：`base.css`（设计令牌+基础组件，先加载）→ `chrome.css`（桌面报纸刊头 masthead（报头行+规线栏目条+主题菜单）/ 移动端顶栏+Tab Bar）→ `views/*.css`（按页面簇）；入口 `styles/index.css`。颜色一律用 CSS 变量，图标统一用 `components/AppIcon.vue` 内联 SVG
- 主题切换走 `frontend/src/theme.ts`（THEME_LIST 单一来源，含中文名与 dark 标记；旧 light/dark 存储值自动迁移为 paper/ink）；新增主题 = base.css 加变量块 + THEME_LIST 加项 + App.vue `themeDots` 加色点
- 版心宽度：`.container` / `.masthead-inner` 全屏流式（无 max-width），桌面左右 padding 48px、≥1800px 宽屏 64px、≤1023px 20px
- 题面、注释、UI 文案用中文；代码标识符用英文
- 版本号单源为根目录 `VERSION` 文件：后端经 compose 注入 `APP_VERSION`（`/api/health` 返回），前端构建时经 vite define 注入并显示在顶栏；docker 镜像按 `leetpath-backend/frontend:<版本>` 打标签
- 不要提交 `.env`、`data/`、种子数据以外的产物
