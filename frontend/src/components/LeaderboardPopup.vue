<template>
  <div class="leaderboard-popup-backdrop" role="presentation" @click.self="close">
    <section class="leaderboard-popup" role="dialog" aria-modal="true" aria-labelledby="leaderboard-popup-title">
      <button class="leaderboard-popup-close" type="button" aria-label="关闭排行榜弹窗" title="关闭" @click="close"><AppIcon name="x" :size="15" /></button>
      <p class="eyebrow">DAILY RANKING</p>
      <h2 id="leaderboard-popup-title">今日排行榜</h2>
      <p class="leaderboard-popup-subtitle">看看今天谁在持续前进</p>

      <div v-if="loading" class="leaderboard-popup-state">正在加载今日榜单…</div>
      <div v-else-if="error" class="leaderboard-popup-state">{{ error }}</div>
      <div v-else-if="entries.length === 0" class="leaderboard-popup-state">今天还没有榜单记录，完成一道题就能上榜。</div>
      <ol v-else class="leaderboard-popup-list">
        <li v-for="entry in entries" :key="`${entry.rank}-${entry.username}`" :class="{ mine: entry.is_me }">
          <span class="leaderboard-popup-rank">{{ entry.rank }}</span>
          <UserAvatar :username="entry.username" :avatar-url="entry.avatar_url" />
          <span class="leaderboard-popup-user">{{ entry.username }}<small v-if="entry.is_me">我</small></span>
          <strong>{{ entry.value }} 题</strong>
        </li>
      </ol>

      <div class="leaderboard-popup-actions">
        <RouterLink class="btn btn-primary" to="/leaderboard" @click="close">查看完整榜单</RouterLink>
        <button class="btn btn-ghost" type="button" @click="close">稍后再看</button>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import { onBeforeUnmount, onMounted, ref } from 'vue'
import { api } from '../api'
import UserAvatar from './UserAvatar.vue'
import AppIcon from './AppIcon.vue'
import type { LeaderboardEntry, LeaderboardResponse } from '../types'

const emit = defineEmits<{ close: [] }>()
const entries = ref<LeaderboardEntry[]>([])
const loading = ref(true)
const error = ref('')
let previousOverflow = ''

function close() { emit('close') }
function onKeydown(event: KeyboardEvent) {
  if (event.key === 'Escape') close()
}

onMounted(async () => {
  previousOverflow = document.body.style.overflow
  document.body.style.overflow = 'hidden'
  window.addEventListener('keydown', onKeydown)
  try {
    const response = await api.get<LeaderboardResponse>('/api/leaderboard?board=problems&period=today')
    entries.value = response.entries.slice(0, 3)
  } catch (err) {
    error.value = err instanceof Error ? err.message : '今日榜单暂时不可用'
  } finally {
    loading.value = false
  }
})
onBeforeUnmount(() => {
  window.removeEventListener('keydown', onKeydown)
  document.body.style.overflow = previousOverflow
})
</script>
