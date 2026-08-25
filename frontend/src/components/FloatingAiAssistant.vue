<template>
  <div>
    <!-- 1. 全局悬浮胶囊 (Sleek Cyber Glass Floating Capsule) -->
    <div
      v-if="!assistant.isVisible.value && auth.me"
      class="floating-capsule"
      :class="{ 'has-context': isContextual, 'is-dragging': isDraggingCapsule }"
      :style="capsuleStyle"
      @mousedown="startDragCapsule"
      @click="onCapsuleClick"
      title="按住拖拽位置 · 点击唤起 AI 导师"
    >
      <div class="capsule-inner">
        <!-- 科技光芒图标 -->
        <div class="capsule-icon-box">
          <svg class="spark-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor">
            <path
              d="M12 2L14.4 8.6L21 11L14.4 13.4L12 20L9.6 13.4L3 11L9.6 8.6L12 2Z"
              fill="var(--accent)"
              stroke="var(--accent)"
              stroke-width="1.5"
              stroke-linejoin="round"
            />
          </svg>
        </div>

        <div class="capsule-info">
          <div class="capsule-row-top">
            <span class="capsule-brand">LeetPath AI</span>
            <span class="capsule-dot" :class="{ ready: ai.isConfigured.value }"></span>
          </div>
          <span class="capsule-sub mono">{{ contextBadgeText }}</span>
        </div>
      </div>
    </div>

    <!-- 2. 悬浮智能交互窗口 (Glassmorphic Neo-Dark Window) -->
    <div
      v-if="assistant.isVisible.value"
      class="floating-window-backdrop"
      :class="{ maximized: assistant.isMaximized.value }"
      @click.self="onBackdropClick"
    >
      <div
        class="floating-window"
        :class="{ 'is-max': assistant.isMaximized.value, 'is-dragging': isDraggingWindow }"
        :style="windowStyle"
      >
        <!-- 窗口顶栏（极简高端拖拽条） -->
        <div
          class="f-window-head"
          @mousedown="startDragWindow"
          title="按住顶部可自由拖动位置"
        >
          <div class="f-head-info">
            <div class="f-head-badge">
              <span class="sparkle-mini">✦</span>
              <span class="badge-source-label">{{ contextTypeLabel }}</span>
              <span class="badge-model-tag mono">{{ ai.selectedModel.value || '未选模型' }}</span>
            </div>
            <h3 class="f-title" :title="assistant.currentContext.value.title">
              {{ assistant.currentContext.value.title }}
            </h3>
          </div>

          <div class="f-head-actions" @mousedown.stop>
            <!-- 新建会话 / 清空记忆 -->
            <button class="win-btn" title="新建会话 / 清空历史记忆 (0 Token 重置)" @click="onNewChat">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="12" y1="5" x2="12" y2="19" />
                <line x1="5" y1="12" x2="19" y2="12" />
              </svg>
            </button>
            <!-- 智能压缩上下文 -->
            <button
              v-if="messages.length > 2"
              class="win-btn"
              title="智能压缩上下文（提炼关键要点，释放 Token）"
              :disabled="generating"
              @click="onCompressContext"
            >
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                <polyline points="4 14 10 14 10 20" />
                <polyline points="20 10 14 10 14 4" />
                <line x1="14" y1="10" x2="21" y2="3" />
                <line x1="3" y1="21" x2="10" y2="14" />
              </svg>
            </button>
            <!-- 设置按钮 -->
            <button class="win-btn" title="AI 设置与模型配置" @click="showSettings = true">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="3" />
                <path d="M19.4 15a1.65 1.65 0 0 0 .33 1.82l.06.06a2 2 0 0 1 0 2.83 2 2 0 0 1-2.83 0l-.06-.06a1.65 1.65 0 0 0-1.82-.33 1.65 1.65 0 0 0-1 1.51V21a2 2 0 0 1-2 2 2 2 0 0 1-2-2v-.09A1.65 1.65 0 0 0 9 19.4a1.65 1.65 0 0 0-1.82.33l-.06.06a2 2 0 0 1-2.83 0 2 2 0 0 1 0-2.83l.06-.06a1.65 1.65 0 0 0 .33-1.82 1.65 1.65 0 0 0-1.51-1H3a2 2 0 0 1-2-2 2 2 0 0 1 2-2h.09A1.65 1.65 0 0 0 4.6 9a1.65 1.65 0 0 0-.33-1.82l-.06-.06a2 2 0 0 1 0-2.83 2 2 0 0 1 2.83 0l.06.06a1.65 1.65 0 0 0 1.82.33H9a1.65 1.65 0 0 0 1-1.51V3a2 2 0 0 1 2-2 2 2 0 0 1 2 2v.09a1.65 1.65 0 0 0 1 1.51 1.65 1.65 0 0 0 1.82-.33l.06-.06a2 2 0 0 1 2.83 0 2 2 0 0 1 0 2.83l-.06.06a1.65 1.65 0 0 0-.33 1.82V9a1.65 1.65 0 0 0 1.51 1H21a2 2 0 0 1 2 2 2 2 0 0 1-2 2h-.09a1.65 1.65 0 0 0-1.51 1z" />
              </svg>
            </button>
            <!-- 居中复位 -->
            <button
              v-if="!assistant.isMaximized.value"
              class="win-btn"
              title="复位窗口位置"
              @click="resetWindowPos"
            >
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10" />
                <line x1="22" y1="12" x2="18" y2="12" />
                <line x1="6" y1="12" x2="2" y2="12" />
                <line x1="12" y1="6" x2="12" y2="2" />
                <line x1="12" y1="22" x2="12" y2="18" />
              </svg>
            </button>
            <!-- 最大化/还原 -->
            <button
              class="win-btn"
              :title="assistant.isMaximized.value ? '还原' : '最大化'"
              @click="assistant.toggleMaximize()"
            >
              <svg v-if="!assistant.isMaximized.value" viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2" ry="2" />
              </svg>
              <svg v-else viewBox="0 0 24 24" width="13" height="13" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="6" y="9" width="14" height="12" rx="1.5" />
                <path d="M4 15V5a1 1 0 0 1 1-1h10" />
              </svg>
            </button>
            <!-- 关闭/最小化 -->
            <button class="win-btn win-close" title="最小化收起" @click="assistant.close()">
              <svg viewBox="0 0 24 24" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2">
                <line x1="18" y1="6" x2="6" y2="18" />
                <line x1="6" y1="6" x2="18" y2="18" />
              </svg>
            </button>
          </div>
        </div>

        <!-- 未配置 API Key 引导 -->
        <div v-if="!ai.isConfigured.value" class="f-config-guide">
          <div class="guide-icon">⚡</div>
          <div class="guide-text">
            <h4>尚未配置大模型 API Key</h4>
            <p>
              已默认接入 Antithor 专属中转站，可
              <a href="https://api.antithor.asia" target="_blank" rel="noopener noreferrer" style="color:var(--accent);text-decoration:underline;font-weight:600">点击登录 antithor 获取 key ↗</a>
            </p>
          </div>
          <button class="btn btn-xs btn-primary guide-btn" @click="showSettings = true">
            一键配置
          </button>
        </div>

        <!-- 场景化快捷追问 Chips -->
        <div
          v-if="assistant.currentContext.value.presetPrompts?.length"
          class="f-chips-wrapper"
        >
          <div class="f-chips-track">
            <button
              v-for="p in assistant.currentContext.value.presetPrompts"
              :key="p.label"
              class="chip-pill"
              :disabled="generating"
              @click="onSendPrompt(p.prompt)"
            >
              <span class="chip-glow"></span>
              <span class="chip-label">{{ p.label }}</span>
            </button>
          </div>
        </div>

        <!-- 对话流消息区域 -->
        <div class="f-messages-container" ref="msgContainer">
          <div
            v-for="(msg, idx) in messages"
            :key="idx"
            class="msg-bubble-group"
            :class="`role-${msg.role}`"
          >
            <!-- 头像标识 -->
            <div class="msg-avatar">
              <div v-if="msg.role === 'assistant'" class="assistant-avatar-badge">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none">
                  <path
                    d="M12 2L14.4 8.6L21 11L14.4 13.4L12 20L9.6 13.4L3 11L9.6 8.6L12 2Z"
                    fill="currentColor"
                  />
                </svg>
              </div>
              <div v-else class="user-avatar-badge">
                {{ (auth.me?.username || 'U').slice(0, 1).toUpperCase() }}
              </div>
            </div>

            <!-- 消息主体 -->
            <div class="msg-card">
              <div class="msg-header">
                <span class="msg-sender">
                  {{ msg.role === 'assistant' ? (ai.selectedModel.value ? `AI 导师 · ${ai.selectedModel.value}` : 'AI 导师') : '我' }}
                </span>
                <div class="msg-actions" v-if="msg.role === 'assistant'">
                  <span v-if="msg.isCached" class="tag-cache" title="已从本地浏览器 0 Token 秒级读取">
                    ⚡ 0 Token 缓存
                  </span>
                  <button
                    v-if="msg.isCached && msg.originalPrompt"
                    class="btn-text-action"
                    :disabled="generating"
                    @click="onSendPrompt(msg.originalPrompt, true)"
                  >
                    🔄 重新生成
                  </button>
                  <button
                    v-if="msg.content"
                    class="btn-text-action"
                    @click="copyText(msg.content)"
                  >
                    复制
                  </button>
                </div>
              </div>

              <div class="msg-markdown statement" v-html="renderMd(msg.content)"></div>
            </div>
          </div>

          <!-- 正在流式生成状态 -->
          <div v-if="generating" class="msg-bubble-group role-assistant">
            <div class="msg-avatar">
              <div class="assistant-avatar-badge pulsing">
                <svg viewBox="0 0 24 24" width="14" height="14" fill="none">
                  <path
                    d="M12 2L14.4 8.6L21 11L14.4 13.4L12 20L9.6 13.4L3 11L9.6 8.6L12 2Z"
                    fill="currentColor"
                  />
                </svg>
              </div>
            </div>
            <div class="msg-card">
              <div class="msg-header">
                <span class="msg-sender">AI 导师正在深度思考生成中...</span>
              </div>
              <div class="msg-markdown statement" v-html="renderMd(streamBuffer || '...')"></div>
              <span class="typing-cursor"></span>
            </div>
          </div>
        </div>

        <!-- 底部输入框区域 -->
        <div class="f-bottom-composer">
          <div class="composer-box">
            <textarea
              v-model="inputQuestion"
              class="composer-textarea"
              placeholder="输入你的技术疑问、更多解法追问或时空复杂度诊断... (Enter 发送)"
              rows="2"
              :disabled="generating"
              @keydown.enter.exact.prevent="onEnterSend"
            ></textarea>
            
            <div class="composer-toolbar">
              <div class="composer-status">
                <span class="status-shield" :class="tokenLevelClass" :title="`当前会话预估已占用 ${currentTotalTokens} Tokens，总预算上限 ${ai.maxContextTokens.value} Tokens`">
                  ⚡ 记忆占用: {{ formatTokens(currentTotalTokens) }} / {{ formatTokens(ai.maxContextTokens.value) }} ({{ tokenPercent }}%)
                </span>
              </div>
              
              <div class="composer-actions">
                <button
                  v-if="generating"
                  class="btn-stop"
                  @click="abort"
                >
                  <span class="stop-icon">■</span> 停止
                </button>
                <button
                  v-else
                  class="btn-send"
                  :disabled="!inputQuestion.trim() || !ai.isConfigured.value"
                  @click="onSendPrompt(inputQuestion)"
                  title="发送提问 (Enter)"
                >
                  <svg viewBox="0 0 24 24" width="15" height="15" fill="none" stroke="currentColor" stroke-width="2.5">
                    <line x1="12" y1="19" x2="12" y2="5" />
                    <polyline points="5 12 12 5 19 12" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>

        <!-- 右下角拉伸角标 -->
        <div class="f-resize-corner" title="拖动右下角拉伸窗口">
          <svg viewBox="0 0 10 10" width="10" height="10" fill="none" stroke="currentColor">
            <line x1="8" y1="2" x2="2" y2="8" stroke-width="1.5" />
            <line x1="8" y1="5" x2="5" y2="8" stroke-width="1.5" />
            <line x1="8" y1="8" x2="8" y2="8" stroke-width="1.5" />
          </svg>
        </div>
      </div>
    </div>

    <!-- AI 设置弹窗 -->
    <AiSettingsModal v-if="showSettings" @close="showSettings = false" />
  </div>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import AiSettingsModal from './AiSettingsModal.vue'
