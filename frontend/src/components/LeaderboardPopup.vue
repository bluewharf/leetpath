<template>
  <div class="leaderboard-popup-backdrop" role="presentation" @click.self="close">
    <section class="leaderboard-popup" role="dialog" aria-modal="true" aria-labelledby="leaderboard-popup-title">
      <button class="leaderboard-popup-close" type="button" aria-label="关闭排行榜弹窗" title="关闭" @click="close">×</button>
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

<style scoped>
.leaderboard-popup-backdrop { position:fixed; inset:0; z-index:1000; display:grid; place-items:center; padding:20px; background:rgb(15 23 42 / 48%); backdrop-filter:blur(4px); }
.leaderboard-popup { position:relative; width:min(440px, 100%); padding:28px; border:1px solid var(--border-strong); border-radius:10px; background:var(--surface); box-shadow:0 24px 80px rgb(15 23 42 / 28%); }
.leaderboard-popup-close { position:absolute; top:12px; right:14px; width:32px; height:32px; border:0; border-radius:6px; background:transparent; color:var(--text-dim); font-size:25px; line-height:1; cursor:pointer; }.leaderboard-popup-close:hover { background:var(--surface-2); color:var(--text); }
.leaderboard-popup h2 { margin:4px 0 4px; font-size:26px; }.leaderboard-popup-subtitle { margin:0 0 20px; color:var(--text-dim); font-size:14px; }
.leaderboard-popup-list { display:grid; gap:8px; padding:0; margin:0 0 22px; list-style:none; }.leaderboard-popup-list li { display:flex; align-items:center; gap:12px; padding:11px 12px; border:1px solid var(--border); border-radius:7px; background:var(--surface-2); }.leaderboard-popup-list li.mine { border-color:var(--accent); background:color-mix(in srgb,var(--accent) 9%,var(--surface-2)); }.leaderboard-popup-rank { width:22px; color:var(--accent); font-weight:800; text-align:center; }.leaderboard-popup-user { flex:1; min-width:0; overflow:hidden; text-overflow:ellipsis; white-space:nowrap; }.leaderboard-popup-user small { margin-left:7px; color:var(--accent); }.leaderboard-popup-list strong { white-space:nowrap; }.leaderboard-popup-state { min-height:92px; display:grid; place-items:center; color:var(--text-dim); text-align:center; }
.leaderboard-popup-actions { display:flex; justify-content:flex-end; gap:8px; flex-wrap:wrap; }.leaderboard-popup-actions .btn { flex:1; min-width:130px; }
@media (max-width:480px) { .leaderboard-popup { padding:24px 18px 18px; }.leaderboard-popup h2 { font-size:22px; }.leaderboard-popup-actions { display:grid; grid-template-columns:1fr; }.leaderboard-popup-actions .btn { width:100%; } }
</style>
