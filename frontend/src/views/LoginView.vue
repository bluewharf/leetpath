<template>
  <div class="auth-wrap">
    <div class="card auth-card">
      <div class="brand-big">leet<span class="path">path</span></div>
      <div class="auth-sub">登录后继续刷题，草稿自动同步</div>
      <div v-if="error" class="form-error">{{ error }}</div>
      <form @submit.prevent="onSubmit">
        <div class="field">
          <label>用户名</label>
          <input v-model="username" class="input" autocomplete="username" required />
        </div>
        <div class="field">
          <label>密码</label>
          <input v-model="password" class="input" type="password" autocomplete="current-password" required />
        </div>
        <button class="btn btn-primary" :disabled="loading">{{ loading ? '登录中…' : '登录' }}</button>
      </form>
      <div class="auth-switch">还没有账号？<RouterLink to="/register">注册一个</RouterLink></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

async function onSubmit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(username.value, password.value)
    router.push((route.query.redirect as string) || '/')
  } catch (e) {
    error.value = e instanceof Error ? e.message : '登录失败'
  } finally {
    loading.value = false
  }
}
</script>
