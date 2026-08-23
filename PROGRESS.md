# leetpath 进度表

> 规则：每个任务的负责人在完成（或失败）后更新自己那一行：状态改为 ✅ 完成 / ⚠️ 有问题，并填产物摘要与更新时间。只改自己的行，别动别人的。状态图例：⏳ 未开始 · 🔄 进行中 · ✅ 完成 · ⚠️ 有问题。

| # | 任务 | 负责 | 状态 | 产物/验收 | 更新时间 |
|---|---|---|---|---|---|
| 1 | 规格文档 + 热题100清单 + 种子校验器 | Kimi | ✅ | docs/spec/*、docs/seed/hot100-manifest.md、scripts/validate_seed.py | 2026-08-23 |
| 2 | 后端（FastAPI 全部 API + seed loader + pytest） | grok | ✅ | FastAPI 全路由 + seed loader + links.json；pytest 30 passed | 2026-08-23 23:10 |
| 3 | 判题 worker + 判题镜像（python/cpp） | grok | ✅ | backend/judge/{worker.py,__init__.py,Dockerfile.python,Dockerfile.cpp}；leetpath-judge-python/cpp 构建成功；python stdin 与 cpp hello 冒烟通过 | 2026-08-23 22:53 |
| 4 | 前端 SPA（Vue3 全部页面，响应式） | Kimi | ✅ | vite build + vue-tsc 通过；v4 暖纸设计（陶土橙/衬线标题/手动主题切换）；jobs 396 条已入库 | 2026-08-23 |
| 5 | 种子批次01（题 1-10） | grok | ✅ | 10 题 validate 全 OK；用例数 9/9/9/9/9/9/9/10/9/9 | 2026-08-23 22:50 |
| 6 | 种子批次02（题 11-20） | grok | ✅ | 10 题 validate_seed 全 OK，各 10 组用例 | 2026-08-23 22:48 |
| 7 | 种子批次03（题 21-30） | grok | ✅ | 10 题 validate_seed.py 全 OK，共 81 组用例（8/9/8/8/8/8/8/8/8/8） | 2026-08-23 22:48 |
| 8 | 种子批次04（题 31-40） | grok | ✅ | 10 题 validate 全 OK；用例 8/10/10/10/9/9/9/9/10/9 | 2026-08-23 22:49 |
| 9 | 种子批次05（题 41-50） | grok | ✅ | validate_seed.py 全 OK（用例 9/8/9/8/9/8/8/9/8/9） | 2026-08-23 22:49 |
| 10 | 种子批次06（题 51-60） | grok | ✅ | 10 题 validate_seed.py 全 OK；用例 10/10/10/10/10/10/10/10/8/10 | 2026-08-23 22:50 |
| 11 | 种子批次07（题 61-70） | grok | ✅ | 10 题 validate OK；用例 9/9/9/9/10/9/9/9/10/9 | 2026-08-23 22:47 |
| 12 | 种子批次08（题 71-80） | grok | ✅ | 10 题 validate_seed.py 全 OK，各 10 用例 | 2026-08-23 22:49 |
| 13 | 种子批次09（题 81-90） | grok | ✅ | validate_seed.py 全 OK；用例 8/8/9/8/9/8/8/9/8/9 共 84 | 2026-08-23 22:47 |
| 14 | 种子批次10（题 91-100） | grok | ✅ | validate_seed.py 全 OK；用例 9/9/9/9/9/9/9/9/9/9 共 90 | 2026-08-23 22:49 |
| 15 | 部署配置（compose/nginx/.env/README） | grok | ✅ | docker-compose.yml / deploy/nginx.conf / backend/Dockerfile / .env.example / README.md；compose config -q 通过 | 2026-08-23 23:17 |
| 16 | 端到端验证（pytest / build / 判题六状态） | Kimi | ✅ | pytest 30 passed；前端 typecheck+build 通过；E2E 走真 API：AC/WA/TLE/RE/MLE(python)+AC/CE(cpp) 全 PASS；浏览器截图联调正常 | 2026-08-23 |
| 17 | 背题模式：规格 + 后端（solution_md/ReviewCard/API） | Kimi | ✅ | docs/spec/seed-format.md solution.md 契约；validate_seed.py 题解实测；pytest 32 passed | 2026-08-23 |
| 18 | 题解批次01（3sum ~ combination-sum） | grok | ✅ | 10 题 solution.md（思路+复杂度+Py/C++ ACM 模板），validate_seed 全 OK | 2026-08-24 00:42 |
| 19 | 题解批次02（construct-bt ~ find-all-anagrams） | grok | ✅ | solution.md ×10，validate_seed 全 OK | 2026-08-24 00:43 |
| 20 | 题解批次03（find-first-and-last ~ implement-trie） | grok | ✅ | solution.md ×10，validate_seed 全 OK | 2026-08-24 00:42 |
| 21 | 题解批次04（intersection ~ linked-list-cycle-ii） | grok | ✅ | solution.md ×10，validate_seed 全 OK；用例 9/9/10/10/10/8/10/10/8/8 | 2026-08-24 00:42 |
| 22 | 题解批次05（longest-common-subseq ~ max-depth） | grok | ✅ | solution.md ×10，validate_seed 全 OK | 2026-08-24 00:42 |
| 23 | 题解批次06（max-product-subarray ~ move-zeroes） | grok | ✅ | solution.md ×10，validate_seed 全 OK | 2026-08-24 00:42 |
| 24 | 题解批次07（n-queens ~ perfect-squares） | grok | ✅ | solution.md ×10，validate_seed.py 全 OK | 2026-08-24 00:43 |
| 25 | 题解批次08（permutations ~ search-2d-matrix-ii） | grok | ✅ | solution.md ×10，validate_seed 全 OK（10 题 0 问题） | 2026-08-24 00:41 |
| 26 | 题解批次09（search-rotated ~ subsets） | grok | ✅ | 10 题 solution.md，validate_seed 全 OK；用例 9/9/10/9/10/9/10/10/9/10 | 2026-08-24 00:41 |
| 27 | 题解批次10（swap-nodes ~ word-search） | grok | ✅ | 10 题 solution.md，validate_seed 全 OK（10 题 0 问题） | 2026-08-24 00:42 |
| 28 | 前端：背题模式 + 看板筛选 + jobs 分层 | Kimi | ✅ | /review 卡片翻面 + 记忆打卡；看板按大/中/小厂分组 + 公司/规模/关键词/在招筛选；typecheck+build 通过；全量 100 题题解校验 0 问题并已入库 | 2026-08-24 |
| 29 | 前端 UI/UX 体验全方位升级 + 秋招公司聚合看板 + 算法新手速查手册 | Antigravity | ✅ | KaTeX 数学公式渲染；分栏拖拽/计时器/快捷键/题解Tab/代码回填；秋招公司聚合折叠+个人投递追踪；算法新手手册(/handbook)；年度打卡热力图+骨架屏+Toast；vue-tsc+build 0 报错通过 | 2026-08-24 |

