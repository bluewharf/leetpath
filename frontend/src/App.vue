<template>
  <div>
    <header class="topbar" v-if="auth.me">
      <RouterLink class="brand" to="/">leet<span class="path">path</span></RouterLink>
      <span class="brand-version" :title="`当前部署版本 v${appVersion}`">v{{ appVersion }}</span>
      <nav>
        <RouterLink to="/leaderboard" :class="{ active: route.path === '/leaderboard' }">排行榜</RouterLink>
        <RouterLink to="/problems" :class="{ active: route.path.startsWith('/problems') }">题库</RouterLink>
        <RouterLink to="/quiz" :class="{ active: route.path.startsWith('/quiz') }">八股刷题</RouterLink>
        <RouterLink to="/review" :class="{ active: route.path === '/review' }">背题</RouterLink>
        <RouterLink to="/handbook" :class="{ active: route.path === '/handbook' }">新手速查</RouterLink>
        <RouterLink to="/jobs" :class="{ active: route.path === '/jobs' }">秋招看板</RouterLink>
        <RouterLink to="/links" :class="{ active: route.path === '/links' }">八股笔记</RouterLink>
        <RouterLink v-if="auth.me.is_admin" to="/admin" :class="{ active: route.path === '/admin' }">管理</RouterLink>
      </nav>
      <div class="user">
        <!-- AI 设置 -->
        <button
          class="lang-toggle-btn ai-settings-btn"
          :title="aiStore.isConfigured.value ? `当前 AI: ${aiStore.selectedModel.value}（点击设置）` : '点击配置自定义 AI 密钥与模型'"
          @click="showAiSettings = true"
        >
          <span class="ai-ico">🤖</span>
          <span class="lang-text">{{ aiStore.isConfigured.value ? (aiStore.selectedModel.value.length > 10 ? aiStore.selectedModel.value.slice(0, 8) + '..' : aiStore.selectedModel.value) : 'AI 设置' }}</span>
        </button>

        <!-- 全局语言偏好切换（移动端隐藏，做题页/背题页内可切） -->
        <button
          class="lang-toggle-btn desktop-only"
          :title="langPref === 'python3' ? '当前全局语言: Python 3（点击切换到 C++）' : '当前全局语言: C++（点击切换到 Python 3）'"
          @click="toggleLang"
        >
          <span class="lang-text mono">{{ langPref === 'python3' ? 'Python3' : 'C++' }}</span>
        </button>

        <!-- 全站字号自由调节（移动端隐藏） -->
        <button
          class="font-size-btn desktop-only"
          :title="fontSizeTooltip"
          @click="cycleFontSize"
        >
          <span>aA</span>
          <span class="font-label">{{ fontSizeLabel }}</span>
        </button>

        <!-- 四态主题切换：浅色 ➔ 深色 ➔ 赛博霓虹 ➔ 豆沙护眼 -->
        <button
          class="theme-btn"
          :title="themeTooltip"
          @click="onToggleTheme"
        >
          {{ themeIcon }}
        </button>
        <RouterLink class="user-chip" to="/settings" title="账号设置：改密与头像">
          <UserAvatar :username="auth.me.username" :avatar-url="auth.me.avatar_url" />
          <span class="username">{{ auth.me.username }}</span>
        </RouterLink>
        <button class="btn btn-sm" @click="onLogout">退出</button>
      </div>
    </header>

    <RouterView />
    <Toast />
    <FloatingAiAssistant />
    <AiSettingsModal v-if="showAiSettings" @close="showAiSettings = false" />
    <LeaderboardPopup v-if="showLeaderboardPopup" @close="showLeaderboardPopup = false" />

    <nav class="bottom-tabs" v-if="auth.me">
      <RouterLink to="/" exact-active-class="active">
        <span class="tab-icon">⌂</span>首页
      </RouterLink>
      <RouterLink to="/leaderboard" :class="{ active: route.path === '/leaderboard' }">
        <span class="tab-icon">♜</span>榜单
      </RouterLink>
      <RouterLink to="/problems" :class="{ active: route.path.startsWith('/problems') }">
        <span class="tab-icon">≡</span>题库
      </RouterLink>
      <RouterLink to="/quiz" :class="{ active: route.path.startsWith('/quiz') }">
        <span class="tab-icon">✎</span>刷八股
      </RouterLink>
      <RouterLink to="/review" :class="{ active: route.path === '/review' }">
        <span class="tab-icon">✦</span>背题
      </RouterLink>
      <RouterLink to="/handbook" :class="{ active: route.path === '/handbook' }">
        <span class="tab-icon">§</span>手册
      </RouterLink>
      <RouterLink to="/jobs" :class="{ active: route.path === '/jobs' }">
        <span class="tab-icon">▦</span>秋招
      </RouterLink>
      <RouterLink to="/links" :class="{ active: route.path === '/links' }">
        <span class="tab-icon">⇱</span>八股
      </RouterLink>
      <RouterLink v-if="auth.me.is_admin" to="/admin" :class="{ active: route.path === '/admin' }">
        <span class="tab-icon">⚙</span>管理
      </RouterLink>
    </nav>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AiSettingsModal from './components/AiSettingsModal.vue'
