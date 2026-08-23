<template>
  <div class="container">
    <div v-if="loading" class="empty">加载中…</div>
    <div v-else-if="!problem" class="empty">题目不存在或未发布</div>
    <template v-else>
      <div class="mobile-tabs">
        <button :class="{ active: tab === 'statement' }" @click="tab = 'statement'">题面</button>
        <button :class="{ active: tab === 'code' }" @click="tab = 'code'">代码</button>
        <button :class="{ active: tab === 'result' }" @click="tab = 'result'">
          结果<span v-if="submission && !isFinal(submission.status)"> ·</span>
        </button>
      </div>

      <div class="problem-layout">
        <!-- 题面 -->
        <section class="pane pane-statement card statement" v-show="isDesktop || tab === 'statement'">
          <h1 style="font-size:20px">{{ problem.title }}</h1>
          <div class="problem-meta">
            <span class="badge" :class="`badge-${problem.difficulty}`">{{ difficultyText }}</span>
            <span class="badge badge-source">{{ problem.source === 'hot100' ? '热题100' : '面经手撕' }}</span>
            <span v-for="t in problem.tags" :key="t" class="badge badge-tag">{{ t }}</span>
          </div>
          <div class="problem-limits">时间限制 {{ problem.time_limit_ms / 1000 }}s · 内存限制 {{ problem.memory_limit_mb }}MB</div>

          <div v-html="statementHtml"></div>

          <div v-for="s in problem.samples" :key="s.ordinal" class="sample-block">
            <h3>样例 {{ s.ordinal }}</h3>
            <div class="tc-detail" style="padding-left:0">
              <div class="io-block">
                <div class="io-label">输入</div>
                <pre>{{ s.input }}</pre>
              </div>
              <div class="io-block">
                <div class="io-label">输出</div>
                <pre>{{ s.expected_output }}</pre>
              </div>
            </div>
          </div>

          <div class="solution-block">
            <a v-if="!showSolution" href="javascript:;" @click="openSolution">查看题解（背题模式）▾</a>
            <template v-else>
              <h3 style="margin-top:22px">题解</h3>
              <div v-if="solutionHtml" v-html="solutionHtml"></div>
              <div v-else class="empty" style="padding:18px 0">{{ solutionHint }}</div>
            </template>
          </div>

          <div class="sub-history" v-if="history.length > 0">
            <h3>我的提交</h3>
            <div v-for="s in history" :key="s.id" class="sub-item">
              <div class="sub-line" @click="toggleHistory(s.id)">
                <StatusBadge :status="s.status" />
                <span class="mono" style="font-size:12px">{{ s.language === 'cpp' ? 'C++' : 'Python3' }}</span>
                <span v-if="s.runtime_ms !== null" style="color:var(--text-faint);font-size:12px">{{ s.runtime_ms }}ms</span>
                <span class="sub-time">{{ formatTime(s.created_at) }}</span>
              </div>
              <pre v-if="expandedHistory.has(s.id) && historyCode[s.id]">{{ historyCode[s.id] }}</pre>
            </div>
          </div>
        </section>

        <!-- 编辑器 + 结果 -->
        <section class="pane pane-right" v-show="isDesktop || tab === 'code' || tab === 'result'">
          <div class="card" v-show="isDesktop || tab === 'code'">
            <div class="editor-toolbar">
              <select v-model="language" class="select" @change="onLanguageChange">
                <option value="python3">Python3</option>
                <option value="cpp">C++</option>
              </select>
              <button class="btn btn-primary btn-sm" :disabled="submitting" @click="submit">
                {{ submitting ? '评测中…' : '提交评测' }}
              </button>
              <span class="save-hint">{{ saveHint }}</span>
            </div>
            <Editor v-model="code" :language="language" />
          </div>

          <div class="card result-panel" v-show="isDesktop || tab === 'result'">
            <div class="result-body">
              <div v-if="!submission" class="empty" style="padding:24px 0">提交后在这里查看评测结果</div>
              <template v-else>
                <div class="result-head">
                  <StatusBadge :status="submission.status" />
                  <span v-if="submission.runtime_ms !== null" class="runtime">总耗时 {{ submission.runtime_ms }}ms</span>
                </div>
                <div v-if="submission.compile_output" class="io-block">
                  <div class="io-label">编译/系统输出</div>
                  <pre class="mono" style="background:var(--surface-2);border:1px solid var(--border);border-radius:7px;padding:8px 10px;font-size:12.5px;white-space:pre-wrap;word-break:break-all">{{ submission.compile_output }}</pre>
                </div>
                <div v-for="tc in submission.detail ?? []" :key="tc.ordinal">
                  <div class="tc-row" :style="tc.is_sample ? 'cursor:pointer' : ''" @click="tc.is_sample && toggleTc(tc.ordinal)">
                    <span class="tc-ord">#{{ tc.ordinal }}</span>
                    <span v-if="tc.is_sample" class="tc-sample">样例</span>
                    <span class="status-pill" :class="`st-${tc.status}`" style="padding:1px 10px;font-size:12px">{{ tc.status }}</span>
                    <span class="tc-time">{{ tc.runtime_ms ?? '-' }}ms</span>
                  </div>
                  <div v-if="tc.is_sample && expandedTc.has(tc.ordinal)" class="tc-detail">
                    <div class="io-block">
                      <div class="io-label">输入</div>
                      <pre>{{ tc.input }}</pre>
                    </div>
                    <div class="io-block">
                      <div class="io-label">期望输出</div>
                      <pre>{{ tc.expected }}</pre>
                    </div>
                    <div class="io-block">
                      <div class="io-label">你的输出</div>
                      <pre>{{ tc.output ?? '(无)' }}</pre>
                    </div>
                  </div>
                  <div v-if="tc.stderr" class="tc-detail">
                    <div class="io-block">
                      <div class="io-label">错误输出</div>
                      <pre>{{ tc.stderr }}</pre>
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </div>
        </section>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import DOMPurify from 'dompurify'
