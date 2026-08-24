<template>
  <div class="container" :class="{ 'zen-container': isZen }">
    <div v-if="loading" class="card" style="padding:24px;margin-top:20px">
      <Skeleton :count="1" height="32px" width="40%" radius="6px" gap="14px" />
      <Skeleton :count="3" height="18px" width="85%" radius="6px" gap="10px" />
      <div style="margin-top:30px">
        <Skeleton :count="6" height="24px" width="100%" radius="6px" gap="12px" />
      </div>
    </div>
    <div v-else-if="!problem" class="empty">题目不存在或未发布</div>
    <template v-else>
      <!-- 移动端 Tabs -->
      <div class="mobile-tabs">
        <button :class="{ active: tab === 'statement' }" @click="tab = 'statement'">题面</button>
        <button :class="{ active: tab === 'solution' }" @click="tab = 'solution'">
          题解<span v-if="problem.has_solution"> ·</span>
        </button>
        <button :class="{ active: tab === 'code' }" @click="tab = 'code'">代码</button>
        <button :class="{ active: tab === 'result' }" @click="tab = 'result'">
          结果<span v-if="submission && !isFinal(submission.status)"> ·</span>
        </button>
      </div>

      <!-- 顶部辅助工具栏（全屏/禅模式、计时器） -->
      <div class="workspace-bar">
        <div class="workspace-left">
          <RouterLink to="/problems" class="btn btn-sm back-link">← 返回题库</RouterLink>
          <span class="problem-title-inline">{{ problemHeading(problem) }}</span>
          <span class="badge" :class="`badge-${problem.difficulty}`">{{ difficultyText }}</span>
        </div>

        <div class="workspace-right">
          <!-- 计时器 -->
          <div class="stopwatch-badge" :class="{ running: timerRunning, urgent: timerMode === 'countdown' && timerSeconds <= 300 }">
            <span class="timer-icon">◷</span>
            <span class="timer-text mono">{{ formattedTimer }}</span>
            <button class="timer-btn" :title="timerRunning ? '暂停' : '开始'" @click="toggleTimer">
              {{ timerRunning ? '⏸' : '▶' }}
            </button>
            <button class="timer-btn" title="重置计时器" @click="resetTimer">↺</button>
            <button class="timer-btn mode-btn" :title="timerMode === 'stopwatch' ? '切换为30分钟面试倒计时' : '切换为正向计时'" @click="toggleTimerMode">
              {{ timerMode === 'stopwatch' ? '倒计时' : '正计时' }}
            </button>
          </div>

          <!-- 禅模式切换 -->
          <button class="btn btn-sm zen-btn" :class="{ active: isZen }" :title="isZen ? '退出禅模式 (Esc)' : '开启沉浸禅模式'" @click="isZen = !isZen">
            {{ isZen ? '✕ 退出全屏' : '禅模式' }}
          </button>
        </div>
      </div>

      <div
        class="problem-layout"
        :class="{ 'is-dragging': isDragging }"
        :style="isDesktop ? { gridTemplateColumns: `${splitRatio}% 6px calc(${100 - splitRatio}% - 6px)` } : {}"
      >
        <!-- 左侧面板：题面 / 题解 -->
        <section class="pane pane-statement card statement" v-show="isDesktop || tab === 'statement' || tab === 'solution'">
          <!-- 桌面端左面板 Tab（题面 / 题解思路） -->
          <div class="pane-tab-bar" v-if="isDesktop">
            <button class="pane-tab" :class="{ active: leftPaneTab === 'statement' }" @click="leftPaneTab = 'statement'">
              题目描述
            </button>
            <button class="pane-tab" :class="{ active: leftPaneTab === 'solution' }" @click="leftPaneTab = 'solution'">
              官方题解
            </button>
          </div>

          <!-- 题面内容 -->
          <div v-show="!isDesktop ? tab === 'statement' : leftPaneTab === 'statement'">
            <h1 style="font-size:20px;margin-top:4px">{{ problemHeading(problem) }}</h1>
            <div class="problem-meta">
              <span class="badge" :class="`badge-${problem.difficulty}`">{{ difficultyText }}</span>
              <span class="badge badge-source">{{ problem.source === 'hot100' ? '热题100' : '面经手撕' }}</span>
              <span v-for="t in problem.tags" :key="t" class="badge badge-tag">{{ t }}</span>
            </div>
            <div class="problem-limits">时间限制 {{ problem.time_limit_ms / 1000 }}s · 内存限制 {{ problem.memory_limit_mb }}MB</div>

            <div class="markdown-body" v-html="statementHtml"></div>

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

            <!-- 历史提交记录 -->
            <div class="sub-history" v-if="history.length > 0">
              <h3>我的提交 ({{ history.length }})</h3>
              <div v-for="s in history" :key="s.id" class="sub-item">
                <div class="sub-line" @click="toggleHistory(s.id)">
                  <StatusBadge :status="s.status" />
                  <span class="mono" style="font-size:12px">{{ s.language === 'cpp' ? 'C++' : 'Python3' }}</span>
                  <span v-if="s.runtime_ms !== null" style="color:var(--text-faint);font-size:12px">{{ s.runtime_ms }}ms</span>
                  <span class="sub-time">{{ formatTime(s.created_at) }}</span>
                </div>
                <div v-if="expandedHistory.has(s.id)" class="history-code-box">
                  <div class="history-code-actions">
                    <button class="btn btn-xs" @click.stop="loadCodeIntoEditor(historyCode[s.id], s.language)">
                      载入编辑器
                    </button>
                    <button class="btn btn-xs" @click.stop="copyCode(historyCode[s.id])">
                      复制代码
                    </button>
                  </div>
                  <pre class="history-pre">{{ historyCode[s.id] }}</pre>
                </div>
              </div>
            </div>
          </div>

          <!-- 题解内容 -->
          <div v-show="!isDesktop ? tab === 'solution' : leftPaneTab === 'solution'" class="solution-pane-wrap">
            <h2 style="font-size:18px;margin-top:6px;display:flex;align-items:center;gap:8px">
              <span>{{ problemHeading(problem) }} · 官方题解</span>
            </h2>
            <div v-if="solutionLoading" class="empty" style="padding:24px 0">题解加载中…</div>
            <div v-else-if="solutionHtml" class="markdown-body rc-solution" v-html="solutionHtml"></div>
            <div v-else class="empty" style="padding:24px 0">该题目题解正在整理中…</div>
          </div>
        </section>

        <!-- 桌面端分栏拖拽手柄 -->
        <div
          v-if="isDesktop"
          class="split-resizer"
          :class="{ active: isDragging }"
          title="拖动调整左右分栏宽度"
          @mousedown="onMouseDownResizer"
        >
          <div class="resizer-line"></div>
        </div>

        <!-- 右侧面板：代码编辑器 + 评测结果 -->
        <section class="pane pane-right" v-show="isDesktop || tab === 'code' || tab === 'result'">
          <div class="card" v-show="isDesktop || tab === 'code'">
            <div class="editor-toolbar">
              <!-- 语言由顶栏全局偏好统一控制，此处只读展示 -->
              <span class="editor-lang-label mono" title="在页面右上角切换全局语言">{{ language === 'cpp' ? 'C++ (C++20)' : 'Python3' }}</span>

              <button class="btn btn-primary btn-sm" :disabled="submitting" @click="submit" title="快捷键: Ctrl + Enter">
                {{ submitting ? '评测中…' : '提交评测' }}
              </button>

              <button class="btn btn-sm btn-ghost" @click="confirmResetCode" title="重置为初始模板代码">
                重置
              </button>

              <span class="save-hint" :title="saveHint">{{ saveHint }}</span>
              <span class="shortcut-tip" v-if="isDesktop">Ctrl+Enter 提交 · Ctrl+S 保存</span>
            </div>
            <div class="acm-hint">
              <span>ACM 模式：提交完整程序，自己读 stdin / 打印 stdout，格式以题面「输入 / 输出格式」为准</span>
              <RouterLink to="/handbook" class="acm-hint-link">写法对比 · 极速 I/O 模板 →</RouterLink>
            </div>
            <Editor v-model="code" :language="language" />
          </div>

          <!-- 评测结果面板 -->
          <div class="card result-panel" v-show="isDesktop || tab === 'result'">
            <div class="result-body">
              <div v-if="!submission" class="empty" style="padding:24px 0">
                <p>提交后在这里查看实时评测结果</p>
                <span style="font-size:12px;color:var(--text-faint)">支持 Python 3 & C++ ACM 模式标准输入输出</span>
              </div>
              <template v-else>
                <div class="result-head">
                  <StatusBadge :status="submission.status" />
                  <span v-if="submission.runtime_ms !== null" class="runtime">总耗时 {{ submission.runtime_ms }}ms</span>
                </div>
                <div v-if="submission.compile_output" class="io-block">
                  <div class="io-label">编译 / 系统诊断输出</div>
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
import { api } from '../api'
import Editor from '../components/Editor.vue'
import Skeleton from '../components/Skeleton.vue'
import StatusBadge from '../components/StatusBadge.vue'
import { useToast } from '../stores/toast'
import { useLangPref } from '../stores/pref'
import { useStudyPlan } from '../stores/plan'
import { renderMarkdown, filterSolutionMarkdown } from '../markdown'
import {
  isFinal,
  problemHeading,
  type Draft,
  type Language,
  type ProblemDetail,
  type Submission,
} from '../types'

