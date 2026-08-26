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
          <span class="brand-badge">2027 校招高频冲刺站</span>
        </div>

        <h1 class="auth-hero-title">
          专为大模型算法与研发工程师打造的<br />
          <span class="gradient-text">沉浸式智能刷题平台</span>
        </h1>

        <p class="auth-hero-desc">
          汇聚力扣热题 100、面经高频手撕与 750+ 道大模型八股自测（含 Agent Harness），支持 Docker 沙箱秒级评测与自定义 AI 导师答疑。
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
              <h4>750+ 道八股客观题</h4>
              <p>含 Agent Harness / MCP / Skills，错题本与斩题模式</p>
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

      <!-- 右侧注册表单卡片 -->
      <div class="auth-form-side">
        <div class="auth-glass-card">
          <!-- 切换选项卡 -->
          <div class="auth-tab-switch">
            <RouterLink to="/login" class="tab-item">登录账号</RouterLink>
            <RouterLink to="/register" class="tab-item active">注册新账号</RouterLink>
          </div>

          <div class="auth-card-header">
            <h2>创建你的账号</h2>
            <p>填入信息并使用邀请码激活专属刷题题库</p>
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
                <span class="form-hint">3-32 位字母/数字/下划线</span>
              </label>
              <div class="input-wrap">
                <span class="input-icon">👤</span>
                <input
                  v-model="username"
                  class="modern-input"
                  placeholder="例如: leeter_2026"
                  autocomplete="username"
                  required
                  minlength="3"
                  maxlength="32"
                />
              </div>
            </div>

            <!-- 邮箱（可选） -->
            <div class="form-item">
              <label class="form-label">
                <span>电子邮箱</span>
                <span class="form-hint">可选，用于找回与通知</span>
              </label>
              <div class="input-wrap">
                <span class="input-icon">✉️</span>
                <input
                  v-model="email"
                  class="modern-input"
                  type="email"
                  placeholder="name@example.com"
                  autocomplete="email"
                />
              </div>
            </div>

            <!-- 邀请码 -->
            <div class="form-item">
              <label class="form-label">
                <span>激活邀请码 <span class="req">*</span></span>
                <span class="form-hint">必填</span>
              </label>
              <div class="input-wrap">
                <span class="input-icon">🎟️</span>
                <input
                  v-model="inviteCode"
                  class="modern-input mono"
                  placeholder="输入你的注册邀请码"
                  autocomplete="off"
                  required
                />
              </div>
            </div>

            <!-- 密码 -->
            <div class="form-item">
              <label class="form-label">
                <span>设置密码 <span class="req">*</span></span>
                <span class="form-hint">至少 8 位字符</span>
              </label>
              <div class="input-wrap">
                <span class="input-icon">🔒</span>
                <input
                  v-model="password"
                  class="modern-input"
                  :type="showPwd ? 'text' : 'password'"
                  placeholder="••••••••••••"
                  autocomplete="new-password"
                  required
                  minlength="8"
                />
                <button
                  type="button"
                  class="pwd-toggle-btn"
                  @click="showPwd = !showPwd"
                >
                  {{ showPwd ? '🙈' : '👁️' }}
                </button>
              </div>
              <!-- 密码强度指示条 -->
              <div v-if="password.length > 0" class="pwd-strength-bar">
                <div class="strength-track">
                  <div
                    class="strength-fill"
                    :style="{ width: `${pwdStrength.percent}%`, background: pwdStrength.color }"
                  ></div>
                </div>
                <span class="strength-label" :style="{ color: pwdStrength.color }">{{ pwdStrength.text }}</span>
              </div>
            </div>

            <!-- 确认密码 -->
            <div class="form-item">
              <label class="form-label">
                <span>确认密码 <span class="req">*</span></span>
              </label>
              <div class="input-wrap">
                <span class="input-icon">🛡️</span>
                <input
                  v-model="confirm"
                  class="modern-input"
                  :type="showPwd ? 'text' : 'password'"
                  placeholder="再次输入相同密码"
                  autocomplete="new-password"
                  required
                />
              </div>
            </div>

            <!-- 注册按钮 -->
            <button class="submit-btn" :disabled="loading">
              <span v-if="loading" class="btn-spinner"></span>
              <span>{{ loading ? '正在创建账号…' : '立即注册并开始刷题 →' }}</span>
            </button>
          </form>

          <div class="auth-card-footer">
            <span>已经有账号了？</span>
            <RouterLink to="/login" class="link-highlight">直接登录</RouterLink>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const username = ref('')
