import { computed, ref } from 'vue'

export interface ContextPayload {
  source: 'problem' | 'review' | 'quiz' | 'general'
  title: string
  contextKey: string
  contextText: string
  presetPrompts: { label: string; prompt: string }[]
}

const isVisible = ref(false)
const isMaximized = ref(false)
const currentContext = ref<ContextPayload>({
  source: 'general',
  title: 'LeetPath 智能全能技术助教',
  contextKey: 'general',
  contextText: '',
  presetPrompts: [
    { label: '💡 计算机校招高频常考题型有哪些？', prompt: '请帮我梳理大厂校招后端/大模型算法岗最常考的高频核心题型与考点分布。' },
    { label: '🚀 ACM 模式极速 I/O 避坑口诀', prompt: '请总结在 Python 3 和 C++ 下写 ACM 模式输入输出最关键的几个避坑技巧。' },
    { label: '🧠 大模型 Agent 架构核心概念速记', prompt: '请用简洁易懂的结构，梳理 AI Agent 的 Planning、Memory、Tools 核心组件。' },
  ],
})

// 暂存自动发送指令（供页面按钮直达触发）
const pendingPrompt = ref<string | null>(null)

export function useAiAssistant() {
  function openWithContext(ctx: ContextPayload, autoSendPrompt?: string) {
    currentContext.value = ctx
    isVisible.value = true
    if (autoSendPrompt) {
      pendingPrompt.value = autoSendPrompt
    }
  }

  function toggle() {
    isVisible.value = !isVisible.value
  }

  function close() {
    isVisible.value = false
  }

  function toggleMaximize() {
    isMaximized.value = !isMaximized.value
  }

  function setContext(ctx: ContextPayload) {
    currentContext.value = ctx
  }

  return {
    isVisible,
    isMaximized,
    currentContext,
    pendingPrompt,
    openWithContext,
    toggle,
    close,
    toggleMaximize,
    setContext,
  }
}