const route = useRoute()
const slug = computed(() => route.params.slug as string)
const toast = useToast()
const { langPref, setLang } = useLangPref()

const loading = ref(true)
const problem = ref<ProblemDetail | null>(null)
const language = ref<Language>(langPref.value)
const code = ref('')
const submission = ref<Submission | null>(null)
const submitting = ref(false)
const saveHint = ref('')
const history = ref<Submission[]>([])
const tab = ref<'statement' | 'solution' | 'code' | 'result'>('statement')
const leftPaneTab = ref<'statement' | 'solution'>('statement')
const isDesktop = ref(window.innerWidth >= 1024)
const isZen = ref(false)

// 分栏拖拽
const splitRatio = ref(50)
const isDragging = ref(false)

// 计时器状态
const timerSeconds = ref(0)
const timerRunning = ref(false)
const timerMode = ref<'stopwatch' | 'countdown'>('stopwatch')
let timerInterval: ReturnType<typeof setInterval> | null = null

// 题解数据
const solutionMd = ref('')
const solutionLoading = ref(false)

const expandedTc = ref(new Set<number>())
const expandedHistory = ref(new Set<number>())
const historyCode = ref<Record<number, string>>({})

let saveTimer: ReturnType<typeof setTimeout> | null = null
let pollTimer: ReturnType<typeof setTimeout> | null = null
let pollDeadline = 0
let dirty = false