const email = ref('')
const inviteCode = ref('')
const password = ref('')
const confirm = ref('')
const error = ref('')
const loading = ref(false)
const showPwd = ref(false)

const auth = useAuthStore()
const router = useRouter()

// 计算密码强度
const pwdStrength = computed(() => {
  const p = password.value
  if (!p) return { percent: 0, text: '', color: 'transparent' }
  if (p.length < 8) return { percent: 25, text: '太短', color: 'var(--red)' }
  
  let score = 0
  if (/[a-z]/.test(p)) score++
  if (/[A-Z]/.test(p)) score++
  if (/[0-9]/.test(p)) score++
  if (/[^a-zA-Z0-9]/.test(p)) score++
  if (p.length >= 12) score++

  if (score <= 2) return { percent: 50, text: '中等', color: 'var(--amber, #f59e0b)' }
  if (score >= 4) return { percent: 100, text: '极强', color: 'var(--green, #10b981)' }
  return { percent: 75, text: '良好', color: 'var(--accent, #6366f1)' }
})

async function onSubmit() {
  error.value = ''
  if (password.value !== confirm.value) {
    error.value = '两次输入的密码不一致，请重新检查'
    return
  }
  loading.value = true
  try {
    await auth.register(username.value, password.value, inviteCode.value.trim(), email.value)
    router.push('/')
  } catch (e) {
    error.value = e instanceof Error ? e.message : '注册失败，请检查邀请码或用户名'
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
  background: var(--accent-2);
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
  background: var(--accent-soft);
  color: var(--accent);
  border: 1px solid var(--accent-border);
}

.auth-hero-title {
  font-size: 32px;
  line-height: 1.35;
  font-weight: 800;
  font-family: var(--serif);
  margin-bottom: 16px;
  color: var(--text);
}

.gradient-text {
  background: var(--grad-text);
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
  background: var(--surface);
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
  background: var(--surface);
  border: 1px solid var(--border);
  backdrop-filter: blur(16px);
  border-radius: 16px;
  padding: 32px 32px;
  box-shadow: var(--shadow-lg);
}

/* 顶部 Tab 切换 */
.auth-tab-switch {
  display: flex;
  background: var(--surface-2);
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
  color: var(--bg);
  box-shadow: var(--shadow-accent);
}

.auth-card-header {
  margin-bottom: 20px;
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
  background: var(--red-soft);
  border: 1px solid var(--red);
  color: var(--red);
  font-size: 13px;
  margin-bottom: 18px;
}

.form-item {
  margin-bottom: 16px;
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

.form-hint {
  font-size: 11.5px;
  font-weight: 400;
  color: var(--text-faint);
}

.req {
  color: var(--red);
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
  background: var(--surface-2);
  border: 1px solid var(--border);
  border-radius: 8px;
  color: var(--text);
  font-size: 13.5px;
  transition: all 0.2s;
  outline: none;
}

.modern-input:focus {
  border-color: var(--accent);
  background: var(--surface);
  box-shadow: 0 0 0 3px var(--accent-soft);
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

/* 密码强度条 */
.pwd-strength-bar {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-top: 6px;
}

.strength-track {
  flex: 1;
  height: 4px;
  background: var(--surface-3);
  border-radius: 2px;
  overflow: hidden;
}

.strength-fill {
  height: 100%;
  transition: width 0.25s ease, background 0.25s ease;
}

.strength-label {
  font-size: 11px;
  font-weight: 600;
  width: 32px;
}

/* 提交按钮 */
.submit-btn {
  width: 100%;
  padding: 12px;
  margin-top: 10px;
  border-radius: 8px;
  border: none;
  background: var(--grad);
  color: var(--bg);
  font-size: 14px;
  font-weight: 650;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  box-shadow: 0 4px 14px var(--accent-soft);
}

.submit-btn:hover:not(:disabled) {
  transform: translateY(-1px);
  box-shadow: 0 6px 20px var(--accent-border);
}

.submit-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.auth-card-footer {
  margin-top: 20px;
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
    display: none; /* 小屏隐藏特性列表保持紧凑 */
  }
  .auth-glass-card {
    padding: 24px 20px;
  }
}
</style>