import { renderMarkdown } from '../markdown'
import { estimateTokens, useAiStore, type AiMessage } from '../stores/ai'
import { useAiAssistant } from '../stores/aiAssistant'
import { useAuthStore } from '../stores/auth'
import { useToast } from '../stores/toast'

interface ChatMessage extends AiMessage {
  isCached?: boolean
  originalPrompt?: string
}

const auth = useAuthStore()
const ai = useAiStore()
const assistant = useAiAssistant()
const toast = useToast()

const showSettings = ref(false)
const generating = ref(false)
const inputQuestion = ref('')
const streamBuffer = ref('')
const messages = ref<ChatMessage[]>([])
const msgContainer = ref<HTMLElement | null>(null)
let abortController: AbortController | null = null

// --- 窗口自由拖拽与尺寸管理 ---
const isDraggingWindow = ref(false)
const isDraggingCapsule = ref(false)
let hasMovedCapsule = false

// 悬浮窗口坐标与初始宽高（大幅加大默认尺寸：宽 580px，高 740px）
const windowPos = ref({
  x: typeof window !== 'undefined' ? Math.max(20, window.innerWidth - 620) : 100,
  y: typeof window !== 'undefined' ? Math.max(20, window.innerHeight - 780) : 40,
})

// 悬浮球坐标
const capsulePos = ref<{ x: number | null; y: number | null }>({ x: null, y: null })

