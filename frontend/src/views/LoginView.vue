<template>
  <div class="auth-page">
    <!-- 背景流光与微粒光晕 -->
    <div class="auth-ambient-glow glow-1"></div>
    <div class="auth-ambient-glow glow-2"></div>

    <div class="auth-container">
      <!-- 左侧品牌与特性看板 -->
      <div class="auth-hero">
        <div class="auth-hero-brand">
          <span class="brand-logo">leet<span class="path">path</span></span>
          <span class="brand-badge">2026 校招高频冲刺站</span>
        </div>

        <h1 class="auth-hero-title">
          专为大模型算法与研发工程师打造的<br />
          <span class="gradient-text">沉浸式智能刷题平台</span>
        </h1>

        <p class="auth-hero-desc">
          登录后继续你的刷题进度，代码草稿与错题斩题本多端实时同步，随时唤起 AI 导师答疑拆解。
        </p>

        <!-- 平台四大核心特性卡片 -->
        <div class="hero-features-grid">
          <div class="hero-feat-item">
            <div class="feat-icon">🎯</div>
            <div class="feat-info">
              <h4>热题 100 + 面经手撕</h4>
              <p>Python 3 / C++ ACM 模式沙箱秒级评测</p>
            </div>
          </div>

          <div class="hero-feat-item">
            <div class="feat-icon">📝</div>
            <div class="feat-info">
              <h4>726 道八股客观题</h4>
              <p>34 个大模型核心专题，错题本与斩题模式</p>
            </div>
          </div>

          <div class="hero-feat-item">
            <div class="feat-icon">🤖</div>
            <div class="feat-info">
              <h4>场景化 AI 导师</h4>
              <p>自带 Key / 中转，流式考点拆解与代码找茬</p>
            </div>
          </div>

          <div class="hero-feat-item">
            <div class="feat-icon">💼</div>
            <div class="feat-info">
              <h4>秋招提前批看板</h4>
              <p>大厂投递日程、面试状态与草稿多端同步</p>
            </div>
          </div>
        </div>

        <div class="auth-hero-footer">
          <span>⚡ 基于 FastAPI + Vue 3 + Docker 构建 · 纯净高效</span>
        </div>
      </div>

      <!-- 右侧登录表单卡片 -->
      <div class="auth-form-side">
        <div class="auth-glass-card">
          <!-- 切换选项卡 -->
          <div class="auth-tab-switch">
            <RouterLink to="/login" class="tab-item active">登录账号</RouterLink>
            <RouterLink to="/register" class="tab-item">注册新账号</RouterLink>
          </div>

          <div class="auth-card-header">
            <h2>欢迎回来</h2>
            <p>输入你的用户名与密码继续刷题之旅</p>
          </div>

          <!-- 错误提示横幅 -->
          <transition name="fade">
            <div v-if="error" class="auth-err-banner">
              <span class="err-icon">⚠️</span>
              <span>{{ error }}</span>
            </div>
          </transition>

          <form class="auth-form" @submit.prevent="onSubmit">
            <!-- 用户名 -->
            <div class="form-item">
              <label class="form-label">
                <span>用户名</span>
              </label>
              <div class="input-wrap">
                <span class="input-icon">👤</span>
                <input
                  v-model="username"
                  class="modern-input"
                  placeholder="输入注册用户名"
                  autocomplete="username"
                  required
                />
              </div>
            </div>

            <!-- 密码 -->
            <div class="form-item">
              <label class="form-label">
                <span>账号密码</span>
              </label>
              <div class="input-wrap">
                <span class="input-icon">🔒</span>
                <input
                  v-model="password"
                  class="modern-input"
                  :type="showPwd ? 'text' : 'password'"
                  placeholder="输入密码"
                  autocomplete="current-password"
                  required
                />
                <button
                  type="button"
                  class="pwd-toggle-btn"
                  @click="showPwd = !showPwd"
                >
                  {{ showPwd ? '🙈' : '👁️' }}
                </button>
              </div>
            </div>

            <!-- 登录按钮 -->
            <button class="submit-btn" :disabled="loading">
              <span v-if="loading" class="btn-spinner"></span>
              <span>{{ loading ? '正在验证登录…' : '立即登录 →' }}</span>
            </button>
          </form>

          <div class="auth-card-footer">
            <span>还没有账号？</span>
            <RouterLink to="/register" class="link-highlight">注册一个新账号</RouterLink>
          </div>
        </div>
      </div>
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
const showPwd = ref(false)

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
    error.value = e instanceof Error ? e.message : '用户名或密码错误'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 20px;
  position: relative;
  overflow: hidden;
  background: var(--bg);
}

/* 优雅的环境光晕背景 */
.auth-ambient-glow {
  position: absolute;
  width: 500px;
  height: 500px;
  border-radius: 50%;
  filter: blur(120px);
  pointer-events: none;
  opacity: 0.15;
}

.glow-1 {
  top: -100px;
  left: 10%;
  background: var(--accent);
}

.glow-2 {
  bottom: -100px;
  right: 10%;
  background: #3b82f6;
}

.auth-container {
  width: 100%;
  max-width: 1120px;
  display: grid;
  grid-template-columns: 1.15fr 0.85fr;
  gap: 48px;
  align-items: center;
  position: relative;
  z-index: 10;
}

/* 左侧 Hero 品牌区 */
.auth-hero {
  padding: 20px 0;
}

.auth-hero-brand {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 20px;
}