// ACM 极速模板
const DEFAULT_TEMPLATES: Record<Language, string> = {
  python3: `import sys

def solve():
    input_data = sys.stdin.read().split()
    if not input_data:
        return
    # 在此编写解题代码

if __name__ == "__main__":
    solve()
`,
  cpp: `#include <iostream>
#include <vector>
#include <string>
#include <algorithm>
using namespace std;

int main() {
    ios::sync_with_stdio(false);
    cin.tie(nullptr);

    // 在此编写解题代码
    return 0;
}
`,
}

const statementHtml = computed(() =>
  problem.value ? renderMarkdown(problem.value.statement_md) : '',
)

const solutionHtml = computed(() =>
  solutionMd.value ? renderMarkdown(filterSolutionMarkdown(solutionMd.value, language.value)) : '',
)

const difficultyText = computed(() => {
  const d = problem.value?.difficulty
  return d === 'easy' ? '简单' : d === 'medium' ? '中等' : '困难'
})

const formattedTimer = computed(() => {
  const total = Math.max(0, timerSeconds.value)
  const m = Math.floor(total / 60)
  const s = total % 60
  return `${String(m).padStart(2, '0')}:${String(s).padStart(2, '0')}`
})

function formatTime(iso: string) {
  const d = new Date(iso)
  return `${d.getMonth() + 1}/${d.getDate()} ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
}

function toggleTimer() {
  if (timerRunning.value) {
    timerRunning.value = false
    if (timerInterval) clearInterval(timerInterval)
  } else {
    timerRunning.value = true
    timerInterval = setInterval(() => {
      if (timerMode.value === 'stopwatch') {
        timerSeconds.value++
      } else {
        if (timerSeconds.value > 0) {
          timerSeconds.value--
        } else {
          timerRunning.value = false
          if (timerInterval) clearInterval(timerInterval)
          toast.info('⏱️ 30 分钟模拟面试时间到！')
        }
      }
    }, 1000)
  }
}

function resetTimer() {
  timerRunning.value = false
  if (timerInterval) clearInterval(timerInterval)
  timerSeconds.value = timerMode.value === 'stopwatch' ? 0 : 30 * 60
}

function toggleTimerMode() {
  timerMode.value = timerMode.value === 'stopwatch' ? 'countdown' : 'stopwatch'
  resetTimer()
}

// 左右分栏拖拽
function onMouseDownResizer(e: MouseEvent) {
  e.preventDefault()
  isDragging.value = true
  document.body.style.cursor = 'col-resize'
  document.body.style.userSelect = 'none'

  const onMouseMove = (moveEvent: MouseEvent) => {
    if (!isDragging.value) return
    const containerWidth = window.innerWidth
    const newRatio = (moveEvent.clientX / containerWidth) * 100
    if (newRatio >= 25 && newRatio <= 75) {
      splitRatio.value = Math.round(newRatio)
    }
  }

  const onMouseUp = () => {
    isDragging.value = false
    document.body.style.cursor = ''
    document.body.style.userSelect = ''
    localStorage.setItem('leetpath_split_ratio', String(splitRatio.value))
    window.removeEventListener('mousemove', onMouseMove)
    window.removeEventListener('mouseup', onMouseUp)
  }

  window.addEventListener('mousemove', onMouseMove)
  window.addEventListener('mouseup', onMouseUp)
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

function loadCodeIntoEditor(historySnippet: string, lang: Language) {
  if (!historySnippet) return
  if (confirm('确认将此历史提交代码载入到编辑器中吗？当前未保存的修改将被覆盖。')) {
    if (language.value !== lang) setLang(lang)
    code.value = historySnippet
    dirty = true
    saveDraftNow()
    toast.success('已载入历史提交代码')
  }
}

function copyCode(content: string) {
  if (!content) return
  navigator.clipboard.writeText(content)
  toast.success('代码已复制到剪贴板')
}

function confirmResetCode() {
  if (confirm('确定要重置当前代码吗？将恢复为初始默认模板。')) {
    code.value = DEFAULT_TEMPLATES[language.value] || ''
    dirty = true
    saveDraftNow()
    toast.info('代码已重置为初始模板')
  }
}

async function loadSolution() {
  if (solutionMd.value) return
  solutionLoading.value = true
  try {
    const res = await api.get<{ slug: string; solution_md: string }>(
      `/api/problems/${slug.value}/solution`,
    )
    solutionMd.value = res.solution_md
  } catch {
    solutionMd.value = ''
  } finally {
    solutionLoading.value = false
  }
}

async function saveDraftNow() {
  if (!problem.value || !dirty) return
  dirty = false
  saveHint.value = '保存中…'
  try {
    await api.put(`/api/drafts/${slug.value}`, { language: language.value, code: code.value })
    const d = new Date()
    saveHint.value = `已保存 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
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
  if (draft.code && draft.code.trim().length > 0) {
    code.value = draft.code
  } else {
    code.value = DEFAULT_TEMPLATES[language.value] || ''
  }
  dirty = false
  saveHint.value = draft.is_default ? '' : '草稿已恢复'
}