const isContextual = computed(() => assistant.currentContext.value.source !== 'general')

const contextTypeLabel = computed(() => {
  const src = assistant.currentContext.value.source
  if (src === 'problem') return '力扣手撕'
  if (src === 'review') return '背题模式'
  if (src === 'quiz') return '八股自测'
  return '技术导师'
})

const contextBadgeText = computed(() => {
  const src = assistant.currentContext.value.source
  if (src === 'problem') return '当前题目'
  if (src === 'review') return '背题助手'
  if (src === 'quiz') return '八股考点'
  return ai.selectedModel.value ? ai.selectedModel.value.slice(0, 10) : '未配置'
})

// 窗口动态样式
const windowStyle = computed(() => {
  if (assistant.isMaximized.value) return {}
  return {
    left: `${windowPos.value.x}px`,
    top: `${windowPos.value.y}px`,
  }
})

// 胶囊动态样式
const capsuleStyle = computed(() => {
  if (capsulePos.value.x === null || capsulePos.value.y === null) return {}
  return {
    left: `${capsulePos.value.x}px`,
    top: `${capsulePos.value.y}px`,
    right: 'auto',
    bottom: 'auto',
  }
})

function resetWindowPos() {
  windowPos.value = {
    x: Math.max(20, window.innerWidth - 620),
    y: Math.max(20, window.innerHeight - 780),
  }
  toast.info('已复位悬浮窗位置')
}

