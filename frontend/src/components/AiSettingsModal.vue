<template>
  <div class="ai-modal-backdrop" @click.self="$emit('close')">
    <div class="ai-modal">
      <div class="ai-modal-head">
        <div class="ai-modal-title">
          <span class="ai-modal-icon"><AppIcon name="robot" :size="19" /></span>
          <div>
            <div class="kicker">BYOK · OpenAI Compatible</div>
            <h2>AI 导师与大模型接入设置</h2>
          </div>
        </div>
        <button class="btn btn-xs btn-ghost ai-close" title="关闭" @click="$emit('close')">
          <AppIcon name="x" :size="14" />
        </button>
      </div>

      <div class="ai-modal-body">
        <p class="muted ai-intro">
          默认已接入 <strong>Antithor 专属中转站</strong>。密钥和问答缓存仅保存在你的本地浏览器中，绝不上报服务器。
        </p>

        <!-- 分组：接入中转站 -->
        <section class="ai-group">
          <!-- 预设中转站胶囊组 -->
          <div class="ai-presets">
            <button
              v-for="p in AI_PRESETS"
              :key="p.name"
              type="button"
              class="ai-preset-pill"
              :class="{ active: ai.baseUrl.value === p.url }"
              :title="p.url"
              @click="applyPreset(p)"
            >
              <span class="ai-preset-dot"></span>
              {{ p.name }}
            </button>
          </div>

          <!-- Base URL -->
          <div class="field">
            <label>
              API 接口地址 (Base URL) <span class="ai-req">*</span>
            </label>
            <input
              v-model="ai.baseUrl.value"
              type="text"
              class="input mono"
              placeholder="默认: https://api.antithor.asia/v1"
            />
            <small class="ai-help">默认已配置 <code>https://api.antithor.asia/v1</code>，输入 Key 即可直接拉取并使用全部模型</small>
          </div>

          <!-- API Key -->
          <div class="field">
            <div class="ai-label-row">
              <label>
                API 密钥 (API Key) <span class="ai-req">*</span>
              </label>
              <a
                href="https://api.antithor.asia"
                target="_blank"
                rel="noopener noreferrer"
                class="ai-link"
                title="点击在新窗口打开 Antithor 中转站控制台获取或创建你的 Key"
              >
                点击链接跳转登录 antithor 获取你的 key ↗
              </a>
            </div>
            <div class="ai-input-action">
              <input
                v-model="ai.apiKey.value"
                :type="showKey ? 'text' : 'password'"
                class="input mono"
                placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
              />
              <button
                type="button"
                class="btn btn-xs btn-ghost ai-input-suffix"
                :title="showKey ? '隐藏 Key' : '显示 Key'"
                @click="showKey = !showKey"
              >
                <AppIcon :name="showKey ? 'eye-off' : 'eye'" :size="15" />
              </button>
            </div>
            <small class="ai-help">
              还没有 API Key？请 <a href="https://api.antithor.asia" target="_blank" rel="noopener noreferrer" class="ai-link">点击链接跳转登录 antithor 获取你的 key</a>
            </small>
          </div>
        </section>

        <!-- 分组：选用模型 -->
        <section class="ai-group">
          <div class="field">
            <div class="ai-label-row">
              <label>选用模型 (Model) <span class="ai-req">*</span></label>
              <button
                type="button"
                class="btn btn-xs btn-outline"
                :disabled="fetchingModels"
                @click="onFetchModels"
              >
                <AppIcon name="refresh" :size="12" />
                <span v-if="fetchingModels">拉取中...</span>
                <span v-else>一键获取全部可用模型</span>
              </button>
            </div>

            <!-- 自由输入 + 下拉建议组合框 -->
            <input
              v-model="ai.selectedModel.value"
              list="models-datalist"
              type="text"
              class="input mono"
              placeholder="请输入或点击上方一键拉取 (例如: deepseek-chat, claude-3-5-sonnet...)"
            />
            <datalist id="models-datalist">
              <option v-for="m in ai.modelsList.value" :key="m" :value="m" />
            </datalist>

            <div v-if="ai.modelsList.value.length > 0" class="form-success">
              <AppIcon name="check" :size="13" /> 已从中转站成功识别 {{ ai.modelsList.value.length }} 个可用模型（输入框支持直接搜索与手动输入）
            </div>
          </div>
        </section>

        <!-- 分组：Token 节省与上下文约束设置 -->
        <section class="ai-group">
          <div class="ai-group-title">
            <AppIcon name="sparkle" :size="13" /> 上下文长度限制与 Token 防溢出策略
          </div>

          <!-- 最大输入上下文 Token 预算 -->
          <div class="field">
            <label>最大上下文 Token 预算 (Max Context Tokens)</label>
            <select v-model.number="ai.maxContextTokens.value" class="select mono">
              <option :value="32768">32,768 Tokens (32K · 常用紧凑)</option>
              <option :value="65536">65,536 Tokens (64K · 进阶长文)</option>
              <option :value="131072">131,072 Tokens (128K · 热门长文本 · 默认)</option>
              <option :value="262144">262,144 Tokens (256K · 超大窗口)</option>
              <option :value="524288">524,288 Tokens (500K · 海量上下文)</option>
              <option :value="1048576">1,048,576 Tokens (1M · 百万级全量窗口)</option>
            </select>
            <small class="ai-help">
              内置<strong>滑动窗口智能裁剪算法</strong>：题干与系统核心 Prompt 永远锁定保护，多轮追问超限时自动丢弃最旧历史，<strong>绝不发生 Context Length Exceeded (400) 报错</strong>。
            </small>
          </div>

          <!-- 单次回复最大 Token -->
          <div class="field">
            <label>单次回复最大输出 (Max Response Tokens)</label>
            <select v-model.number="ai.maxResponseTokens.value" class="select mono">
              <option :value="1024">1,024 Tokens (简短答疑)</option>
              <option :value="2048">2,048 Tokens (标准代码与解析)</option>
              <option :value="4096">4,096 Tokens (推荐 · 深度详尽题解)</option>
              <option :value="8192">8,192 Tokens (超长代码生成)</option>
            </select>
          </div>

          <!-- 上下文轮数约束 -->
          <div class="field">
            <div class="ai-label-row">
              <label>对话记忆深度 (Context Turns)</label>
              <span class="mono ai-val">{{ ai.maxContextTurns.value }} 轮 ({{ ai.maxContextTurns.value * 2 }} 条消息)</span>
            </div>
            <input
              v-model.number="ai.maxContextTurns.value"
              type="range"
              min="1"
              max="10"
              step="1"
              class="ai-range"
            />
            <small class="ai-help">限制追问时仅携带最近 {{ ai.maxContextTurns.value }} 轮历史，配合 Token 滑动裁剪，双重防止费用爆炸</small>
          </div>

          <!-- 本地响应缓存开关（iOS 开关） -->
          <div>
            <div class="ai-cache-row">
              <div class="ai-cache-text">
                <span class="ai-cache-title">本地回答智能缓存 (Local Response Cache)</span>
                <small class="ai-help">
                  开启后，再次点击同一道题的同一追问将<strong>直接读取本地缓存秒级展现，0 消耗 Token</strong>。
                </small>
              </div>
              <label class="switch">
                <input type="checkbox" v-model="ai.enableLocalCache.value" />
                <span class="track"></span>
              </label>
            </div>
            <div class="ai-cache-stats">
              <span class="ai-cache-badge mono">已缓存 {{ cacheCount }} 条回答</span>
              <button
                v-if="cacheCount > 0"
                type="button"
                class="btn btn-xs btn-ghost ai-danger"
                @click="onClearCache"
              >
                清空缓存
              </button>
            </div>
          </div>
        </section>

        <!-- 分组：生成参数 -->
        <section class="ai-group">
          <!-- 温度参数 -->
          <div class="field">
            <div class="ai-label-row">
              <label>发散度 (Temperature)</label>
              <span class="mono ai-val">{{ ai.temperature.value }}</span>
            </div>
            <input
              v-model.number="ai.temperature.value"
              type="range"
              min="0"
              max="1.2"
              step="0.1"
              class="ai-range"
            />
            <small class="ai-help">0.2~0.5 严谨准确（适合代码找茬），0.7 平衡适中（适合考点发散）</small>
          </div>

          <div class="field">
            <div class="ai-label-row">
              <label>推理强度 (reasoning_effort)</label>
              <span class="mono ai-val">{{ effortLabel }}</span>
            </div>
            <div class="segmented ai-effort">
              <button
                v-for="opt in REASONING_EFFORT_OPTIONS"
                :key="opt.value"
                type="button"
                :class="{ active: ai.reasoningEffort.value === opt.value }"
                :title="opt.hint"
                @click="ai.reasoningEffort.value = opt.value"
              >
                {{ opt.label }}
              </button>
            </div>
            <small class="ai-help">
              {{ effortHint }}
              发给中转站的字段是 <code>reasoning_effort</code>（low / medium / high / xhigh）。
              型号名带 reasoning / non-reasoning 也可以直接换模型；不支持该参数时请选「关闭」，否则中转站可能报错。
            </small>
          </div>
        </section>
      </div>

      <div class="ai-modal-foot">
        <div class="ai-test-feedback">
          <span v-if="testMsg" :class="testSuccess ? 'form-success' : 'ai-test-err'">
            {{ testMsg }}
          </span>
        </div>
        <div class="ai-foot-actions">
          <button type="button" class="btn" :disabled="testing" @click="onTestConnection">
            <AppIcon name="play" :size="13" />
            {{ testing ? '测试中...' : '测试连通性' }}
          </button>
          <button type="button" class="btn btn-primary" @click="onSave">
            保存并应用
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import { AI_PRESETS, REASONING_EFFORT_OPTIONS, useAiStore, type AiPreset } from '../stores/ai'
import { useToast } from '../stores/toast'
import AppIcon from './AppIcon.vue'