.brand-logo {
  font-size: 28px;
  font-weight: 900;
  letter-spacing: -0.04em;
  color: var(--text);
}

.brand-logo .path {
  color: var(--accent);
}

.brand-badge {
  font-size: 12px;
  padding: 3px 8px;
  border-radius: 12px;
  background: rgba(var(--accent-rgb, 99, 102, 241), 0.12);
  color: var(--accent);
  border: 1px solid rgba(var(--accent-rgb, 99, 102, 241), 0.3);
}

.auth-hero-title {
  font-size: 32px;
  line-height: 1.35;
  font-weight: 800;
  margin-bottom: 16px;
  color: var(--text);
}

.gradient-text {
  background: linear-gradient(135deg, var(--accent) 0%, #38bdf8 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.auth-hero-desc {
  font-size: 15px;
  line-height: 1.6;
  color: var(--text-dim);
  margin-bottom: 32px;
  max-width: 520px;
}

.hero-features-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 16px;
  margin-bottom: 36px;
}

.hero-feat-item {
  display: flex;
  gap: 12px;
  padding: 14px;
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border);
  border-radius: 10px;
  backdrop-filter: blur(8px);
}

.feat-icon {
  font-size: 24px;
  flex-shrink: 0;
}

.feat-info h4 {
  font-size: 14px;
  margin: 0 0 4px;
  font-weight: 650;
  color: var(--text);
}

.feat-info p {
  font-size: 12px;
  margin: 0;
  color: var(--text-dim);
  line-height: 1.4;
}

.auth-hero-footer {
  font-size: 12px;
  color: var(--text-faint);
}

/* 右侧毛玻璃卡片 */
.auth-form-side {
  width: 100%;
}

.auth-glass-card {
  background: var(--bg-card, rgba(23, 23, 27, 0.7));
  border: 1px solid var(--border);
  backdrop-filter: blur(16px);
  border-radius: 16px;
  padding: 36px 32px;
  box-shadow: 0 20px 50px rgba(0, 0, 0, 0.35);
}

/* 顶部 Tab 切换 */
.auth-tab-switch {
  display: flex;
  background: rgba(255, 255, 255, 0.04);
  border-radius: 8px;
  padding: 4px;
  margin-bottom: 24px;
  border: 1px solid var(--border);
}

.tab-item {
  flex: 1;
  text-align: center;
  padding: 8px;
  font-size: 13px;
  font-weight: 600;
  border-radius: 6px;
  color: var(--text-dim);
  text-decoration: none;
  transition: all 0.2s;
}

.tab-item.active {
  background: var(--accent);
  color: #fff;
  box-shadow: 0 2px 8px rgba(var(--accent-rgb, 99, 102, 241), 0.3);
}

.auth-card-header {
  margin-bottom: 24px;
}

.auth-card-header h2 {
  font-size: 20px;
  font-weight: 700;
  margin: 0 0 6px;
  color: var(--text);
}

.auth-card-header p {
  font-size: 13px;
  margin: 0;
  color: var(--text-dim);
}

/* 错误横幅 */
.auth-err-banner {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 14px;
  border-radius: 8px;
  background: rgba(239, 68, 68, 0.12);
  border: 1px solid rgba(239, 68, 68, 0.3);
  color: var(--red);
  font-size: 13px;
  margin-bottom: 18px;
}

.form-item {
  margin-bottom: 18px;
}

.form-label {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--text);
}

.input-wrap {
  position: relative;
  display: flex;
  align-items: center;
}

.input-icon {
  position: absolute;
  left: 12px;
  font-size: 14px;
  pointer-events: none;
  opacity: 0.6;
}

.modern-input {
  width: 100%;
  padding: 10px 12px 10px 36px;
  background: rgba(255, 255, 255, 0.04);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 13.5px;
  transition: all 0.2s;
  outline: none;
}

.modern-input:focus {
  border-color: var(--accent);
  background: rgba(255, 255, 255, 0.07);
  box-shadow: 0 0 0 3px rgba(var(--accent-rgb, 99, 102, 241), 0.2);
}

.pwd-toggle-btn {
  position: absolute;
  right: 10px;
  background: none;
  border: none;
  cursor: pointer;
  font-size: 14px;
  opacity: 0.6;
  transition: opacity 0.15s;
}

.pwd-toggle-btn:hover {
  opacity: 1;
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  border-radius: 8px;
  border: none;
  background: linear-gradient(135deg, var(--accent) 0%, #4f46e5 100%);
  color: #fff;
  font-size: 14px;
  font-weight: 650;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 14px rgba(var(--accent-rgb, 99, 102, 241), 0.35);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px rgba(var(--accent-rgb, 99, 102, 241), 0.45);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-card-footer {
  margin-top: 24px;
  text-align: center;
  font-size: 13px;
  color: var(--text-dim);
}

.link-highlight {
  color: var(--accent);
  text-decoration: none;
  font-weight: 600;
  margin-left: 6px;
}

.link-highlight:hover {
  text-decoration: underline;
}

/* 响应式适配 */
@media (max-width: 900px) {
  .auth-container {
    grid-template-columns: 1fr;
    gap: 32px;
  }
  .auth-hero {
    text-align: center;
  }
  .auth-hero-brand {
    justify-content: center;
  }
  .auth-hero-desc {
    margin: 0 auto 24px;
  }
  .hero-features-grid {
    display: none;
  }
  .auth-glass-card {
    padding: 24px 20px;
  }
}
</style>