// 1. 拖拽悬浮窗
function startDragWindow(e: MouseEvent) {
  if (assistant.isMaximized.value) return
  if ((e.target as HTMLElement).closest('.f-head-actions')) return

  isDraggingWindow.value = true
  const startX = e.clientX
  const startY = e.clientY
  const initX = windowPos.value.x
  const initY = windowPos.value.y

  function onMouseMove(moveEvent: MouseEvent) {
    const dx = moveEvent.clientX - startX
    const dy = moveEvent.clientY - startY
    const maxX = Math.max(0, window.innerWidth - 200)
    const maxY = Math.max(0, window.innerHeight - 80)

    windowPos.value = {
      x: Math.min(maxX, Math.max(0, initX + dx)),
      y: Math.min(maxY, Math.max(0, initY + dy)),
    }
  }

  function onMouseUp() {
    isDraggingWindow.value = false
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('mouseup', onMouseUp)
  }

  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}

// 2. 拖拽胶囊球
function startDragCapsule(e: MouseEvent) {
  isDraggingCapsule.value = true
  hasMovedCapsule = false
  const startX = e.clientX
  const startY = e.clientY
  const rect = (e.currentTarget as HTMLElement).getBoundingClientRect()
  const initX = rect.left
  const initY = rect.top

  function onMouseMove(moveEvent: MouseEvent) {
    const dx = moveEvent.clientX - startX
    const dy = moveEvent.clientY - startY
    if (Math.abs(dx) > 3 || Math.abs(dy) > 3) {
      hasMovedCapsule = true
    }
    capsulePos.value = {
      x: Math.min(window.innerWidth - 100, Math.max(10, initX + dx)),
      y: Math.min(window.innerHeight - 50, Math.max(10, initY + dy)),
    }
  }

  function onMouseUp() {
    isDraggingCapsule.value = false
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('mouseup', onMouseUp)
  }

  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
}

function onCapsuleClick() {
  if (!hasMovedCapsule) {
    assistant.toggle()
  }
}

function onBackdropClick() {
  if (assistant.isMaximized.value) {
    assistant.close()
  }
}

function renderMd(text: string) {
  if (!text) return ''
  return renderMarkdown(text)
}

function copyText(text: string) {
  navigator.clipboard.writeText(text)
  toast.success('已复制到剪贴板')
}

function scrollToBottom() {
  nextTick(() => {
    if (msgContainer.value) {
      msgContainer.value.scrollTop = msgContainer.value.scrollHeight
    }
  })
}

function onEnterSend() {
  if (!inputQuestion.value.trim() || generating.value) return
  onSendPrompt(inputQuestion.value)
}

function abort() {
  if (abortController) {
    abortController.abort()
    abortController = null
  }
  generating.value = false
}

