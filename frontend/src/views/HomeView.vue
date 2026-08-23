<template>
  <div class="container">
    <div class="hero">
      <div class="kicker">LeetPath · 2026/2027 校招刷题与求职神器</div>
      <h1>空余间隙，<span class="grad">刷一道题</span>。</h1>
      <p class="lede">
        精选力扣热题 100 + 面经高频手撕，Python3 / C++ Docker 沙箱真机评测，全量官方题解与背题卡片，秋招大厂岗位聚合雷达。
      </p>

      <div class="hero-stats">
        <div class="hstat">
          <span class="num grad-num">{{ solvedCount }}<span style="font-size:16px;color:var(--text-faint)"> / {{ problemCount }}</span></span>
          <span class="lbl">已通过题数</span>
        </div>
        <div class="hstat">
          <span class="num accent">{{ rememberedCount }}</span>
          <span class="lbl">已记住题解</span>
        </div>
        <div class="hstat">
          <span class="num">{{ openJobCount }}</span>
          <span class="lbl">秋招在招岗位</span>
        </div>
      </div>

      <div class="hero-actions">
        <RouterLink class="btn btn-primary" to="/problems">进入题库 →</RouterLink>
        <button class="btn btn-ghost" @click="pickRandomProblem">🎲 随机刷一题</button>
        <RouterLink class="btn" to="/review">✦ 背题模式</RouterLink>
        <RouterLink class="btn" to="/handbook">📖 新手手册</RouterLink>
      </div>
    </div>

    <!-- 年度打卡热力图卡片 -->
    <div class="card heatmap-card">
      <div class="heatmap-head">
        <div>
          <h3>🔥 刷题活跃度与打卡记录</h3>
          <span class="heatmap-sub">过去 52 周提交记录</span>
        </div>
        <div class="heatmap-streak">
          <span class="streak-tag">持续打卡手感火热</span>
        </div>
      </div>

      <div class="heatmap-scroll-wrap">
        <div class="heatmap-grid">
          <div
            v-for="(day, idx) in heatmapDays"
            :key="idx"
            class="heatmap-cell"
            :class="`level-${day.level}`"
            :title="`${day.date}: ${day.count} 次提交`"
          ></div>
        </div>
      </div>

      <div class="heatmap-legend">
        <span>Less</span>
        <span class="heatmap-cell level-0"></span>
        <span class="heatmap-cell level-1"></span>
        <span class="heatmap-cell level-2"></span>
        <span class="heatmap-cell level-3"></span>
        <span class="heatmap-cell level-4"></span>
        <span>More</span>
      </div>
    </div>

    <!-- 算法核心专题掌握度 -->
    <div class="card category-card" v-if="categoryStats.length > 0">
      <div class="section-title" style="margin:0 0 16px">
        <h3>📊 经典算法专题掌握度</h3>
        <RouterLink to="/problems">查看全部专题 →</RouterLink>
      </div>

      <div class="category-grid">
        <div v-for="cat in categoryStats" :key="cat.name" class="cat-item">
          <div class="cat-top">
            <span class="cat-name">{{ cat.name }}</span>
            <span class="cat-ratio mono">{{ cat.solved }} / {{ cat.total }}</span>
          </div>
          <div class="cat-track">
            <div class="cat-bar" :style="{ width: `${cat.percent}%` }"></div>
          </div>
        </div>
      </div>
    </div>

    <!-- 秋招看板精选 -->
    <div class="section-title">
      <h2>🍁 秋招高频在招看板</h2>
      <RouterLink to="/jobs">查看全部公司与岗位 →</RouterLink>
    </div>
    <JobBoard :limit="4" />
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { api } from '../api'
import JobBoard from '../components/JobBoard.vue'
import type { Job, ProblemListItem, Submission } from '../types'

const router = useRouter()

const problemCount = ref(0)
const solvedCount = ref(0)
const rememberedCount = ref(0)
const openJobCount = ref(0)
const problems = ref<ProblemListItem[]>([])

interface HeatmapDay {
  date: string
  count: number
  level: number
}
const heatmapDays = ref<HeatmapDay[]>([])

// 随机一题
function pickRandomProblem() {
  if (problems.value.length === 0) return
  const unsolved = problems.value.filter((p) => p.my_status !== 'solved')
  const pool = unsolved.length > 0 ? unsolved : problems.value
  const target = pool[Math.floor(Math.random() * pool.length)]
  if (target) {
    router.push(`/problems/${target.slug}`)
  }
}

// 统计核心算法专题
const CORE_CATEGORIES = ['数组', '双指针', '二叉树', '动态规划', '哈希表', '滑动窗口', '回溯', '图论', '链表', '栈']

const categoryStats = computed(() => {
  if (problems.value.length === 0) return []
  return CORE_CATEGORIES.map((cat) => {
    const list = problems.value.filter((p) => (p.tags || []).includes(cat))
    const solved = list.filter((p) => p.my_status === 'solved').length
    const total = list.length || 1
    return {
      name: cat,
      solved,
      total: list.length,
      percent: Math.round((solved / total) * 100),
    }
  }).filter((c) => c.total > 0)
})

// 生成过去 52 周 (364 天) 热力图占位与真实数据映射
function generateHeatmap(submissions: Submission[]) {
  const days: HeatmapDay[] = []
  const countMap = new Map<string, number>()

  for (const s of submissions) {
    const d = s.created_at.split('T')[0]
    countMap.set(d, (countMap.get(d) || 0) + 1)
  }

  const today = new Date()
  for (let i = 363; i >= 0; i--) {
    const d = new Date(today)
    d.setDate(today.getDate() - i)
    const dateStr = d.toISOString().split('T')[0]
    const count = countMap.get(dateStr) || 0
    let level = 0
    if (count >= 5) level = 4
    else if (count >= 3) level = 3
    else if (count >= 2) level = 2
    else if (count >= 1) level = 1
    days.push({ date: dateStr, count, level })
  }
  heatmapDays.value = days
}

onMounted(async () => {
  try {
    const [pList, jobs, subs] = await Promise.all([
      api.get<ProblemListItem[]>('/api/problems'),
      api.get<Job[]>('/api/jobs'),
      api.get<Submission[]>('/api/submissions?limit=100').catch(() => [] as Submission[]),
    ])
    problems.value = pList
    problemCount.value = pList.length
    solvedCount.value = pList.filter((p) => p.my_status === 'solved').length
    rememberedCount.value = pList.filter((p) => p.memory === 'remembered').length
    openJobCount.value = jobs.filter((j) => j.status !== 'closed' && (j.days_left === null || j.days_left >= 0)).length

    generateHeatmap(subs)
  } catch {
    /* 统计异常优雅降级 */
  }
})
</script>
