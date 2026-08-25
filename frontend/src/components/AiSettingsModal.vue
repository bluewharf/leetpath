<template>
  <div class="modal-backdrop" @click.self="$emit('close')">
    <div class="modal card ai-modal">
      <div class="modal-header">
        <div>
          <div class="kicker">BYOK · OpenAI Compatible</div>
          <h2>🤖 AI 导师与大模型接入设置</h2>
        </div>
        <button class="btn btn-xs btn-ghost" @click="$emit('close')">✕</button>
      </div>

      <div class="modal-body">
        <p class="muted" style="margin-bottom:16px;font-size:13px">
          默认已接入 <strong>Antithor 专属中转站</strong>（也支持直接切换为 DeepSeek 官方或自定义中转）。密钥和问答缓存仅保存在你的本地浏览器中，绝不上报服务器。
        </p>

        <!-- 快捷预设服务商 -->
        <div class="form-group">
          <label class="form-label">快速预设填入：</label>
          <div class="preset-pills">
            <button
              v-for="p in AI_PRESETS"
              :key="p.name"
              type="button"
              class="preset-pill-btn"
              @click="applyPreset(p)"
            >
              {{ p.name }}
            </button>
          </div>
        </div>

        <!-- Base URL -->
        <div class="form-group">
          <label class="form-label">
            API 接口地址 (Base URL) <span class="req">*</span>
          </label>
          <input
            v-model="ai.baseUrl.value"
            type="text"
            class="input mono"
            placeholder="默认: https://api.antithor.asia/v1"
          />
          <small class="form-help">默认已配置 <code>https://api.antithor.asia/v1</code>，可直接输入 Key 拉取模型</small>
        </div>

        <!-- API Key -->
        <div class="form-group">
          <label class="form-label">
            API 密钥 (API Key) <span class="req">*</span>
          </label>
          <div class="input-with-action">
            <input
              v-model="ai.apiKey.value"
              :type="showKey ? 'text' : 'password'"
              class="input mono"
              placeholder="sk-xxxxxxxxxxxxxxxxxxxxxxxx"
            />
            <button type="button" class="btn btn-xs btn-ghost input-suffix-btn" @click="showKey = !showKey">
              {{ showKey ? '隐藏' : '显示' }}
            </button>
          </div>
        </div>

        <!-- 选用模型与拉取 -->
        <div class="form-group">
          <div class="model-fetch-row">
            <label class="form-label">选用模型 (Model) <span class="req">*</span></label>
            <button
              type="button"
              class="btn btn-xs btn-outline"
              :disabled="fetchingModels"
              @click="onFetchModels"
            >
              <span v-if="fetchingModels">拉取中...</span>
              <span v-else>🔄 一键获取全部可用模型</span>
            </button>
          </div>

          <!-- 自由输入 + 下拉建议组合框 -->
          <div class="model-select-wrap">
            <input
              v-model="ai.selectedModel.value"
              list="models-datalist"
              type="text"
              class="input mono"
              placeholder="可直接手填或从下方选择 (如: claude-3-5-sonnet-20241022, deepseek-chat)"
            />
            <datalist id="models-datalist">
              <option v-for="m in ai.modelsList.value" :key="m" :value="m" />
            </datalist>
          </div>

          <!-- 快捷常用高频模型标签 -->
          <div class="quick-model-pills" style="margin-top:8px">
            <span class="muted" style="font-size:11px;margin-right:4px">常用模型直选:</span>
            <button
              type="button"
              class="preset-pill-btn"
              style="font-size:11px;padding:2px 8px"
              @click="ai.selectedModel.value = 'claude-3-5-sonnet-20241022'"
            >
              ⚡ Claude 3.5 Sonnet
            </button>
            <button
              type="button"
              class="preset-pill-btn"
              style="font-size:11px;padding:2px 8px"
              @click="ai.selectedModel.value = 'deepseek-chat'"
            >
              🚀 DeepSeek-V3
            </button>
            <button
              type="button"
              class="preset-pill-btn"
              style="font-size:11px;padding:2px 8px"
              @click="ai.selectedModel.value = 'deepseek-reasoner'"
            >
              🧠 DeepSeek-R1 (思考模式)
            </button>
            <button
              type="button"
              class="preset-pill-btn"
              style="font-size:11px;padding:2px 8px"
              @click="ai.selectedModel.value = 'gpt-4o'"
            >
              🪐 GPT-4o
            </button>
            <button
              type="button"
              class="preset-pill-btn"
              style="font-size:11px;padding:2px 8px"
              @click="ai.selectedModel.value = 'grok-2-latest'"
            >
              ⚡ Grok 2
            </button>
          </div>

          <small v-if="ai.modelsList.value.length > 0" class="form-help" style="color:var(--green);margin-top:6px">
            ✓ 已从中转站自动识别 {{ ai.modelsList.value.length }} 个模型（输入框支持模糊联想与手动自由输入）
          </small>
        </div>

        <!-- Token 节省与上下文约束设置 -->
        <div class="token-saving-card">
          <div class="saving-card-head">
            <span class="saving-title">⚡ Token 节省与性能约束</span>
          </div>

          <!-- 上下文轮数约束 -->
          <div class="form-group" style="margin-bottom:12px">
            <div style="display:flex;justify-content:space-between">
              <label class="form-label" style="font-size:13px">上下文记忆深度 (Context Turns)</label>
              <span class="mono" style="font-size:13px;color:var(--accent)">{{ ai.maxContextTurns.value }} 轮 ({{ ai.maxContextTurns.value * 2 }}条消息)</span>
            </div>
            <input
              v-model.number="ai.maxContextTurns.value"
              type="range"
              min="1"
              max="5"
              step="1"
              class="range-slider"
            />
            <small class="form-help">限制每次提问只附带最近 {{ ai.maxContextTurns.value }} 轮对话，防止多轮追问后 Token 消耗呈指数级膨胀</small>
          </div>

          <!-- 本地响应缓存开关 -->
          <div class="cache-control-row">
            <label class="quiz-switch-label" style="font-weight:500;color:var(--text)">
              <input type="checkbox" v-model="ai.enableLocalCache.value" />
              <span>开启本地回答智能缓存 (Local Response Cache)</span>
            </label>
            <div class="cache-stats-row">
              <span class="cache-count-badge mono">已缓存 {{ cacheCount }} 条回答</span>
              <button
                v-if="cacheCount > 0"
                type="button"
                class="btn btn-xs btn-ghost"
                style="color:var(--red)"
                @click="onClearCache"
              >
                清空缓存
              </button>
            </div>
          </div>
          <small class="form-help" style="margin-top:4px">
            开启后，再次点击同一道题的同一追问将<strong>直接读取本地缓存秒级展现，0 消耗 Token</strong>。
          </small>
        </div>

        <!-- 温度参数 -->
        <div class="form-group" style="margin-top:16px">
          <div style="display:flex;justify-content:space-between">
            <label class="form-label">发散度 (Temperature)</label>
            <span class="mono" style="font-size:13px;color:var(--accent)">{{ ai.temperature.value }}</span>
          </div>
          <input
            v-model.number="ai.temperature.value"
            type="range"
            min="0"
            max="1.2"
            step="0.1"
            class="range-slider"
          />
          <small class="form-help">0.2~0.5 严谨准确（适合代码找茬），0.7 平衡适中（适合考点发散）</small>
        </div>
      </div>

      <div class="modal-footer">
        <div class="test-feedback">
          <span v-if="testMsg" :class="testSuccess ? 'test-success' : 'test-error'">
            {{ testMsg }}
          </span>
        </div>
        <div class="footer-actions">
          <button type="button" class="btn" :disabled="testing" @click="onTestConnection">
            {{ testing ? '测试中...' : '🔌 测试连通性' }}
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
import { AI_PRESETS, useAiStore, type AiPreset } from '../stores/ai'
import { useToast } from '../stores/toast'

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

