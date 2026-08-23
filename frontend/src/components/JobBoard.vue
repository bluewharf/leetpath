<template>
  <div>
    <div v-if="loading" class="empty">加载中…</div>
    <div v-else-if="jobs.length === 0" class="empty">暂无岗位，等管理员录入</div>
    <template v-else>
      <div v-if="!limit" class="filters job-filters">
        <input v-model="q" class="input" placeholder="搜索岗位关键词，如 AI应用 / 算法 / 后端" />
        <select v-model="tier" class="select">
          <option value="">全部规模</option>
          <option value="big">大厂</option>
          <option value="mid">中厂</option>
          <option value="small">小厂</option>
        </select>
        <select v-model="company" class="select">
          <option value="">全部公司</option>
          <option v-for="c in companies" :key="c" :value="c">{{ c }}</option>
        </select>
        <label class="job-open-only">
          <input type="checkbox" v-model="openOnly" /> 只看在招
        </label>
        <span class="problem-limits" style="margin-left:auto">{{ filtered.length }} / {{ jobs.length }} 岗</span>
      </div>
      <div v-if="filtered.length === 0" class="empty">没有匹配的岗位</div>
      <section v-for="g in grouped" :key="g.key" class="tier-section">
        <div class="tier-head">
          <h2>{{ g.label }}</h2>
          <span class="tier-count num">{{ g.items.length }}</span>
        </div>
        <div class="job-grid">
          <div v-for="job in g.items" :key="job.id" class="card job-card" :class="{ 'is-closed': isClosed(job) }">
            <div class="job-top">
              <span class="job-tile" :style="tileStyle(job.company)">{{ job.company.slice(0, 1) }}</span>
              <div class="job-head">
                <span class="job-company">{{ job.company }}</span>
                <span class="job-pos">{{ job.position }}</span>
              </div>
              <span class="dday" :class="ddayClass(job)">{{ ddayText(job) }}</span>
            </div>
            <div class="job-meta">
              <span v-if="job.batch" class="badge badge-source">{{ job.batch }}</span>
              <span v-if="job.open_at">开投 {{ job.open_at }}</span>
              <span v-if="job.deadline_at">截止 {{ job.deadline_at }}</span>
            </div>
            <div v-if="job.jd_text">
              <a v-if="!expanded.has(job.id)" href="javascript:;" @click="toggle(job.id)">展开 JD ▾</a>
              <div v-else>
                <div class="job-jd">{{ job.jd_text }}</div>
                <a href="javascript:;" @click="toggle(job.id)">收起 ▴</a>
              </div>
            </div>
            <div class="job-actions">
              <a v-if="job.apply_url" class="btn btn-sm btn-primary" :href="job.apply_url" target="_blank" rel="noopener">投递入口 ↗</a>
              <slot name="actions" :job="job"></slot>
            </div>
          </div>
        </div>
      </section>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { api } from '../api'
import type { Job } from '../types'

const props = defineProps<{ limit?: number }>()

const jobs = ref<Job[]>([])
const loading = ref(true)
const expanded = ref(new Set<number>())
const q = ref('')
const tier = ref('')
const company = ref('')
const openOnly = ref(true)

const companies = computed(() => [...new Set(jobs.value.map((j) => j.company))].sort())

const filtered = computed(() => {
  const kw = q.value.trim().toLowerCase()
  return jobs.value.filter((j) => {
    if (tier.value && (j.tier ?? 'small') !== tier.value) return false
    if (company.value && j.company !== company.value) return false
    if (openOnly.value && isClosed(j)) return false
    if (
      kw &&
      !j.position.toLowerCase().includes(kw) &&
      !j.company.toLowerCase().includes(kw) &&
      !(j.jd_text ?? '').toLowerCase().includes(kw)
    )
      return false
    return true
  })
})

const shown = computed(() =>
  props.limit ? filtered.value.slice(0, props.limit) : filtered.value,
)

const TIER_ORDER = [
  { key: 'big', label: '大厂' },
  { key: 'mid', label: '中厂' },
  { key: 'small', label: '小厂' },
] as const

const grouped = computed(() =>
  TIER_ORDER.map((t) => ({
    ...t,
    items: shown.value.filter((j) => (j.tier ?? 'small') === t.key),
  })).filter((g) => g.items.length > 0),
)

function isClosed(job: Job) {
  return job.status === 'closed' || (job.days_left !== null && job.days_left < 0)
}

function ddayText(job: Job) {
  if (job.status === 'closed') return '已关闭'
  if (job.days_left === null) return '长期'
  if (job.days_left < 0) return '已截止'
  if (job.days_left === 0) return '今天截止'
  return `D-${job.days_left}`
}

function ddayClass(job: Job) {
  if (isClosed(job)) return 'closed'
  if (job.days_left !== null && job.days_left <= 7) return 'urgent'
  return 'ok'
}

function tileStyle(company: string) {
  let h = 0
  for (const ch of company) h = (h * 31 + ch.codePointAt(0)!) % 360
  return {
    background: `hsl(${h} 65% 55% / 0.14)`,
    color: `hsl(${h} 70% 62%)`,
    border: `1px solid hsl(${h} 65% 55% / 0.25)`,
  }
}

function toggle(id: number) {
  const s = new Set(expanded.value)
  if (s.has(id)) s.delete(id)
  else s.add(id)
  expanded.value = s
}

async function load() {
  loading.value = true
  try {
    jobs.value = await api.get<Job[]>('/api/jobs')
  } finally {
    loading.value = false
  }
}

defineExpose({ reload: load })
onMounted(load)
</script>