async function onSendPrompt(userPrompt: string, forceRefresh = false) {
  if (!userPrompt.trim()) return
  if (!ai.isConfigured.value) {
    showSettings.value = true
    return
  }

  const promptText = userPrompt.trim()
  inputQuestion.value = ''

  const ctx = assistant.currentContext.value
  const cKey = ctx.contextKey || 'general'

  // 1. 检查本地响应缓存（0 Token 秒级读取）
  if (!forceRefresh && ai.enableLocalCache.value) {
    const cached = ai.getCachedAnswer(cKey, promptText)
    if (cached) {
      messages.value.push({ role: 'user', content: promptText })
      messages.value.push({
        role: 'assistant',
        content: cached,
        isCached: true,
        originalPrompt: promptText,
      })
      scrollToBottom()
      toast.info('⚡ 已从本地秒级载入缓存回答 (0 Token 消耗)')
      return
    }
  }

  // 2. 发起真实流式请求
  messages.value.push({ role: 'user', content: promptText })
  scrollToBottom()

  generating.value = true
  streamBuffer.value = ''
  abortController = new AbortController()

  const sysContent = `你是一位资深的技术面试官与计算机/大模型教学导师。
请针对用户目前正在练习或背诵的题目提供深入浅出、极具洞察力的解答。
回答要求：
1. 若询问【更多解法】，请按思维演进清晰罗列（如：暴力法 ➔ 空间换时间哈希法 ➔ 双指针/单调栈最优解），并逐一分析时空复杂度与优缺点；
2. 若询问【记忆口诀/核心代码模板】，请提炼极简、易背、不易写错的骨架；
3. 如涉及代码，请给出清晰注释；如涉及数学公式，使用标准 LaTeX 格式。

【当前题目/学习上下文】：
${ctx.contextText || '无特定上下文'}`

  const apiMessages: AiMessage[] = [
    { role: 'system', content: sysContent },
    ...messages.value.map((m) => ({ role: m.role, content: m.content })),
  ]

  try {
    const full = await ai.streamChat(
      apiMessages,
      (chunk) => {
        streamBuffer.value += chunk
        scrollToBottom()
      },
      abortController.signal,
    )
    const resultText = full || streamBuffer.value
    messages.value.push({
      role: 'assistant',
      content: resultText,
      isCached: false,
      originalPrompt: promptText,
    })

    if (ai.enableLocalCache.value && resultText.trim()) {
      ai.setCachedAnswer(cKey, promptText, resultText)
    }
    streamBuffer.value = ''
  } catch (err: any) {
    if (err.name !== 'AbortError') {
      toast.error(err.message || 'AI 答疑生成失败')
      messages.value.push({
        role: 'assistant',
        content: `✕ 生成失败：${err.message || '网络连接中断'}`,
      })
    }
  } finally {
    generating.value = false
    abortController = null
    scrollToBottom()
  }
}

function formatTokens(n: number): string {
  if (n >= 1048576) return `${(n / 1048576).toFixed(1)}M`
  if (n >= 1024) return `${(n / 1024).toFixed(0)}K`
  return `${n}`
}

const currentTotalTokens = computed(() => {
  const ctx = assistant.currentContext.value
  let total = estimateTokens(ctx.contextText || '') + 200
  for (const m of messages.value) {
    total += estimateTokens(m.content)
  }
  if (streamBuffer.value) {
    total += estimateTokens(streamBuffer.value)
  }
  return total
})

const tokenPercent = computed(() => {
  const budget = ai.maxContextTokens.value || 131072
  return Math.min(100, Math.round((currentTotalTokens.value / budget) * 100))
})

const tokenLevelClass = computed(() => {
  if (tokenPercent.value > 85) return 'token-danger'
  if (tokenPercent.value > 60) return 'token-warning'
  return 'token-normal'
})

function onNewChat() {
  if (generating.value) abort()
  messages.value = [
    {
      role: 'assistant',
      content: `✨ 已为你开启全新会话！\n\n已清空上一轮历史对话，Token 计数已重置归零。当前锚定 **${assistant.currentContext.value.title}**，你可以随时输入新疑问或点击上方快捷芯片！`,
    },
  ]
  toast.success('已新建会话，历史记忆已清空重置')
}

async function onCompressContext() {
  if (generating.value || messages.value.length <= 1) return

  const promptText = '请将我们上方全部讨论过的核心解法、代码要点与关键结论，精炼压缩为 3-4 条极简核心知识备忘（保留关键思路，删除多余废话）。'
  toast.info('正在智能压缩历史上下文要点...')

  await onSendPrompt(promptText, true)

  // 压缩完毕后，把历史多轮消息归约成一条精简摘要
  const lastReply = messages.value[messages.value.length - 1]
  if (lastReply && lastReply.role === 'assistant') {
    messages.value = [
      {
        role: 'assistant',
        content: `🗜️ **[已压缩历史上下文备忘]**：\n\n${lastReply.content}\n\n*(历史长对话已智能精简压缩，释放了大量 Token 空间，你可以顺着以上要点继续提问)*`,
      },
    ]
    toast.success('上下文压缩完毕！已释放大部分 Token 空间')
  }
}