import FloatingAiAssistant from './components/FloatingAiAssistant.vue'
import LeaderboardPopup from './components/LeaderboardPopup.vue'
import Toast from './components/Toast.vue'
import UserAvatar from './components/UserAvatar.vue'
import { useAiStore } from './stores/ai'
import { useAuthStore } from './stores/auth'
import { useFontSize, useLangPref } from './stores/pref'
import { getTheme, toggleTheme, type Theme } from './theme'
import { api } from './api'
import type { ActivityHeartbeatRequest } from './types'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const aiStore = useAiStore()
const showAiSettings = ref(false)
const showLeaderboardPopup = ref(false)
const leaderboardPopupShown = ref(false)
const { langPref, toggleLang } = useLangPref()
const { fontSize, cycleFontSize } = useFontSize()

// 构建时注入的部署版本号（vite define）
const appVersion = __APP_VERSION__

let heartbeatTimer: number | null = null
let leaderboardPopupTimer: number | null = null
let sessionId = ''
let lastSurface: ActivityHeartbeatRequest['surface'] | null = null

function activeSurface(): ActivityHeartbeatRequest['surface'] | null {
  if (route.path.startsWith('/problems')) return 'problem'
  if (route.path.startsWith('/quiz')) return 'quiz'
  if (route.path === '/review') return 'review'
  if (route.path === '/handbook') return 'handbook'
  if (route.path === '/jobs') return 'jobs'
  return null
}

function stopHeartbeat() {
  if (heartbeatTimer !== null) {
    window.clearInterval(heartbeatTimer)
    heartbeatTimer = null
  }
}

async function sendHeartbeat() {
  const surface = activeSurface()
  if (!auth.me || !surface || document.visibilityState !== 'visible' || !document.hasFocus()) return
  if (!sessionId) sessionId = crypto.randomUUID()
  lastSurface = surface
  try {
    await api.post('/api/activity/heartbeat', {
      session_id: sessionId,
      surface,
      elapsed_seconds: 30,
    } satisfies ActivityHeartbeatRequest)
  } catch {
    // 心跳失败不打断当前学习流程，下一次周期继续尝试。
  }
}

function syncHeartbeat() {
  stopHeartbeat()
  if (!auth.me || !activeSurface()) return
  if (!sessionId || lastSurface !== activeSurface()) sessionId = crypto.randomUUID()
  heartbeatTimer = window.setInterval(sendHeartbeat, 30000)
}

function onActivityVisibilityChange() { syncHeartbeat() }

const currentTheme = ref<Theme>(getTheme())

const themeIcon = computed(() => {
  if (currentTheme.value === 'light') return '☀'
  if (currentTheme.value === 'dark') return '☾'
  if (currentTheme.value === 'cyber') return '🌌'
  return '🍵'
})

const themeTooltip = computed(() => {
  if (currentTheme.value === 'light') return '当前：极简冷白（点击切换为黑曜石深色）'
  if (currentTheme.value === 'dark') return '当前：黑曜石深色（点击切换为赛博极客霓虹）'
  if (currentTheme.value === 'cyber') return '当前：赛博极客霓虹（点击切换为豆沙护眼绿）'
  return '当前：豆沙护眼绿（点击切换为极简冷白）'
})

const fontSizeLabel = computed(() => {
  if (fontSize.value === 'sm') return '小'
  if (fontSize.value === 'lg') return '大'
  return '中'
})

const fontSizeTooltip = computed(() => {
  if (fontSize.value === 'sm') return '当前字号：紧凑小号（点击切换为标准中号）'
  if (fontSize.value === 'md') return '当前字号：标准中号（点击切换为护眼大号）'
  return '当前字号：护眼大号（点击切换为紧凑小号）'
})

function onToggleTheme() {
  currentTheme.value = toggleTheme()
}

watch(() => [auth.me?.id, route.path], syncHeartbeat)
watch(() => [auth.me?.id, route.path], () => {
  if (!auth.me || leaderboardPopupShown.value || route.path === '/settings') return
  leaderboardPopupShown.value = true
  leaderboardPopupTimer = window.setTimeout(() => { showLeaderboardPopup.value = true }, 180)
})
onMounted(() => {
  document.addEventListener('visibilitychange', onActivityVisibilityChange)
  window.addEventListener('focus', syncHeartbeat)
  window.addEventListener('blur', stopHeartbeat)
  syncHeartbeat()
  if (auth.me && !leaderboardPopupShown.value && route.path !== '/settings') {
    leaderboardPopupShown.value = true
    leaderboardPopupTimer = window.setTimeout(() => { showLeaderboardPopup.value = true }, 180)
  }
})
onBeforeUnmount(() => {
  stopHeartbeat()
  if (leaderboardPopupTimer !== null) window.clearTimeout(leaderboardPopupTimer)
  document.removeEventListener('visibilitychange', onActivityVisibilityChange)
  window.removeEventListener('focus', syncHeartbeat)
  window.removeEventListener('blur', stopHeartbeat)
})

async function onLogout() {
  await auth.logout()
  router.push('/login')
}
</script>
