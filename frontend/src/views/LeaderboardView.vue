<template>
  <main class="container leaderboard-page">
    <div class="page-head">
      <div>
        <p class="eyebrow">LEETPATH / RANKINGS</p>
        <h1>排行榜</h1>
        <p class="muted">按自然日统计，时区：{{ data?.timezone || 'Asia/Shanghai' }}</p>
      </div>
      <button class="btn btn-ghost" type="button" :disabled="loading" @click="load">刷新</button>
    </div>

    <div class="leaderboard-controls" role="group" aria-label="排行榜筛选">
      <div class="segmented">
        <button v-for="item in boards" :key="item.value" type="button" :class="{ active: board === item.value }" @click="selectBoard(item.value)">{{ item.label }}</button>
      </div>
      <div class="segmented">
        <button v-for="item in periods" :key="item.value" type="button" :class="{ active: period === item.value }" @click="selectPeriod(item.value)">{{ item.label }}</button>
      </div>
    </div>

    <section v-if="data?.me" class="leaderboard-me" aria-live="polite">
      <span>我的排名</span>
      <strong>{{ data.me.rank ? `第 ${data.me.rank} 名` : '暂未上榜' }}</strong>
      <span class="leaderboard-me-value">{{ formatValue(data.me.value) }}</span>
    </section>

    <p v-if="loading" class="state-message">正在加载榜单…</p>
    <p v-else-if="error" class="error-banner">{{ error }} <button class="btn btn-sm" type="button" @click="load">重试</button></p>
    <section v-else-if="!data?.entries.length" class="empty-state">
      <h2>还没有榜单记录</h2>
      <p>完成一道题或开始一段学习，今天的排名就会出现在这里。</p>
    </section>
    <section v-else class="leaderboard-table-wrap">
      <div class="leaderboard-podium" aria-label="前三名">
        <div v-for="entry in data.entries.slice(0, 3)" :key="entry.rank" class="podium-item" :class="`podium-${entry.rank}`">
          <span class="podium-rank">{{ entry.rank }}</span>
          <UserAvatar :username="entry.username" :avatar-url="entry.avatar_url" />
          <strong>{{ entry.username }}</strong>
          <span>{{ formatValue(entry.value) }}</span>
        </div>
      </div>
      <table class="leaderboard-table">
        <thead><tr><th scope="col">排名</th><th scope="col">用户</th><th scope="col">{{ metricLabel }}</th></tr></thead>
        <tbody>
          <tr v-for="entry in data.entries" :key="`${entry.rank}-${entry.username}`" :class="{ mine: entry.is_me }">
            <td>{{ entry.rank }}</td>
            <td class="leaderboard-user-cell">
              <UserAvatar :username="entry.username" :avatar-url="entry.avatar_url" />
              {{ entry.username }}<span v-if="entry.is_me" class="mine-label">我</span>
            </td>
            <td>{{ formatValue(entry.value) }}</td>
          </tr>
        </tbody>
      </table>
    </section>
  </main>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { api } from '../api'
import UserAvatar from '../components/UserAvatar.vue'
import type { LeaderboardBoard, LeaderboardPeriod, LeaderboardResponse } from '../types'

const boards: { value: LeaderboardBoard; label: string }[] = [
  { value: 'problems', label: '算法题完成' },
  { value: 'quiz', label: '八股完成' },
  { value: 'duration', label: '活跃时长' },
]
const periods: { value: LeaderboardPeriod; label: string }[] = [
  { value: 'today', label: '今日' },
  { value: 'week', label: '本周' },
  { value: 'all', label: '历史总榜' },
]
const board = ref<LeaderboardBoard>('problems')
const period = ref<LeaderboardPeriod>('today')
const data = ref<LeaderboardResponse | null>(null)
const loading = ref(false)
const error = ref('')

const metricLabel = computed(() => board.value === 'duration' ? '活跃时长' : '完成数')
function formatValue(value: number): string {
  if (board.value !== 'duration') return `${value} 题`
  const hours = Math.floor(value / 3600)
  const minutes = Math.floor((value % 3600) / 60)
  return hours ? `${hours} 小时 ${minutes} 分` : `${minutes} 分钟`
}
async function load() {
  loading.value = true
  error.value = ''
  try {
    data.value = await api.get<LeaderboardResponse>(`/api/leaderboard?board=${board.value}&period=${period.value}`)
  } catch (e) {
    error.value = e instanceof Error ? e.message : '榜单加载失败'
  } finally { loading.value = false }
}
function selectBoard(value: LeaderboardBoard) { board.value = value; load() }
function selectPeriod(value: LeaderboardPeriod) { period.value = value; load() }
onMounted(load)
</script>

<style scoped>
.leaderboard-page { max-width: 1080px; }
.leaderboard-controls { display:flex; justify-content:space-between; gap:16px; margin:24px 0; flex-wrap:wrap; }
.segmented { display:flex; gap:4px; padding:4px; background:var(--surface-2); border:1px solid var(--border); border-radius:8px; }
.segmented button { border:0; background:transparent; color:var(--muted); padding:8px 14px; border-radius:5px; cursor:pointer; font:inherit; }
.segmented button.active { background:var(--surface); color:var(--text); box-shadow:0 1px 3px rgb(0 0 0 / 12%); }
.leaderboard-me { display:flex; align-items:center; gap:14px; padding:14px 16px; margin-bottom:20px; border-left:3px solid var(--accent); background:var(--surface-2); }
.leaderboard-me strong { margin-left:auto; }.leaderboard-me-value { color:var(--accent); font-weight:700; }
.leaderboard-podium { display:grid; grid-template-columns:repeat(3,1fr); gap:12px; margin-bottom:18px; }
.podium-item { display:flex; flex-direction:column; gap:5px; padding:18px; background:var(--surface-2); border:1px solid var(--border); border-radius:8px; }.podium-rank { color:var(--accent); font-size:24px; font-weight:800; }.podium-item span:last-child { color:var(--muted); }
.leaderboard-table-wrap { overflow:hidden; border:1px solid var(--border); border-radius:8px; background:var(--surface); }.leaderboard-table { width:100%; border-collapse:collapse; }.leaderboard-table th,.leaderboard-table td { text-align:left; padding:13px 16px; border-bottom:1px solid var(--border); }.leaderboard-table th:last-child,.leaderboard-table td:last-child { text-align:right; }.leaderboard-table tbody tr:last-child td { border-bottom:0; }.leaderboard-table tr.mine { background:color-mix(in srgb,var(--accent) 10%,transparent); }.mine-label { margin-left:8px; color:var(--accent); font-size:12px; }
.leaderboard-user-cell { display:flex; align-items:center; gap:8px; }
.state-message,.empty-state { padding:56px 20px; text-align:center; color:var(--muted); }.empty-state h2 { color:var(--text); font-size:20px; }
@media (max-width: 640px) { .leaderboard-controls { display:block; }.segmented { width:100%; margin-bottom:8px; }.segmented button { flex:1; padding-inline:6px; font-size:13px; }.leaderboard-podium { gap:6px; }.podium-item { padding:12px 9px; font-size:13px; overflow:hidden; }.podium-item strong { overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }.leaderboard-table th,.leaderboard-table td { padding:11px 10px; font-size:13px; }.leaderboard-me { gap:8px; font-size:13px; }.leaderboard-me strong { margin-left:auto; } }
</style>