async function onLanguageChange() {
  if (saveTimer) clearTimeout(saveTimer)
  await saveDraftNow()
  await loadDraft()
}

// 全局语言偏好变化时，编辑器语言与草稿同步切换
watch(langPref, async (lang) => {
  if (language.value === lang) return
  language.value = lang
  await onLanguageChange()
})

async function submit() {
  if (!problem.value || submitting.value) return
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
    toast.error(e instanceof Error ? e.message : '提交评测失败')
    submitting.value = false
  }
}

const { recordSolvedProblem, activePlan } = useStudyPlan()

async function poll(id: number) {
  try {
    const s = await api.get<Submission>(`/api/submissions/${id}`)
    submission.value = s
    if (isFinal(s.status)) {
      submitting.value = false
      if (s.status === 'AC') {
        toast.success('恭喜！代码全部通过 (Accepted)')
        if (activePlan.value) {
          recordSolvedProblem(slug.value)
        }
      } else {
        toast.info(`评测完成：状态为 ${s.status}`)
      }
      loadHistory()
      return
    }
  } catch {
    /* 忽略网络抖动 */
  }
  if (Date.now() > pollDeadline) {
    submitting.value = false
    toast.error('评测响应超时，请刷新重试')
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
  solutionMd.value = ''
  tab.value = window.innerWidth >= 1024 ? 'code' : 'statement'
  try {
    problem.value = await api.get<ProblemDetail>(`/api/problems/${slug.value}`)
    await Promise.all([loadDraft(), loadHistory(), loadSolution()])
  } catch {
    problem.value = null
  } finally {
    loading.value = false
  }
}

function onGlobalKeydown(e: KeyboardEvent) {
  if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
    e.preventDefault()
    submit()
  } else if ((e.ctrlKey || e.metaKey) && (e.key === 's' || e.key === 'S')) {
    e.preventDefault()
    saveDraftNow()
    toast.success('草稿已立即保存')
  } else if (e.key === 'Escape') {
    if (isZen.value) isZen.value = false
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
  const savedRatio = localStorage.getItem('leetpath_split_ratio')
  if (savedRatio) {
    const r = parseInt(savedRatio, 10)
    if (!isNaN(r) && r >= 25 && r <= 75) splitRatio.value = r
  }
  window.addEventListener('resize', onResize)
  window.addEventListener('keydown', onGlobalKeydown)
  loadAll()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', onResize)
  window.removeEventListener('keydown', onGlobalKeydown)
  if (saveTimer) clearTimeout(saveTimer)
  if (pollTimer) clearTimeout(pollTimer)
  if (timerInterval) clearInterval(timerInterval)
  saveDraftNow()
})
</script>
