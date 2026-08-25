<template>
  <div class="container">
    <div class="page-head">
      <div>
        <div class="kicker">Review Deck</div>
        <h1 class="display">背题模式</h1>
      </div>
      <div class="head-stats">
        <div class="stat">
          <span class="num accent">{{ rememberedCount }}</span>
          <span class="lbl">已记住</span>
        </div>
        <div class="stat">
          <span class="num">{{ deck.length - rememberedCount }}</span>
          <span class="lbl">待背</span>
        </div>
        <div class="stat">
          <span class="num">{{ deck.length }}</span>
          <span class="lbl">题解总数</span>
        </div>
      </div>
    </div>

    <!-- 顶部进度条 -->
    <div v-if="!loading && deck.length" class="progress-track" style="margin-bottom:24px">
      <div class="seg" :style="{ width: `${(rememberedCount / deck.length) * 100}%`, background: 'var(--accent)' }"></div>
    </div>

    <!-- 语言切换工具栏 -->
    <div class="review-toolbar" v-if="!loading && deck.length > 0">
      <span class="review-lang-hint">当前背题语言：</span>
      <div class="lang-switch-pills">
        <button
          :class="{ active: langPref === 'python3' }"
          @click="setLang('python3')"
        >
          Python 3
        </button>
        <button
          :class="{ active: langPref === 'cpp' }"
          @click="setLang('cpp')"
        >
          C++ 20
        </button>
      </div>
    </div>

    <!-- 骨架屏加载 -->
    <div v-if="loading" class="card" style="padding:32px;max-width:720px;margin:0 auto">
      <Skeleton :count="1" height="32px" width="50%" radius="6px" gap="16px" />
      <Skeleton :count="4" height="20px" width="100%" radius="6px" gap="12px" />
    </div>
    <div v-else-if="deck.length === 0" class="empty">题解还在生成中，稍后再来</div>

    <!-- 背题卡片主体：正面只亮题名，翻开后是「题目 | 题解」对照画布 -->
    <template v-else-if="current">
      <div class="review-stage" :class="{ open: flipped }">
        <transition name="fade" mode="out-in">
          <div
            v-if="!flipped"
            key="front"
            class="card review-card"
            @click="flipped = true"
          >
            <div class="problem-meta" style="justify-content:center;margin:0 0 14px">
              <span class="badge" :class="`badge-${current.difficulty}`">{{ difficultyText(current.difficulty) }}</span>
              <span class="badge badge-source">{{ current.source === 'hot100' ? '热题100' : '面经手撕' }}</span>
              <span v-if="current.memory === 'remembered'" class="badge" style="color:var(--green)">✓ 已记住</span>
            </div>
            <div class="rc-title">{{ problemHeading(current) }}</div>
            <div class="rc-slug mono">{{ current.slug }}</div>
            <div class="rc-tags">{{ current.tags.join(' · ') }}</div>
            <div class="rc-hint">
              点击翻开题目与【{{ langPref === 'cpp' ? 'C++' : 'Python3' }}】题解（Space / Enter）
            </div>
          </div>

          <div v-else key="back" class="review-board">
            <div class="review-canvas-bar">
              <div class="review-canvas-bar-main">
                <div class="problem-meta" style="margin:0 0 8px">
                  <span class="badge" :class="`badge-${current.difficulty}`">{{ difficultyText(current.difficulty) }}</span>
                  <span class="badge badge-source">{{ current.source === 'hot100' ? '热题100' : '面经手撕' }}</span>
                  <span v-if="current.memory === 'remembered'" class="badge" style="color:var(--green)">✓ 已记住</span>
                </div>
                <div class="review-canvas-title">{{ problemHeading(current) }}</div>
                <div class="rc-slug mono" style="margin-top:4px">{{ current.slug }} · {{ current.tags.join(' · ') }}</div>
              </div>
              <div class="review-canvas-bar-actions">
                <button class="btn btn-xs btn-ghost" type="button" @click="flipped = false">↺ 翻回正面</button>
                <RouterLink :to="`/problems/${current.slug}`">去刷这道题 →</RouterLink>
              </div>
            </div>

            <div class="review-spread">
              <section class="review-sheet">
                <div class="review-sheet-label">题目</div>
                <div v-if="payloadLoading && !statementHtml" class="empty" style="padding:28px 0">题面加载中…</div>
                <div v-else class="markdown-body" v-html="statementHtml"></div>
              </section>
              <section class="review-sheet review-sheet-solution">
                <div class="review-sheet-label">题解 · {{ langPref === 'cpp' ? 'C++' : 'Python3' }}</div>
                <div v-if="payloadLoading && !solutionHtml" class="empty" style="padding:28px 0">题解加载中…</div>
                <div v-else class="markdown-body rc-solution" v-html="solutionHtml"></div>
              </section>
            </div>
          </div>
        </transition>

        <div class="review-actions">
          <button class="btn" :disabled="index === 0" @click="go(index - 1)">← 上一张</button>
          <button class="btn" :disabled="marking" @click="mark(false)">没记住</button>
          <button class="btn btn-primary" :disabled="marking" @click="mark(true)">记住了 ✓</button>
          <button class="btn" :disabled="index >= deck.length - 1" @click="go(index + 1)">下一张 →</button>
        </div>
        <div class="review-pos num">{{ index + 1 }} / {{ deck.length }}</div>
      </div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, onMounted, ref } from 'vue'
