# 排行榜设计

## 目标

为登录用户提供三套相互独立的排行榜：算法题完成数榜、八股答题完成数榜、活跃学习时长榜。每套榜单支持今日、当周和历史总榜，并返回当前用户自己的排名。

## 统计口径

- 时区固定为 `Asia/Shanghai`，日界线为本地自然日 00:00；周界线为周一 00:00。
- 算法题完成数按用户在时间窗口内首次获得 AC 的不同 `Problem` 数量统计。历史总榜按曾经 AC 的不同题数量统计。仅统计 `Problem.source` 为 `hot100` 或 `mianjing` 的已发布题目。
- 八股完成数按用户在时间窗口内首次答对的不同 `QuizQuestion` 数量统计；历史总榜按曾经答对的不同题数量统计。答错、重复答对不增加完成数。
- 活跃学习时长按服务端接受的活动会话秒数统计，覆盖题目、八股、背题、手册和岗位页面。仅统计前台且可见页面发出的心跳；服务端将单次心跳增量限制为 60 秒、单日总时长限制为 8 小时，并按用户/会话去重。
- 榜单排序为指标降序；同值按更早达到该指标的时间升序，再按用户名升序。返回前 50 名及当前用户行（若不在前 50）。

## 数据模型

- `Submission.judged_at`：判题 worker 写入最终状态的 UTC 时间，用于准确识别 AC 发生时间。
- `QuizSolveEvent`：记录每次用户首次答对某道八股题的时间，唯一键为 `(user_id, question_id)`，避免重复答对刷榜。
- `StudySession`：记录用户会话的 `session_id`、页面 `surface`、最近心跳时间、累计秒数、自然日。心跳更新采用幂等的 `(session_id, heartbeat_at)` 窗口，拒绝倒退时间和超额增量。

## API

### `GET /api/leaderboard`

查询参数：

- `board`: `problems`、`quiz`、`duration`，默认 `problems`
- `period`: `today`、`week`、`all`，默认 `today`

响应：

```json
{
  "board": "problems",
  "period": "today",
  "timezone": "Asia/Shanghai",
  "metric": "solved_count",
  "me": {"rank": 3, "username": "alice", "value": 8},
  "entries": [
    {"rank": 1, "username": "bob", "value": 12, "is_me": false}
  ]
}
```

`value` 对题数为整数，对时长为秒数。未登录访问返回 401；参数非法返回 422。

### `POST /api/activity/heartbeat`

请求体：`{"session_id":"uuid", "surface":"problem", "elapsed_seconds":30}`。

`surface` 取 `problem`、`quiz`、`review`、`handbook`、`jobs`；`elapsed_seconds` 必须为 1-60 的整数。服务端按当天上限截断并返回 `{"accepted_seconds": 30, "daily_seconds": 120}`。

## 前端行为

- 新增 `/leaderboard` 页面，提供榜单类型和周期切换、前三名突出展示、表格列表、我的排名和加载/空/错误状态。
- 顶部导航和移动底部导航增加“排行榜”入口。
- `App.vue` 挂载全局活跃计时器：登录后在页面可见且窗口有焦点时，每 30 秒发送一次心跳；路由或页面失焦时停止；每次登录生成新的 `session_id`。
- 视觉沿用现有 token，不新增大面积装饰；表格在移动端改为紧凑行布局，保持用户名和值不溢出。

## 迁移与兼容

- SQLite 通过 `ensure_schema` 为旧库补充 `submissions.judged_at`，新表由 `create_all` 创建。
- 旧提交没有 `judged_at` 时，历史总榜仍可使用状态数据；日/周榜只统计有 `judged_at` 的 AC 记录，避免把提交时间误认为完成时间。
- 旧八股记录不回填 `QuizSolveEvent`，因此八股榜从功能上线后开始累计。
