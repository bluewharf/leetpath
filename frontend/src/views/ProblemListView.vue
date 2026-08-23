<template>
  <div class="container">
    <div class="page-head">
      <div>
        <div class="kicker">Problems</div>
        <h1 class="display">题库</h1>
      </div>
      <div class="head-stats">
        <div class="stat">
          <span class="num accent">{{ stats.solved }}</span>
          <span class="lbl">已通过</span>
        </div>
        <div class="stat">
          <span class="num">{{ stats.attempted }}</span>
          <span class="lbl">尝试过</span>
        </div>
        <div class="stat">
          <span class="num">{{ problems.length }}</span>
          <span class="lbl">总题数</span>
        </div>
      </div>
    </div>

    <div v-if="!loading && problems.length" class="progress-track" title="按难度统计已通过">
      <div class="seg easy" :style="{ width: pct(stats.easySolved) }"></div>
      <div class="seg medium" :style="{ width: pct(stats.mediumSolved) }"></div>
      <div class="seg hard" :style="{ width: pct(stats.hardSolved) }"></div>
    </div>

    <div class="filters">
      <input v-model="q" class="input" placeholder="搜索题目标题 / slug" />
      <select v-model="difficulty" class="select">
        <option value="">全部难度</option>
        <option value="easy">简单</option>
        <option value="medium">中等</option>
        <option value="hard">困难</option>
      </select>
      <select v-model="source" class="select">
        <option value="">全部来源</option>
        <option value="hot100">热题 100</option>
        <option value="mianjing">面经手撕</option>
      </select>
      <select v-model="tag" class="select">
        <option value="">全部标签</option>
        <option v-for="t in allTags" :key="t" :value="t">{{ t }}</option>
      </select>
      <span class="problem-limits" style="margin-left:auto">{{ filtered.length }} / {{ problems.length }} 题</span>
    </div>

    <div class="card list-card">
      <div v-if="loading" class="empty">加载中…</div>
      <div v-else-if="filtered.length === 0" class="empty">没有匹配的题目</div>
      <template v-else>
        <div class="list-head">
          <span>#</span>
          <span></span>
          <span>题目</span>
          <span>难度</span>
          <span>来源</span>
          <span>标签</span>
          <span></span>
        </div>
        <RouterLink
          v-for="(p, i) in filtered"
          :key="p.id"
          class="p-row"
          :to="`/problems/${p.slug}`"
        >
          <span class="p-idx">{{ String(i + 1).padStart(2, '0') }}</span>
          <span class="p-check">
            <span v-if="p.my_status === 'solved'" class="solved" title="已通过">✓</span>
            <span v-else-if="p.my_status === 'attempted'" class="attempted" title="尝试过">●</span>
            <span v-else class="todo">·</span>
          </span>
          <span class="p-main">
            <span class="p-title">{{ p.title }}</span>
            <span class="p-slug">{{ p.slug }}</span>
          </span>
          <span class="badge" :class="`badge-${p.difficulty}`">{{ difficultyText(p.difficulty) }}</span>
          <span class="p-src">{{ p.source === 'hot100' ? '热题100' : '面经' }}</span>
          <span class="p-tags">{{ p.tags.slice(0, 3).join(' · ') }}</span>
          <span class="p-arrow">→</span>
        </RouterLink>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { api } from '../api'
import type { Difficulty, ProblemListItem } from '../types'

const problems = ref<ProblemListItem[]>([])
const loading = ref(true)
const q = ref('')
const difficulty = ref('')
const source = ref('')
const tag = ref('')

const allTags = computed(() => {
  const s = new Set<string>()
  problems.value.forEach((p) => p.tags.forEach((t) => s.add(t)))
  return [...s].sort()
})

const stats = computed(() => {
  let solved = 0, attempted = 0, easySolved = 0, mediumSolved = 0, hardSolved = 0
  for (const p of problems.value) {
    if (p.my_status === 'solved') {
      solved++
      if (p.difficulty === 'easy') easySolved++
      else if (p.difficulty === 'medium') mediumSolved++
      else hardSolved++
    } else if (p.my_status === 'attempted') attempted++
  }
  return { solved, attempted, easySolved, mediumSolved, hardSolved }
})

function pct(n: number) {
  return problems.value.length ? `${(n / problems.value.length) * 100}%` : '0%'
}

const filtered = computed(() => {
  const kw = q.value.trim().toLowerCase()
  return problems.value.filter((p) => {
    if (difficulty.value && p.difficulty !== difficulty.value) return false
    if (source.value && p.source !== source.value) return false
    if (tag.value && !p.tags.includes(tag.value)) return false
    if (kw && !p.title.toLowerCase().includes(kw) && !p.slug.includes(kw)) return false
    return true
  })
})

function difficultyText(d: Difficulty) {
  return d === 'easy' ? '简单' : d === 'medium' ? '中等' : '困难'
}

onMounted(async () => {
  try {
    problems.value = await api.get<ProblemListItem[]>('/api/problems')
  } finally {
    loading.value = false
  }
})
</script>
