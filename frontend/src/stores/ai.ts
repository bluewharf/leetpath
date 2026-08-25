import { computed, ref } from 'vue'

export interface AiMessage {
  role: 'system' | 'user' | 'assistant'
  content: string
}

export interface AiPreset {
  name: string
  url: string
  defaultModel?: string
  placeholder?: string
}

export const AI_PRESETS: AiPreset[] = [
  {
    name: 'Antithor 专属中转站 (默认)',
    url: 'https://api.antithor.asia/v1',
  },
  {
    name: 'DeepSeek 官方',
    url: 'https://api.deepseek.com/v1',
    defaultModel: 'deepseek-chat',
  },
]

const STORAGE_KEY = 'leetpath_ai_config'
const CACHE_STORAGE_KEY = 'leetpath_ai_response_cache_v1'

interface AiConfig {
  baseUrl: string
  apiKey: string
  model: string
  modelsList: string[]
  temperature: number
  maxContextTurns: number // 上下文轮数约束，默认 2~3 轮以极大节省 Token
  enableLocalCache: boolean // 是否开启响应本地缓存
}

interface CacheItem {
  content: string
  model: string
  timestamp: number
}

// 读取配置
const savedConfig: Partial<AiConfig> = (() => {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
})()

const baseUrl = ref<string>(savedConfig.baseUrl || 'https://api.antithor.asia/v1')
const apiKey = ref<string>(savedConfig.apiKey || '')
const selectedModel = ref<string>(savedConfig.model || 'claude-3-5-sonnet-20241022')
const modelsList = ref<string[]>(savedConfig.modelsList || [
  'claude-3-5-sonnet-20241022',
  'deepseek-chat',
  'deepseek-reasoner',
  'gpt-4o',
  'gpt-4o-mini',
  'qwen-2.5-coder-32b',
])
const temperature = ref<number>(savedConfig.temperature ?? 0.7)
const maxContextTurns = ref<number>(savedConfig.maxContextTurns ?? 2)
const enableLocalCache = ref<boolean>(savedConfig.enableLocalCache ?? true)

// 读取本地问答响应缓存
function getCacheMap(): Record<string, CacheItem> {
  try {
    const raw = localStorage.getItem(CACHE_STORAGE_KEY)
    return raw ? JSON.parse(raw) : {}
  } catch {
    return {}
  }
}

function saveCacheMap(map: Record<string, CacheItem>) {
  try {
    localStorage.setItem(CACHE_STORAGE_KEY, JSON.stringify(map))
  } catch {
    // 若超限清空旧缓存
    const keys = Object.keys(map)
    if (keys.length > 50) {
      const trimmed: Record<string, CacheItem> = {}
      keys.slice(-30).forEach((k) => {
        const item = map[k]
        if (item) trimmed[k] = item
      })
      localStorage.setItem(CACHE_STORAGE_KEY, JSON.stringify(trimmed))
    }
  }
}

const isConfigured = computed(() => {
  return baseUrl.value.trim().length > 0 && apiKey.value.trim().length > 0 && selectedModel.value.trim().length > 0
})

function saveConfig() {
  const cfg: AiConfig = {
    baseUrl: baseUrl.value.trim(),
    apiKey: apiKey.value.trim(),
    model: selectedModel.value.trim(),
    modelsList: modelsList.value,
    temperature: temperature.value,
    maxContextTurns: maxContextTurns.value,
    enableLocalCache: enableLocalCache.value,
  }
  localStorage.setItem(STORAGE_KEY, JSON.stringify(cfg))
}

function extractModelNames(data: any): string[] {
  const models = new Set<string>()

  function tryAdd(val: any) {
    if (!val) return
    if (typeof val === 'string') {
      const s = val.trim()
      if (s && s.length < 120) models.add(s)
    } else if (typeof val === 'object') {
      const name = val.id || val.name || val.model || val.model_name || val.slug || val.value
      if (typeof name === 'string' && name.trim()) {
        models.add(name.trim())
      }
    }
  }

  if (Array.isArray(data)) {
    data.forEach(tryAdd)
  } else if (data && typeof data === 'object') {
    if (Array.isArray(data.data)) {
      data.data.forEach(tryAdd)
    } else if (Array.isArray(data.models)) {
      data.models.forEach(tryAdd)
    } else if (Array.isArray(data.result)) {
      data.result.forEach(tryAdd)
    } else if (Array.isArray(data.items)) {
      data.items.forEach(tryAdd)
    } else if (Array.isArray(data.model_list)) {
      data.model_list.forEach(tryAdd)
    } else if (data.data && typeof data.data === 'object') {
      Object.keys(data.data).forEach(tryAdd)
    } else if (data.models && typeof data.models === 'object') {
      Object.keys(data.models).forEach(tryAdd)
    }
  }

  return Array.from(models)
}