const emit = defineEmits<{
  (e: 'close'): void
}>()

const toast = useToast()
const ai = useAiStore()

const showKey = ref(false)
const fetchingModels = ref(false)
const testing = ref(false)
const testMsg = ref('')
const testSuccess = ref(false)
const modelSearchQuery = ref('')
const cacheCount = ref(ai.getCacheCount())

const effortLabel = computed(() => {
  const found = REASONING_EFFORT_OPTIONS.find((o) => o.value === ai.reasoningEffort.value)
  return found ? found.label : '关闭'
})

const effortHint = computed(() => {
  const found = REASONING_EFFORT_OPTIONS.find((o) => o.value === ai.reasoningEffort.value)
  return found?.hint || ''
})

const filteredModels = computed(() => {
  const q = modelSearchQuery.value.trim().toLowerCase()
  if (!q) return ai.modelsList.value
  return ai.modelsList.value.filter((m) => m.toLowerCase().includes(q))
})

function applyPreset(p: AiPreset) {
  ai.baseUrl.value = p.url
  if (p.defaultModel) {
    ai.selectedModel.value = p.defaultModel
  }
  testMsg.value = ''
  toast.info(`已应用 ${p.name} 预设地址`)
}

async function onFetchModels() {
  if (!ai.baseUrl.value) {
    toast.error('请先填写 Base URL')
    return
  }
  fetchingModels.value = true
  testMsg.value = ''
  try {
    const list = await ai.fetchModels()
    modelSearchQuery.value = ''
    toast.success(`成功识别 ${list.length} 个可用模型！`)
  } catch (err: any) {
    toast.error(err.message || '获取模型列表失败')
  } finally {
    fetchingModels.value = false
  }
}

function onClearCache() {
  ai.clearAllCache()
  cacheCount.value = 0
  toast.success('本地 AI 问答缓存已全部清空')
}

async function onTestConnection() {
  testing.value = true
  testMsg.value = '正在发起测试对话...'
  testSuccess.value = false
  try {
    let result = ''
    await ai.streamChat(
      [
        { role: 'system', content: 'You are a test assistant.' },
        { role: 'user', content: 'Reply "OK" in 2 words.' },
      ],
      (chunk) => {
        result += chunk
      },
    )
    testSuccess.value = true
    testMsg.value = `✓ 连接成功！模型响应: ${result.trim() || 'OK'}`
    toast.success('AI 服务连接正常！')
  } catch (err: any) {
    testSuccess.value = false
    testMsg.value = `✕ 测试失败: ${err.message}`
    toast.error(err.message || '测试连接失败')
  } finally {
    testing.value = false
  }
}

function onSave() {
  ai.saveConfig()
  toast.success('AI 设置与缓存策略已保存！')
  emit('close')
}
</script>

