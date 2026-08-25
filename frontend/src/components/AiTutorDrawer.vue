<template>
  <div v-if="visible" class="drawer-backdrop" @click.self="$emit('close')">
    <div class="drawer card">
      <!-- 头部 -->
      <div class="drawer-head">
        <div class="drawer-title-group">
          <div class="drawer-kicker">AI Tutor & In-Context Assistant</div>
          <h3 class="drawer-title">{{ title || '🤖 AI 导师智能答疑' }}</h3>
        </div>
        <div class="drawer-actions">
          <button class="btn btn-xs" :title="`当前模型: ${ai.selectedModel.value}`" @click="showSettings = true">
            <span class="mono" style="font-size:12px">⚡ {{ ai.selectedModel.value || '未选模型' }}</span>
          </button>
          <button class="btn btn-xs btn-ghost" @click="$emit('close')">✕</button>
        </div>
      </div>

      <!-- 未配置提示 -->
      <div v-if="!ai.isConfigured.value" class="drawer-warning-card">
        <p>⚠️ <strong>尚未配置 AI API Key</strong></p>
        <p class="muted" style="margin:4px 0 10px;font-size:13px">
          支持接入 DeepSeek、硅基流动、Claude、OpenRouter 或自定义中转站。
        </p>
        <button class="btn btn-sm btn-primary" @click="showSettings = true">
          ⚙️ 立即前往配置 Base URL 与 Key
        </button>
      </div>

      <!-- 快捷预设提问 Chips -->
      <div class="quick-prompts-bar" v-if="presetPrompts && presetPrompts.length > 0">
        <span class="quick-lbl">快捷追问：</span>
        <div class="quick-chips">
          <button
            v-for="p in presetPrompts"
            :key="p.label"
            class="chip-btn"
            :disabled="generating"
            @click="onPromptClick(p.prompt)"
          >
            {{ p.label }}
          </button>
        </div>
      </div>

      <!-- 对话消息记录区 -->
      <div class="drawer-messages" ref="msgContainer">
        <div v-for="(msg, idx) in messages" :key="idx" class="chat-bubble" :class="`bubble-${msg.role}`">
          <div class="bubble-avatar">
            {{ msg.role === 'assistant' ? '🤖' : '👤' }}
          </div>
          <div class="bubble-body">
            <div class="bubble-header">
              <span class="bubble-name">{{ msg.role === 'assistant' ? `AI 导师 (${ai.selectedModel.value})` : '我' }}</span>
              <div class="bubble-header-actions" v-if="msg.role === 'assistant'">
                <span v-if="msg.isCached" class="cached-badge" title="从本地浏览器直接秒级载入，未调用网络 API">
                  ⚡ 命中本地缓存 (0 Token)
                </span>
                <button
                  v-if="msg.isCached && msg.originalPrompt"
                  class="btn btn-xs btn-ghost"
                  style="font-size:11px;color:var(--accent)"
                  :disabled="generating"
                  @click="reGenerate(msg.originalPrompt)"
                >
                  🔄 重新生成
                </button>
                <button
                  v-if="msg.content"
                  class="btn btn-xs btn-ghost bubble-copy"
                  @click="copyText(msg.content)"
                >
                  复制
                </button>
              </div>
            </div>
            <div class="statement bubble-markdown" v-html="renderMd(msg.content)"></div>
          </div>
        </div>

        <!-- 正在生成的流式消息 -->
        <div v-if="generating" class="chat-bubble bubble-assistant">
          <div class="bubble-avatar">🤖</div>
          <div class="bubble-body">
            <div class="bubble-header">
              <span class="bubble-name">AI 导师思考中...</span>
            </div>
            <div class="statement bubble-markdown" v-html="renderMd(streamBuffer || '...')"></div>
            <div class="stream-cursor"></div>
          </div>
        </div>
      </div>

      <!-- 底部输入框 -->
      <div class="drawer-input-bar">
        <textarea
          v-model="inputQuestion"
          class="input drawer-textarea"
          placeholder="深入追问这道题或考点... (按 Enter 发送，Shift+Enter 换行)"
          rows="2"
          :disabled="generating"
          @keydown.enter.exact.prevent="onEnterSend"
        ></textarea>
        <div class="input-bottom-row">
          <span class="drawer-hint">已开启上下文约束 (保留近 {{ ai.maxContextTurns.value }} 轮) 与本地缓存</span>
          <button v-if="generating" class="btn btn-sm btn-outline" @click="abort">
            ⏹ 停止生成
          </button>
          <button
            v-else
            class="btn btn-sm btn-primary"
            :disabled="!inputQuestion.trim() || !ai.isConfigured.value"
            @click="onPromptClick(inputQuestion)"
          >
            发送 (Enter)
          </button>
        </div>
      </div>
    </div>

    <!-- AI 设置弹窗 -->
    <AiSettingsModal v-if="showSettings" @close="showSettings = false" />
  </div>