// 监听上下文切换时重置会话并提示
watch(
  () => assistant.currentContext.value.contextKey,
  (newKey, oldKey) => {
    if (newKey !== oldKey) {
      messages.value = [
        {
          role: 'assistant',
          content: `👋 你好！已为你锁定当前 **${assistant.currentContext.value.title}**。\n\n你可以点击下方的**快捷追问**（例如查看*更多解法*、*时空优化*、*记忆口诀*），或直接输入你的疑问！`,
        },
      ]
    }
  },
  { immediate: true },
)

// 监听待发送的 pendingPrompt
watch(
  () => assistant.pendingPrompt.value,
  (prompt) => {
    if (prompt) {
      assistant.pendingPrompt.value = null
      onSendPrompt(prompt)
    }
  },
)

onMounted(() => {
  if (typeof window !== 'undefined') {
    windowPos.value = {
      x: Math.max(20, window.innerWidth - 620),
      y: Math.max(20, window.innerHeight - 780),
    }
  }
})
</script>

<style scoped>
/* 1. 悬浮胶囊球 (Themed Floating Capsule) */
.floating-capsule {
  position: fixed;
  bottom: 28px;
  right: 28px;
  z-index: 850;
  cursor: grab;
  border-radius: 40px;
  padding: 1px;
  background: var(--accent-border, var(--border));
  box-shadow: 0 8px 24px var(--shadow-lg, rgba(0, 0, 0, 0.4));
  transition: transform 0.2s cubic-bezier(0.16, 1, 0.3, 1), box-shadow 0.2s;
  user-select: none;
}

.floating-capsule.is-dragging {
  cursor: grabbing;
  transform: scale(1.04);
  box-shadow: 0 16px 40px rgba(0, 0, 0, 0.6);
}

.floating-capsule:hover {
  transform: translateY(-2px) scale(1.02);
  border-color: var(--accent);
  box-shadow: 0 12px 32px var(--shadow-accent, rgba(0, 0, 0, 0.5));
}

.capsule-inner {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 7px 16px 7px 10px;
  border-radius: 40px;
  background: var(--surface, #1f2125);
  backdrop-filter: blur(16px);
  border: 1px solid var(--border);
}

.capsule-icon-box {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--accent-soft);
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--accent);
}

.spark-icon {
  width: 15px;
  height: 15px;
  animation: sparkSpin 12s linear infinite;
}

@keyframes sparkSpin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.capsule-info {
  display: flex;
  flex-direction: column;
}

.capsule-row-top {
  display: flex;
  align-items: center;
  gap: 6px;
}

.capsule-brand {
  font-size: 13px;
  font-weight: 700;
  color: var(--text);
  letter-spacing: -0.2px;
}

.capsule-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--text-faint);
}

