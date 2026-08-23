<template>
  <div class="auth-wrap">
    <div class="card auth-card">
      <div class="brand-big">leet<span class="path">path</span></div>
      <div class="auth-sub">注册账号，开始刷题</div>
      <div v-if="error" class="form-error">{{ error }}</div>
      <form @submit.prevent="onSubmit">
        <div class="field">
          <label>用户名（3-32 位字母/数字/下划线）</label>
          <input v-model="username" class="input" autocomplete="username" required minlength="3" maxlength="32" />
        </div>
        <div class="field">
          <label>邮箱（可选）</label>
          <input v-model="email" class="input" type="email" autocomplete="email" />
        </div>
        <div class="field">
          <label>密码（至少 8 位）</label>
          <input v-model="password" class="input" type="password" autocomplete="new-password" required minlength="8" />
        </div>
        <div class="field">
          <label>确认密码</label>
          <input v-model="confirm" class="input" type="password" autocomplete="new-password" required />
        </div>
        <button class="btn btn-primary" :disabled="loading">{{ loading ? '注册中…' : '注册' }}</button>
      </form>
      <div class="auth-switch">已有账号？<RouterLink to="/login">直接登录</RouterLink></div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const email = ref('')
const password = ref('')
const confirm = ref('')
const error = ref('')
const loading = ref(false)
const auth = useAuthStore()
const router = useRouter()

async function onSubmit() {
  error.value = ''
  if (password.value !== confirm.value) {
    error.value = '两次输入的密码不一致'
    return
  }
  loading.value = true
  try {
    await auth.register(username.value, password.value, email.value)
    router.push('/')
  } catch (e) {
    error.value = e instanceof Error ? e.message : '注册失败'
  } finally {
    loading.value = false
  }
}
</script>