import { marked } from 'marked'
import { api } from '../api'
import Editor from '../components/Editor.vue'
import StatusBadge from '../components/StatusBadge.vue'
import {
  isFinal,
  type Draft,
  type Language,
  type ProblemDetail,
  type Submission,
} from '../types'

const route = useRoute()
const slug = computed(() => route.params.slug as string)

const loading = ref(true)
const problem = ref<ProblemDetail | null>(null)
const language = ref<Language>('python3')
const code = ref('')
const submission = ref<Submission | null>(null)
const submitting = ref(false)
const saveHint = ref('')
const history = ref<Submission[]>([])
const tab = ref<'statement' | 'code' | 'result'>('statement')
const isDesktop = ref(window.innerWidth >= 1024)

const expandedTc = ref(new Set<number>())
const expandedHistory = ref(new Set<number>())
const historyCode = ref<Record<number, string>>({})
const showSolution = ref(false)
const solutionMd = ref('')
const solutionHint = ref('加载中…')

const solutionHtml = computed(() =>
  solutionMd.value
    ? DOMPurify.sanitize(marked.parse(solutionMd.value, { async: false }))
    : '',
)

async function openSolution() {
  showSolution.value = true
  solutionHint.value = '加载中…'
  try {
    const r = await api.get<{ slug: string; solution_md: string }>(
      `/api/problems/${slug.value}/solution`,
    )
    solutionMd.value = r.solution_md
  } catch {
    solutionMd.value = ''
    solutionHint.value = '题解还在生成中，稍后再来'
  }
}

let saveTimer: ReturnType<typeof setTimeout> | null = null
let pollTimer: ReturnType<typeof setTimeout> | null = null
let pollDeadline = 0
let dirty = false

const statementHtml = computed(() =>
  problem.value ? DOMPurify.sanitize(marked.parse(problem.value.statement_md, { async: false })) : '',
)

