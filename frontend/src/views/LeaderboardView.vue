<template>
  <main class="container leaderboard-page">
    <div class="page-head">
      <div>
        <p class="eyebrow">LEETPATH / RANKINGS</p>
        <h1 class="display">排行榜</h1>
        <p class="muted">按自然日统计，时区：{{ data?.timezone || 'Asia/Shanghai' }}</p>
      </div>
      <button class="btn btn-ghost" type="button" :disabled="loading" @click="load"><AppIcon name="refresh" :size="14" /> 刷新</button>
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
          <span class="podium-rank"><AppIcon v-if="entry.rank === 1" name="trophy" :size="18" class="podium-trophy" />{{ entry.rank }}</span>
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
import AppIcon from '../components/AppIcon.vue'
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