export function useAiStore() {
  /**
   * 一键拉取中转站 / 官方 API 提供的全部可用模型列表 (通过后端安全代理，完美解决浏览器跨域与预检拦截)
   */
  async function fetchModels(): Promise<string[]> {
    if (!baseUrl.value.trim()) {
      throw new Error('请先填写 Base URL')
    }
    if (!apiKey.value.trim()) {
      throw new Error('请先填写 API Key')
    }

    const res = await fetch('/api/ai/models', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        base_url: baseUrl.value.trim(),
        api_key: apiKey.value.trim(),
      }),
    })

    if (!res.ok) {
      const errJson = await res.json().catch(() => ({}))
      throw new Error(errJson.detail || `获取模型列表失败 (${res.status})`)
    }

    const data = await res.json()
    const list = extractModelNames(data)

    if (list.length === 0) {
      throw new Error('中转站未返回模型列表，请检查 Key 权限或直接在下方输入框中手动填写模型名称')
    }

    list.sort((a, b) => a.localeCompare(b))
    modelsList.value = list
    if (!list.includes(selectedModel.value)) {
      selectedModel.value = list[0] || 'claude-3-5-sonnet-20241022'
    }
    saveConfig()
    return list
  }

  /**
   * 本地响应缓存查询：根据 contextKey + prompt + model
   */
  function getCachedAnswer(contextKey: string, prompt: string, model?: string): string | null {
    if (!enableLocalCache.value) return null
    const map = getCacheMap()
    const targetModel = model || selectedModel.value
    const key = `${contextKey}:::${prompt.trim()}:::${targetModel}`
    const item = map[key]
    return item ? item.content : null
  }

  /**
   * 写入本地响应缓存
   */
  function setCachedAnswer(contextKey: string, prompt: string, content: string, model?: string) {
    if (!enableLocalCache.value || !content.trim()) return
    const map = getCacheMap()
    const targetModel = model || selectedModel.value
    const key = `${contextKey}:::${prompt.trim()}:::${targetModel}`
    map[key] = {
      content,
      model: targetModel,
      timestamp: Date.now(),
    }
    saveCacheMap(map)
  }

  /**
   * 清空所有本地 AI 响应缓存
   */
  function clearAllCache() {
    localStorage.removeItem(CACHE_STORAGE_KEY)
  }

  /**
   * 获取当前已缓存条目数
   */
  function getCacheCount(): number {
    const map = getCacheMap()
    return Object.keys(map).length
  }

  /**
   * 发起流式对话（通过透明代理 + 严格上下文约束 + 前缀缓存优化）
   */
  async function streamChat(
    messages: AiMessage[],
    onChunk: (chunk: string) => void,
    signal?: AbortSignal,
  ): Promise<string> {
    if (!isConfigured.value) {
      throw new Error('请先在顶部「🤖 AI 设置」中配置 API Key 与模型')
    }

    // 上下文约束：保留 system 提示词 + 最近 maxContextTurns 轮（1轮=1user+1assistant），防止无限膨胀 Token
    const systemMsg = messages.find((m) => m.role === 'system')
    const historyMsgs = messages.filter((m) => m.role !== 'system')
    const maxHistoryCount = Math.max(1, maxContextTurns.value * 2)
    const trimmedHistory = historyMsgs.slice(-maxHistoryCount)

    const finalMessages: AiMessage[] = []
    if (systemMsg) finalMessages.push(systemMsg)
    finalMessages.push(...trimmedHistory)

    const res = await fetch('/api/ai/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        base_url: baseUrl.value.trim(),
        api_key: apiKey.value.trim(),
        model: selectedModel.value.trim(),
        messages: finalMessages,
        temperature: temperature.value,
      }),
      signal,
    })

    if (!res.ok) {
      const errJson = await res.json().catch(() => ({}))
      throw new Error(errJson.detail || `AI 请求失败 [${res.status}]`)
    }

    if (!res.body) {
      throw new Error('返回数据流为空')
    }

    const reader = res.body.getReader()
    const decoder = new TextDecoder('utf-8')
    let fullText = ''
    let buffer = ''

    try {
      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          const trimmed = line.trim()
          if (!trimmed || trimmed.startsWith(':')) continue
          if (trimmed === 'data: [DONE]') continue

          if (trimmed.startsWith('data:')) {
            const jsonStr = trimmed.slice(5).trim()
            try {
              const parsed = JSON.parse(jsonStr)
              const delta = parsed.choices?.[0]?.delta
              const content = delta?.content || delta?.reasoning_content || ''
              if (content) {
                fullText += content
                onChunk(content)
              }
            } catch {
              // 容错
            }
          }
        }
      }
    } finally {
      reader.releaseLock()
    }

    return fullText
  }

  return {
    baseUrl,
    apiKey,
    selectedModel,
    modelsList,
    temperature,
    maxContextTurns,
    enableLocalCache,
    isConfigured,
    saveConfig,
    fetchModels,
    getCachedAnswer,
    setCachedAnswer,
    clearAllCache,
    getCacheCount,
    streamChat,
  }
}