const difficultyText = computed(() => {
  const d = problem.value?.difficulty
  return d === 'easy' ? '简单' : d === 'medium' ? '中等' : '困难'
})

function formatTime(iso: string) {
  const d = new Date(iso)
  return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function toggleTc(ordinal: number) {
  const s = new Set(expandedTc.value)
  if (s.has(ordinal)) s.delete(ordinal)
  else s.add(ordinal)
  expandedTc.value = s
}

async function toggleHistory(id: number) {
  const s = new Set(expandedHistory.value)
  if (s.has(id)) {
    s.delete(id)
  } else {
    s.add(id)
    if (!historyCode.value[id]) {
      const full = await api.get<Submission>(`/api/submissions/${id}`)
      historyCode.value = { ...historyCode.value, [id]: full.code ?? '' }
    }
  }
  expandedHistory.value = s
}

async function saveDraftNow() {
  if (!problem.value || !dirty) return
  dirty = false
  saveHint.value = '保存中…'
  try {
    await api.put(`/api/drafts/${slug.value}`, { language: language.value, code: code.value })
    const d = new Date()
    saveHint.value = `已保存 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}:${String(d.getSeconds()).padStart(2, '0')}`
  } catch {
    saveHint.value = '保存失败'
  }
}

watch(code, () => {
  dirty = true
  if (saveTimer) clearTimeout(saveTimer)
  saveTimer = setTimeout(saveDraftNow, 1000)
})

async function loadDraft() {
  const draft = await api.get<Draft>(`/api/drafts/${slug.value}?language=${language.value}`)
  code.value = draft.code
  dirty = false
  saveHint.value = draft.is_default ? '' : '草稿已恢复'
}

async function onLanguageChange() {
  if (saveTimer) clearTimeout(saveTimer)
  await saveDraftNow()
  await loadDraft()
}

async function submit() {
  if (!problem.value) return
  if (saveTimer) clearTimeout(saveTimer)
  await saveDraftNow()
  submitting.value = true
  tab.value = 'result'
  try {
    const res = await api.post<{ id: number; status: string }>('/api/submissions', {
      problem_slug: slug.value,
      language: language.value,
      code: code.value,
    })
    submission.value = null
    pollDeadline = Date.now() + 90_000
    poll(res.id)
  } catch (e) {
    alert(e instanceof Error ? e.message : '提交失败')
    submitting.value = false
  }
}

async function poll(id: number) {
  try {
    const s = await api.get<Submission>(`/api/submissions/${id}`)
    submission.value = s
    if (isFinal(s.status)) {
      submitting.value = false
      loadHistory()
      return
    }
  } catch {
    /* 网络抖动，继续轮询 */
  }
  if (Date.now() > pollDeadline) {
    submitting.value = false
    return
  }
  pollTimer = setTimeout(() => poll(id), 800)
}

async function loadHistory() {
  history.value = await api.get<Submission[]>(`/api/submissions?problem_slug=${slug.value}&limit=20`)
}

async function loadAll() {
  loading.value = true
  submission.value = null
  showSolution.value = false
  solutionMd.value = ''
  tab.value = window.innerWidth >= 1024 ? 'code' : 'statement'
  try {
    problem.value = await api.get<ProblemDetail>(`/api/problems/${slug.value}`)
    await Promise.all([loadDraft(), loadHistory()])
  } catch {
    problem.value = null
  } finally {
    loading.value = false
  }
}

function onResize() {
  isDesktop.value = window.innerWidth >= 1024
}

watch(slug, async (n, o) => {
  if (n !== o && o) {
    if (saveTimer) clearTimeout(saveTimer)
    await saveDraftNow()
    await loadAll()
  }
})

onMounted(() => {
  window.addEventListener('resize', onResize)
  loadAll()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
  if (saveTimer) clearTimeout(saveTimer)
  if (pollTimer) clearTimeout(pollTimer)
  saveDraftNow()
})
</script>
