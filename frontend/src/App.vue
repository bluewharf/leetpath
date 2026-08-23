<template>
  <div>
    <header class="topbar" v-if="auth.me">
      <RouterLink class="brand" to="/">leet<span class="path">path</span></RouterLink>
      <nav>
        <RouterLink to="/problems" :class="{ active: route.path.startsWith('/problems') }">题库</RouterLink>
        <RouterLink to="/review" :class="{ active: route.path === '/review' }">背题</RouterLink>
        <RouterLink to="/jobs" :class="{ active: route.path === '/jobs' }">校招看板</RouterLink>
        <RouterLink to="/links" :class="{ active: route.path === '/links' }">八股笔记</RouterLink>
        <RouterLink v-if="auth.me.is_admin" to="/admin" :class="{ active: route.path === '/admin' }">管理</RouterLink>
      </nav>
      <div class="user">
        <button class="theme-btn" :title="isDark ? '切换到浅色' : '切换到深色'" @click="onToggleTheme">
          {{ isDark ? '☾' : '☀' }}
        </button>
        <span class="avatar">{{ auth.me.username.slice(0, 1).toUpperCase() }}</span>
        <span class="username">{{ auth.me.username }}</span>
        <button class="btn btn-sm" @click="onLogout">退出</button>
      </div>
    </header>

    <RouterView />

    <nav class="bottom-tabs" v-if="auth.me">
      <RouterLink to="/" exact-active-class="active">
        <span class="tab-icon">⌂</span>首页
      </RouterLink>
      <RouterLink to="/problems" :class="{ active: route.path.startsWith('/problems') }">
        <span class="tab-icon">≡</span>题库
      </RouterLink>
      <RouterLink to="/review" :class="{ active: route.path === '/review' }">
        <span class="tab-icon">✦</span>背题
      </RouterLink>
      <RouterLink to="/jobs" :class="{ active: route.path === '/jobs' }">
        <span class="tab-icon">▦</span>看板
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
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from './stores/auth'
import { getTheme, toggleTheme } from './theme'

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const isDark = ref(getTheme() === 'dark')
function onToggleTheme() {
  isDark.value = toggleTheme() === 'dark'
}

async function onLogout() {
  await auth.logout()
  router.push('/login')
}
</script>
