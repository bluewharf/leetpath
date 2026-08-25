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
        <p class="muted" style="margin-bottom:14px;font-size:13px">
          默认已接入 <strong>Antithor 专属中转站</strong>。密钥和问答缓存仅保存在你的本地浏览器中，绝不上报服务器。
        </p>

        <!-- 专属中转站标识 -->
        <div class="form-group" style="margin-bottom:14px">
          <div class="relay-brand-badge">
            <span class="relay-dot"></span>
            <span class="relay-title">⚡ Antithor 专属中转站 (默认高速通道)</span>
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
          <small class="form-help">默认已配置 <code>https://api.antithor.asia/v1</code>，输入 Key 即可直接拉取并使用全部模型</small>
        </div>

        <!-- API Key -->
        <div class="form-group">
          <div class="label-with-link">
            <label class="form-label" style="margin-bottom:0">
              API 密钥 (API Key) <span class="req">*</span>
            </label>
            <a
              href="https://api.antithor.asia"
              target="_blank"
              rel="noopener noreferrer"
              class="key-portal-link"
              title="点击在新窗口打开 Antithor 中转站控制台获取或创建你的 Key"
            >
              🔗 点击链接跳转登录 antithor 获取你的 key ↗
            </a>
          </div>
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
          <small class="form-help">
            还没有 API Key？请 <a href="https://api.antithor.asia" target="_blank" rel="noopener noreferrer" class="link-highlight">点击链接跳转登录 antithor 获取你的 key</a>
          </small>
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
              placeholder="请输入或点击上方一键拉取 (例如: deepseek-chat, claude-3-5-sonnet...)"
            />
            <datalist id="models-datalist">
              <option v-for="m in ai.modelsList.value" :key="m" :value="m" />
            </datalist>
          </div>

          <small v-if="ai.modelsList.value.length > 0" class="form-help" style="color:var(--green);margin-top:6px">
            ✓ 已从中转站成功识别 {{ ai.modelsList.value.length }} 个可用模型（输入框支持直接搜索与手动输入）
          </small>
        </div>

        <!-- Token 节省与上下文约束设置 -->
        <div class="token-saving-card">
          <div class="saving-card-head">
            <span class="saving-title">⚡ 上下文长度限制与 Token 防溢出策略</span>
          </div>

          <!-- 最大输入上下文 Token 预算 -->
          <div class="form-group" style="margin-bottom:12px">
            <label class="form-label" style="font-size:13px">最大上下文 Token 预算 (Max Context Tokens)</label>
            <select v-model.number="ai.maxContextTokens.value" class="input mono" style="font-size:13px">
              <option :value="32768">32,768 Tokens (32K · 常用紧凑)</option>
              <option :value="65536">65,536 Tokens (64K · 进阶长文)</option>
              <option :value="131072">131,072 Tokens (128K · 热门长文本 · 默认)</option>
              <option :value="262144">262,144 Tokens (256K · 超大窗口)</option>
              <option :value="524288">524,288 Tokens (500K · 海量上下文)</option>
              <option :value="1048576">1,048,576 Tokens (1M · 百万级全量窗口)</option>
            </select>
            <small class="form-help">
              内置<strong>滑动窗口智能裁剪算法</strong>：题干与系统核心 Prompt 永远锁定保护，多轮追问超限时自动丢弃最旧历史，<strong>绝不发生 Context Length Exceeded (400) 报错</strong>。
            </small>
          </div>

          <!-- 单次回复最大 Token -->
          <div class="form-group" style="margin-bottom:12px">
            <label class="form-label" style="font-size:13px">单次回复最大输出 (Max Response Tokens)</label>
            <select v-model.number="ai.maxResponseTokens.value" class="input mono" style="font-size:13px">
              <option :value="1024">1,024 Tokens (简短答疑)</option>
              <option :value="2048">2,048 Tokens (标准代码与解析)</option>
              <option :value="4096">4,096 Tokens (推荐 · 深度详尽题解)</option>
              <option :value="8192">8,192 Tokens (超长代码生成)</option>
            </select>
          </div>

          <!-- 上下文轮数约束 -->
          <div class="form-group" style="margin-bottom:12px">
            <div style="display:flex;justify-content:space-between">
              <label class="form-label" style="font-size:13px">对话记忆深度 (Context Turns)</label>
              <span class="mono" style="font-size:13px;color:var(--accent)">{{ ai.maxContextTurns.value }} 轮 ({{ ai.maxContextTurns.value * 2 }} 条消息)</span>
            </div>
            <input
              v-model.number="ai.maxContextTurns.value"
              type="range"
              min="1"
              max="10"
              step="1"
              class="range-slider"
            />
            <small class="form-help">限制追问时仅携带最近 {{ ai.maxContextTurns.value }} 轮历史，配合 Token 滑动裁剪，双重防止费用爆炸</small>
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

.label-with-link {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  flex-wrap: wrap;
  gap: 6px;
}

.key-portal-link {
  font-size: 12px;
  color: var(--accent);
  text-decoration: none;
  font-weight: 600;
  transition: opacity 0.15s;
}

.key-portal-link:hover {
  text-decoration: underline;
  opacity: 0.85;
}

.link-highlight {
  color: var(--accent);
  text-decoration: underline;
  font-weight: 600;
}

.relay-brand-badge {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 6px 12px;
  border-radius: 6px;
  background: var(--accent-soft);
  border: 1px solid var(--accent-border);
  color: var(--accent);
  font-size: 12.5px;
  font-weight: 600;
}

.relay-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: var(--green, #10b981);
  box-shadow: 0 0 6px var(--green, #10b981);
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
  border: 1px solid var(--accent-border);
  background: var(--accent-soft);
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