</template>

<script setup lang="ts">
import { nextTick, ref, watch } from 'vue'
import AiSettingsModal from './AiSettingsModal.vue'
import { renderMarkdown } from '../markdown'
import { useAiStore, type AiMessage } from '../stores/ai'
import { useToast } from '../stores/toast'

export interface PromptPreset {
  label: string
  prompt: string
}

interface DrawerMessage extends AiMessage {
  isCached?: boolean
  originalPrompt?: string
}

const props = defineProps<{
  visible: boolean
  title?: string
  contextKey?: string // 用于本地缓存键，如 `quiz:12` 或 `problem:two-sum`
  contextText?: string
  presetPrompts?: PromptPreset[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
}>()

const toast = useToast()
const ai = useAiStore()

const showSettings = ref(false)
const generating = ref(false)
const inputQuestion = ref('')
const streamBuffer = ref('')
const messages = ref<DrawerMessage[]>([])
const msgContainer = ref<HTMLElement | null>(null)
let abortController: AbortController | null = null

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
  onPromptClick(inputQuestion.value)
}

function abort() {
  if (abortController) {
    abortController.abort()
    abortController = null
  }
  generating.value = false
}

// 检查本地缓存或发起请求
async function onPromptClick(userPrompt: string, forceRefresh = false) {
  if (!userPrompt.trim()) return
  if (!ai.isConfigured.value) {
    showSettings.value = true
    return
  }

  const promptText = userPrompt.trim()
  inputQuestion.value = ''

  const cKey = props.contextKey || props.title || 'default'

  // 1. 如果不强制刷新，先检查本地响应缓存！
  if (!forceRefresh && ai.enableLocalCache.value) {
    const cached = ai.getCachedAnswer(cKey, promptText)
    if (cached) {
      messages.value.push({
        role: 'user',
        content: promptText,
      })
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

  // 2. 没有缓存，发起真实流式请求
  messages.value.push({
    role: 'user',
    content: promptText,
  })
  scrollToBottom()

  generating.value = true
  streamBuffer.value = ''
  abortController = new AbortController()

  // 构造标准静态系统前缀（利于服务商端 Prefix/Prompt Caching）
  const sysContent = `你是一位资深的技术面试官与计算机/大模型教学导师。
请针对用户目前正在学习或练习的题目进行清晰、深度、易懂的答疑。
回答风格要求：
1. 深入浅出，善于用直观比喻或实际工业场景说明原理；
2. 如涉及代码，请给出清晰注释；如涉及数学公式，请使用标准 LaTeX 格式（例如 $O(n)$ 或 $$...$$）；
3. 重点突出，条理分明。

【当前学习上下文】：
${props.contextText || '无指定上下文'}`

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

    // 写入本地持久缓存
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

function reGenerate(promptText: string) {
  onPromptClick(promptText, true)
}

// 监听打开时初始化欢迎语
watch(
  () => props.visible,
  (val) => {
    if (val && messages.value.length === 0) {
      messages.value = [
        {
          role: 'assistant',
          content: '👋 你好！我是你的 AI 导师。你可以点击上方的**快捷追问**按钮，或在下方输入你想深入了解的疑问，我将结合这道题为你深度剖析！',
        },
      ]
    }
  },
  { immediate: true },
)
</script>

<style scoped>
.drawer-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.5);
  backdrop-filter: blur(2px);
  z-index: 900;
  display: flex;
  justify-content: flex-end;
}

.drawer {
  width: 100%;
  max-width: 580px;
  height: 100vh;
  border-radius: 0;
  border-left: 1px solid var(--border);
  display: flex;
  flex-direction: column;
  background: var(--bg-card, var(--card));
  box-shadow: -4px 0 24px rgba(0, 0, 0, 0.4);
  animation: slideIn 0.2s ease-out;
}

@keyframes slideIn {
  from {
    transform: translateX(100%);
  }
  to {
    transform: translateX(0);
  }
}

.drawer-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  border-bottom: 1px solid var(--border);
}

