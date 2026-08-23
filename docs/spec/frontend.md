# 前端规格（`frontend/`）

## 技术栈

- Vite + Vue 3 + TypeScript + vue-router + pinia。
- 代码编辑器：CodeMirror 6（`codemirror`、`@codemirror/lang-python`、`@codemirror/lang-cpp`、`@codemirror/theme-one-dark`）。
- Markdown：`marked` + `dompurify`（渲染 statement_md，必须 sanitize）。
- 不引 UI 组件库；手写 CSS，CSS 变量做主题，跟随 `prefers-color-scheme`。
- `vite.config.ts`：`server.proxy = { '/api': 'http://localhost:8000' }`。

## 全局

- `src/api.ts`：`api<T>(path, options?)` 封装 fetch：`credentials: 'include'`、JSON body/响应、非 2xx 抛出 `{status, message}`（取 detail 字段）；401 时若当前不在 /login|/register 则跳转 /login。
- `src/stores/auth.ts`（pinia）：`me`、`loaded`；`fetchMe()`、`login()`、`register()`、`logout()`；路由守卫：除 /login、/register 外都要求已登录（未加载先 fetchMe）。
- 顶栏：站点名 leetpath、导航（题库 / 看板 / 八股）、右侧用户名+退出。移动端折叠为底部 tab 或汉堡菜单（实现任选，要求手机上可用）。
- 提交状态颜色：AC 绿、WA 红、TLE/MLE 橙、CE/RE/IE 紫灰、pending/judging 蓝。做一个 `StatusBadge.vue`。

## 路由与页面

| 路径 | 组件 | 说明 |
|---|---|---|
| `/` | HomeView | 校招看板（复用 JobBoard 组件）+ 两个入口卡片（去刷题 / 八股笔记） |
| `/login` `/register` | LoginView / RegisterView | 表单 + 错误提示；成功后回 `/`；页脚互相跳转链接 |
| `/problems` | ProblemListView | 筛选（难度/来源 hot100·面经/标签）+ 搜索框；表格列：状态(✓做过/●尝试过)、标题、难度、来源、标签；点击进入刷题页；移动端卡片式列表 |
| `/problems/:slug` | ProblemView | 核心刷题页，见下 |
| `/jobs` | JobsView | 完整看板页（首页嵌入同一组件） |
| `/links` | LinksView | 按 category 分组的卡片链接，外链 `target="_blank" rel="noopener"` |
| `/admin` | AdminView | 仅 is_admin：两个 tab（题目管理：上下架开关 + 重新导入种子按钮；看板管理：job 增删改表单） |

## ProblemView（刷题页）

- 布局：≥1024px 左右双栏（左题面可滚动，右编辑器+结果）；<1024px 顶部三个 tab：`题面 | 代码 | 结果`。
- 题面：渲染 statement_md（含输入/输出格式、样例、提示）；样例展示 input/expected 代码块。
- 编辑器 `Editor.vue`：CodeMirror，行号、4 空格缩进、语言随选择切换（python3/cpp）、主题跟随系统深浅色；字号移动端 ≥14px 防 iOS 缩放。
- 语言切换下拉：`Python3` / `C++`。切换时保存当前草稿、加载目标语言草稿。
- **草稿**：编辑器内容变化防抖 1000ms → `PUT /api/drafts/{slug}`；状态栏显示`已保存 HH:mm:ss`或`保存中…`。进入页面 `GET /api/drafts/{slug}?language=` 恢复。
- **提交**：按钮`提交评测`→ `POST /api/submissions`；之后按钮禁用并每 800ms 轮询 `GET /api/submissions/{id}`（终态或 90s 超时停止）。
- **结果面板**：状态大徽章 + 总耗时；逐用例列表（`#1 样例 AC 12ms`）；样例用例可展开看 输入/期望/你的输出；CE 展示 compile_output 代码块。隐藏用例只显示状态。
- 历史：题面 tab 内底部"我的提交"列表（`GET /api/submissions?problem_slug=`），点开展示 code（只读 CodeMirror 或 pre）。

## 看板 `JobBoard.vue`

- 卡片：公司、岗位、batch 徽标、截止时间（D-n 形式，≤7 天红色高亮，已截止置灰）、JD 可折叠展开、`投递入口` 外链按钮。
- 排序：服务端已排好；组件不做额外排序。
- 空态文案`暂无岗位，等管理员录入`。

## 构建

`npm run build` 产物 `dist/`；`npm run typecheck`（vue-tsc）必须通过。Dockerfile：node:22 build → nginx:alpine 托管（nginx 配置由仓库 `deploy/nginx.conf` 提供，SPA history fallback + /api 反代）。