.capsule-dot.ready {
  background: var(--green, #10b981);
  box-shadow: 0 0 6px var(--green, #10b981);
}

.capsule-sub {
  font-size: 10.5px;
  color: var(--text-dim);
}

/* 2. 悬浮智能交互窗口 (Themed Floating Window) */
.floating-window-backdrop {
  position: fixed;
  inset: 0;
  z-index: 920;
  pointer-events: none;
}

.floating-window-backdrop.maximized {
  background: rgba(0, 0, 0, 0.6);
  backdrop-filter: blur(6px);
  pointer-events: auto;
  display: flex;
  align-items: center;
  justify-content: center;
}

.floating-window {
  position: fixed;
  width: 580px;
  height: 740px;
  min-width: 380px;
  min-height: 480px;
  max-width: calc(100vw - 24px);
  max-height: calc(100vh - 24px);
  resize: both;
  background: var(--surface, #1f2125);
  border: 1px solid var(--border-strong, var(--border));
  backdrop-filter: blur(28px);
  border-radius: var(--radius, 14px);
  display: flex;
  flex-direction: column;
  box-shadow: 0 24px 60px rgba(0, 0, 0, 0.5), 0 0 0 1px var(--border);
  pointer-events: auto;
  overflow: hidden;
  animation: windowIn 0.2s cubic-bezier(0.16, 1, 0.3, 1);
}

.floating-window.is-max {
  position: relative !important;
  left: auto !important;
  top: auto !important;
  width: 980px !important;
  height: 88vh !important;
  max-width: 95vw !important;
  max-height: 92vh !important;
  resize: none;
}

@keyframes windowIn {
  from {
    opacity: 0;
    transform: scale(0.96);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

/* 顶栏拖拽条 */
.f-window-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 12px 18px;
  border-bottom: 1px solid var(--border);
  background: var(--surface-2, #282b31);
  cursor: grab;
  user-select: none;
}

.f-window-head:active {
  cursor: grabbing;
}

.f-head-badge {
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 3px;
}

.sparkle-mini {
  color: var(--accent);
  font-size: 11px;
}

.badge-source-label {
  font-size: 11px;
  font-weight: 700;
  color: var(--accent);
  letter-spacing: 0.3px;
}

.badge-model-tag {
  font-size: 10px;
  color: var(--text-dim);
  background: var(--surface-3, #34383f);
  padding: 1px 6px;
  border-radius: 4px;
  border: 1px solid var(--border);
}

.f-title {
  margin: 0;
  font-size: 14.5px;
  font-weight: 700;
  color: var(--text);
  max-width: 380px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.f-head-actions {
  display: flex;
  align-items: center;
  gap: 6px;
  cursor: default;
}

.win-btn {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface-3, #34383f);
  color: var(--text-dim);
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: all 0.15s ease;
}

.win-btn:hover {
  background: var(--surface-2);
  color: var(--text);
  border-color: var(--border-strong);
}

.win-close:hover {
  background: var(--red-soft, rgba(192, 73, 47, 0.15));
  color: var(--red, #c0492f);
  border-color: var(--red);
}

/* 引导配置 */
.f-config-guide {
  display: flex;
  align-items: center;
  gap: 12px;
  margin: 12px 16px 0;
  padding: 10px 14px;
  border-radius: 8px;
  background: var(--amber-soft, rgba(168, 121, 42, 0.12));
  border: 1px solid var(--border);
}

.guide-icon {
  font-size: 18px;
}

.guide-text h4 {
  margin: 0;
  font-size: 12.5px;
  color: var(--amber, #d97706);
}

.guide-text p {
  margin: 2px 0 0;
  font-size: 11px;
  color: var(--text-dim);
}

.guide-btn {
  margin-left: auto;
  flex-shrink: 0;
}

/* 快捷 Chips */
.f-chips-wrapper {
  padding: 10px 16px;
  background: var(--surface-2);
  border-bottom: 1px solid var(--border);
}

.f-chips-track {
  display: flex;
  gap: 8px;
  overflow-x: auto;
  padding-bottom: 4px;
  scrollbar-width: thin;
}

.f-chips-track::-webkit-scrollbar {
  height: 3px;
}

.f-chips-track::-webkit-scrollbar-thumb {
  background: var(--border-strong);
  border-radius: 3px;
}

.chip-pill {
  position: relative;
  display: inline-flex;
  align-items: center;
  padding: 5px 12px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--surface);
  color: var(--text);
  font-size: 12px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.15s ease;
}

.chip-pill:hover:not(:disabled) {
  border-color: var(--accent);
  background: var(--accent-soft);
  color: var(--accent);
  transform: translateY(-1px);
}

/* 消息流区域 */
.f-messages-container {
  flex: 1;
  overflow-y: auto;
  overflow-x: hidden;
  padding: 16px;
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 0;
  max-width: 100%;
}

.msg-bubble-group {
  display: flex;
  gap: 10px;
  min-width: 0;
  max-width: 100%;
}

.msg-bubble-group.role-user {
  flex-direction: row-reverse;
}

.msg-avatar {
  flex-shrink: 0;
}

.assistant-avatar-badge {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: var(--shadow-accent);
}

.assistant-avatar-badge.pulsing {
  animation: pulseGlow 1.5s infinite alternate;
}

@keyframes pulseGlow {
  0% { transform: scale(0.95); opacity: 0.8; }
  100% { transform: scale(1.05); opacity: 1; }
}

.user-avatar-badge {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--surface-3);
  border: 1px solid var(--border);
  color: var(--text);
  font-size: 11px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.msg-card {
  flex: 1;
  min-width: 0;
  max-width: calc(100% - 38px);
  overflow-wrap: break-word;
  word-break: break-word;
}

.role-user .msg-card {
  background: var(--accent-soft);
  border: 1px solid var(--accent-border);
  padding: 10px 14px;
  border-radius: var(--radius, 10px);
  border-top-right-radius: 2px;
}

.role-assistant .msg-card {
  background: var(--surface-2, #282b31);
  border: 1px solid var(--border);
  padding: 12px 14px;
  border-radius: var(--radius, 10px);
  border-top-left-radius: 2px;
}

.msg-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  gap: 8px;
}

.msg-sender {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--text-dim);
}

.msg-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.tag-cache {
  font-size: 10px;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--green-soft);
  color: var(--green);
  border: 1px solid var(--green);
}

.btn-text-action {
  background: none;
  border: none;
  color: var(--text-dim);
  font-size: 11px;
  cursor: pointer;
  padding: 2px 4px;
  border-radius: 4px;
}

.btn-text-action:hover {
  color: var(--text);
  background: var(--surface-3);
}

.msg-markdown {
  font-size: 13.5px;
  line-height: 1.65;
  color: var(--text);
  min-width: 0;
  max-width: 100%;
  overflow-wrap: break-word;
  word-break: break-word;
}

/* 严格约束所有 Markdown 内部元素不超出 */
.msg-markdown :deep(pre) {
  max-width: 100% !important;
  box-sizing: border-box !important;
  overflow-x: auto !important;
  white-space: pre-wrap !important;
  word-break: break-all !important;
  background: var(--bg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 6px !important;
  padding: 10px 12px !important;
  margin: 8px 0 !important;
  font-size: 12.5px !important;
  line-height: 1.5 !important;
  color: var(--text) !important;
}

.msg-markdown :deep(code) {
  font-family: var(--mono) !important;
  font-size: 12.5px !important;
  word-break: break-word !important;
}

.msg-markdown :deep(p),
.msg-markdown :deep(ul),
.msg-markdown :deep(ol),
.msg-markdown :deep(li),
.msg-markdown :deep(blockquote) {
  max-width: 100% !important;
  overflow-wrap: break-word !important;
  word-break: break-word !important;
  margin: 6px 0 !important;
  color: var(--text);
}

.msg-markdown :deep(h1),
.msg-markdown :deep(h2),
.msg-markdown :deep(h3),
.msg-markdown :deep(h4) {
  max-width: 100% !important;
  overflow-wrap: break-word !important;
  word-break: break-word !important;
  color: var(--text) !important;
  margin: 12px 0 6px 0 !important;
}

.msg-markdown :deep(table) {
  display: block !important;
  max-width: 100% !important;
  overflow-x: auto !important;
  border-collapse: collapse !important;
  margin: 8px 0 !important;
}

.msg-markdown :deep(th),
.msg-markdown :deep(td) {
  border: 1px solid var(--border) !important;
  padding: 6px 10px !important;
  font-size: 12px !important;
  color: var(--text);
}

/* 底部编辑器 */
.f-bottom-composer {
  padding: 14px 16px;
  border-top: 1px solid var(--border);
  background: var(--surface-2);
}

.composer-box {
  border: 1px solid var(--border);
  border-radius: 8px;
  background: var(--surface);
  padding: 8px 10px;
  transition: border-color 0.2s, box-shadow 0.2s;
}

.composer-box:focus-within {
  border-color: var(--accent);
  box-shadow: 0 0 0 2px var(--accent-soft);
}

.composer-textarea {
  width: 100%;
  border: none;
  background: transparent;
  color: var(--text);
  font-size: 13px;
  line-height: 1.5;
  resize: none;
  outline: none;
  padding: 2px;
}

.composer-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 4px;
  padding-top: 6px;
  border-top: 1px solid var(--border);
}

.status-shield {
  font-size: 11px;
  color: var(--text-dim);
  font-family: var(--mono);
  display: flex;
  align-items: center;
  gap: 4px;
}

.status-shield.token-normal {
  color: var(--text-dim);
}

.status-shield.token-warning {
  color: var(--amber);
  font-weight: 600;
}

.status-shield.token-danger {
  color: var(--red);
  font-weight: 700;
}

.composer-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.btn-send {
  width: 28px;
  height: 28px;
  border-radius: 6px;
  border: none;
  background: var(--accent);
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  transition: background 0.15s, transform 0.15s;
}

.btn-send:hover:not(:disabled) {
  background: var(--accent-hover);
  transform: translateY(-1px);
}

.btn-send:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}

.btn-stop {
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid var(--red);
  background: var(--red-soft);
  color: var(--red);
  font-size: 11px;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 4px;
}

.typing-cursor {
  display: inline-block;
  width: 6px;
  height: 14px;
  background: var(--accent);
  margin-left: 4px;
  vertical-align: middle;
  animation: blink 1s infinite;
}

.f-resize-corner {
  position: absolute;
  right: 3px;
  bottom: 3px;
  color: var(--text-faint);
  pointer-events: none;
  user-select: none;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}

@media (max-width: 768px) {
  .floating-capsule {
    bottom: 16px;
    right: 16px;
  }
  .floating-window {
    left: 0 !important;
    top: auto !important;
    bottom: 0 !important;
    width: 100vw !important;
    height: 82vh !important;
    border-radius: 16px 16px 0 0;
    max-width: 100vw;
    resize: none;
  }
}
</style>