.drawer-kicker {
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: var(--accent);
}

.drawer-title {
  margin: 2px 0 0;
  font-size: 16px;
}

.drawer-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}

.drawer-warning-card {
  margin: 16px 20px;
  padding: 14px 16px;
  border-radius: 8px;
  border: 1px solid rgba(245, 158, 11, 0.4);
  background: rgba(245, 158, 11, 0.08);
}

.quick-prompts-bar {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 20px;
  background: rgba(255, 255, 255, 0.02);
  border-bottom: 1px solid var(--border);
  overflow-x: auto;
}

.quick-lbl {
  font-size: 12px;
  color: var(--text-dim);
  white-space: nowrap;
}

.quick-chips {
  display: flex;
  gap: 6px;
  flex-wrap: nowrap;
}

.chip-btn {
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: var(--accent-soft);
  color: var(--text);
  font-size: 12px;
  white-space: nowrap;
  cursor: pointer;
  transition: all 0.15s;
}

.chip-btn:hover:not(:disabled) {
  border-color: var(--accent);
  background: var(--accent-soft);
}

.drawer-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 18px;
}

.chat-bubble {
  display: flex;
  gap: 12px;
}

.bubble-user {
  flex-direction: row-reverse;
}

.bubble-avatar {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.08);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.bubble-body {
  max-width: 86%;
}

.bubble-user .bubble-body {
  background: var(--accent-soft);
  border: 1px solid var(--accent-border);
  padding: 10px 14px;
  border-radius: 10px;
  border-top-right-radius: 2px;
}

.bubble-assistant .bubble-body {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid var(--border);
  padding: 12px 16px;
  border-radius: 10px;
  border-top-left-radius: 2px;
}

.bubble-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  gap: 8px;
}

.bubble-header-actions {
  display: flex;
  align-items: center;
  gap: 6px;
}

.bubble-name {
  font-size: 12px;
  color: var(--text-dim);
  font-weight: 600;
}

.cached-badge {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--green-soft);
  color: var(--green);
  border: 1px solid var(--green);
}

.bubble-markdown {
  font-size: 14px;
  line-height: 1.6;
}

.drawer-input-bar {
  padding: 14px 20px;
  border-top: 1px solid var(--border);
  background: var(--bg);
}

.drawer-textarea {
  width: 100%;
  resize: none;
  font-size: 14px;
  margin-bottom: 8px;
}

.input-bottom-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.drawer-hint {
  font-size: 11px;
  color: var(--text-dim);
}

.stream-cursor {
  display: inline-block;
  width: 6px;
  height: 14px;
  background: var(--accent);
  margin-left: 4px;
  vertical-align: middle;
  animation: blink 1s infinite;
}

@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0; }
}
</style>
