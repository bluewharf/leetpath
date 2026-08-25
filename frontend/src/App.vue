<template>
  <div>
    <header class="topbar" v-if="auth.me">
      <RouterLink class="brand" to="/">leet<span class="path">path</span></RouterLink>
      <nav>
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
          class="lang-toggle-btn"
          :title="aiStore.isConfigured.value ? `当前 AI: ${aiStore.selectedModel.value}（点击设置）` : '点击配置自定义 AI 密钥与模型'"
          @click="showAiSettings = true"
        >
          <span class="lang-text">🤖 {{ aiStore.isConfigured.value ? (aiStore.selectedModel.value.length > 10 ? aiStore.selectedModel.value.slice(0, 8) + '..' : aiStore.selectedModel.value) : 'AI 设置' }}</span>
        </button>

        <!-- 全局语言偏好切换 -->
        <button
          class="lang-toggle-btn"
          :title="langPref === 'python3' ? '当前全局语言: Python 3（点击切换到 C++）' : '当前全局语言: C++（点击切换到 Python 3）'"
          @click="toggleLang"
        >
          <span class="lang-text mono">{{ langPref === 'python3' ? 'Python3' : 'C++' }}</span>
        </button>

        <!-- 全站字号自由调节 -->
        <button
          class="font-size-btn"
          :title="fontSizeTooltip"
          @click="cycleFontSize"
        >
          <span>aA</span>
          <span class="font-label">{{ fontSizeLabel }}</span>
        </button>

        <!-- 三态主题切换：浅色 ➔ 深色 ➔ 赛博霓虹 -->
        <button
          class="theme-btn"
          :title="themeTooltip"
          @click="onToggleTheme"
        >
          {{ themeIcon }}
        </button>
        <span class="avatar">{{ auth.me.username.slice(0, 1).toUpperCase() }}</span>
        <span class="username">{{ auth.me.username }}</span>
        <button class="btn btn-sm" @click="onLogout">退出</button>
      </div>
    </header>

    <RouterView />
    <Toast />
    <AiSettingsModal v-if="showAiSettings" @close="showAiSettings = false" />

    <nav class="bottom-tabs" v-if="auth.me">
      <RouterLink to="/" exact-active-class="active">
        <span class="tab-icon">⌂</span>首页
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
import { computed, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import AiSettingsModal from './components/AiSettingsModal.vue'
import Toast from './components/Toast.vue'
import { useAiStore } from './stores/ai'
import { useAuthStore } from './stores/auth'
import { useFontSize, useLangPref } from './stores/pref'
import { getTheme, toggleTheme, type Theme } from './theme'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()
const aiStore = useAiStore()
const showAiSettings = ref(false)
const { langPref, toggleLang } = useLangPref()
const { fontSize, cycleFontSize } = useFontSize()

const currentTheme = ref<Theme>(getTheme())

const themeIcon = computed(() => {
  if (currentTheme.value === 'light') return '☀'
  if (currentTheme.value === 'dark') return '☾'
  return '🌌'
})

const themeTooltip = computed(() => {
  if (currentTheme.value === 'light') return '当前：极简冷白（点击切换为黑曜石深色）'
  if (currentTheme.value === 'dark') return '当前：黑曜石深色（点击切换为赛博极客霓虹）'
  return '当前：赛博极客霓虹（点击切换为极简冷白）'
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

async function onLogout() {
  await auth.logout()
  router.push('/login')
}
</script>