import { api } from '../api'
import { renderMarkdown, filterSolutionMarkdown } from '../markdown'
import Skeleton from '../components/Skeleton.vue'
import { useLangPref } from '../stores/pref'
import {
  problemHeading,
  type Difficulty,
  type ProblemDetail,
  type ProblemListItem,
} from '../types'

const { langPref, setLang } = useLangPref()

interface ReviewPayload {
  statement_md: string
  solution_md: string
}

const loading = ref(true)
const deck = ref<ProblemListItem[]>([])
const index = ref(0)
const flipped = ref(false)
const marking = ref(false)
const payloadLoading = ref(false)
const payloadCache = new Map<string, ReviewPayload>()
const statementMd = ref('')
const solutionMd = ref('')

const rememberedCount = computed(
  () => deck.value.filter((p) => p.memory === 'remembered').length,
)
const current = computed(() => deck.value[index.value])

const statementHtml = computed(() =>
  statementMd.value ? renderMarkdown(statementMd.value) : '',
)

// 根据用户选择的语言过滤题解内容，只呈现选定语言
const solutionHtml = computed(() => {
  if (!solutionMd.value) return ''
  const filtered = filterSolutionMarkdown(solutionMd.value, langPref.value)
  return renderMarkdown(filtered)
})

function difficultyText(d: Difficulty) {
  return d === 'easy' ? '简单' : d === 'medium' ? '中等' : '困难'
}

async function fetchPayload(slug: string): Promise<ReviewPayload> {
  const hit = payloadCache.get(slug)
  if (hit) return hit
  const [detail, sol] = await Promise.all([
    api.get<ProblemDetail>(`/api/problems/${slug}`),
    api.get<{ slug: string; solution_md: string }>(`/api/problems/${slug}/solution`),
  ])
  const payload: ReviewPayload = {
    statement_md: detail.statement_md,
    solution_md: sol.solution_md,
  }
  payloadCache.set(slug, payload)
  return payload
}

function applyPayload(slug: string, payload: ReviewPayload) {
  if (current.value?.slug !== slug) return
  statementMd.value = payload.statement_md
  solutionMd.value = payload.solution_md
}

async function loadPayload() {
  const c = current.value
  if (!c) return
  const cached = payloadCache.get(c.slug)
  if (cached) {
    applyPayload(c.slug, cached)
    payloadLoading.value = false
    prefetchNeighbor(index.value + 1)
    return
  }
  statementMd.value = ''
  solutionMd.value = ''
  payloadLoading.value = true
  try {
    const payload = await fetchPayload(c.slug)
    applyPayload(c.slug, payload)
  } catch {
    if (current.value?.slug === c.slug) {
      statementMd.value = '题目加载失败'
      solutionMd.value = '题解加载失败'
    }
  } finally {
    if (current.value?.slug === c.slug) payloadLoading.value = false
  }
  prefetchNeighbor(index.value + 1)
}

function prefetchNeighbor(i: number) {
  const n = deck.value[i]
  if (!n || payloadCache.has(n.slug)) return
  void fetchPayload(n.slug).catch(() => undefined)
}

function go(i: number) {
  index.value = i
  flipped.value = false
  loadPayload()
}

async function mark(remembered: boolean) {
  const c = current.value
  if (!c || marking.value) return
  marking.value = true
  try {
    await api.post(`/api/problems/${c.slug}/memory`, { remembered })
    c.memory = remembered ? 'remembered' : 'unremembered'
    if (remembered && index.value < deck.value.length - 1) {
      go(index.value + 1)
    }
  } finally {
    marking.value = false
  }
}

function onKey(e: KeyboardEvent) {
  const tag = (e.target as HTMLElement)?.tagName
  if (tag === 'INPUT' || tag === 'TEXTAREA' || tag === 'BUTTON' || tag === 'A' || tag === 'SELECT') return
  if (e.key === ' ' || e.key === 'Enter') {
    e.preventDefault()
    flipped.value = !flipped.value
  } else if (e.key === 'ArrowLeft' && index.value > 0) go(index.value - 1)
  else if (e.key === 'ArrowRight' && index.value < deck.value.length - 1) go(index.value + 1)
}

onMounted(async () => {
  window.addEventListener('keydown', onKey)
  try {
    const all = await api.get<ProblemListItem[]>('/api/problems')
    const withSol = all.filter((p) => p.has_solution)
    deck.value = withSol.sort((a, b) => {
      const ra = a.memory === 'remembered' ? 1 : 0
      const rb = b.memory === 'remembered' ? 1 : 0
      return ra - rb || a.id - b.id
    })
    await loadPayload()
  } finally {
    loading.value = false
  }
})

onBeforeUnmount(() => window.removeEventListener('keydown', onKey))
</script>