<style scoped>
.modal-backdrop {
  position: fixed;
  inset: 0;
  background: rgba(0, 0, 0, 0.65);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
  padding: 16px;
}

.ai-modal {
  width: 100%;
  max-width: 580px;
  max-height: 90vh;
  overflow-y: auto;
  padding: 24px;
}

.modal-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 18px;
}

.form-label {
  display: block;
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 6px;
  color: var(--text);
}

.req {
  color: var(--red);
}

.form-help {
  display: block;
  margin-top: 4px;
  font-size: 12px;
  color: var(--text-dim);
}

.preset-pills {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.preset-pill-btn {
  padding: 4px 10px;
  border-radius: 6px;
  border: 1px solid var(--border);
  background: rgba(255, 255, 255, 0.04);
  color: var(--text);
  font-size: 12px;
  cursor: pointer;
  transition: all 0.15s;
}

.preset-pill-btn:hover {
  border-color: var(--accent);
  background: rgba(var(--accent-rgb, 99, 102, 241), 0.12);
}

.input-with-action {
  position: relative;
  display: flex;
  align-items: center;
}

.input-with-action .input {
  padding-right: 60px;
}

.input-suffix-btn {
  position: absolute;
  right: 6px;
}

.model-fetch-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.token-saving-card {
  border-radius: 8px;
  border: 1px solid rgba(var(--accent-rgb, 99, 102, 241), 0.25);
  background: rgba(var(--accent-rgb, 99, 102, 241), 0.04);
  padding: 14px 16px;
  margin: 18px 0;
}

.saving-card-head {
  margin-bottom: 12px;
}

.saving-title {
  font-weight: 600;
  font-size: 13px;
  color: var(--accent);
}

.cache-control-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
}

.cache-stats-row {
  display: flex;
  align-items: center;
  gap: 8px;
}

.cache-count-badge {
  font-size: 11px;
  padding: 2px 6px;
  border-radius: 4px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid var(--border);
}

.modal-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  margin-top: 24px;
  padding-top: 16px;
  border-top: 1px solid var(--border);
}

.footer-actions {
  display: flex;
  gap: 10px;
}

.test-feedback {
  font-size: 12px;
  max-width: 260px;
}

.test-success {
  color: var(--green);
}

.test-error {
  color: var(--red);
}

.range-slider {
  width: 100%;
  accent-color: var(--accent);
}

.quiz-switch-label {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  cursor: pointer;
  user-select: none;
}
</style>
