<template>
  <div>
    <!-- 场景 A: 存在激活的打卡计划 -->
    <div v-if="activePlan" class="card active-plan-card">
      <!-- 计划头部 -->
      <div class="plan-header">
        <div class="plan-info">
          <div class="plan-badge-line">
            <span class="badge badge-source">{{ activePlan.badge }}</span>
            <span class="plan-day-tag mono">
              第 {{ currentDayIndex }} / {{ activePlan.totalDays }} 天
            </span>
          </div>
          <h2 class="plan-title">{{ activePlan.title }}</h2>
          <p class="plan-tagline">{{ activePlan.tagline }}</p>
        </div>

        <div class="plan-actions-top">
          <button class="btn btn-ghost btn-xs" @click="$emit('open-modal')">
            切换计划
          </button>
          <button class="btn btn-ghost btn-xs text-red" @click="handleReset">
            重置
          </button>
        </div>
      </div>

      <!-- 计划整体进度条 -->
      <div class="plan-progress-section">
        <div class="plan-progress-stats">
          <span>总进度：<strong>{{ completedDaysCount }}</strong> / {{ activePlan.totalDays }} 天达标</span>
          <span class="mono">{{ planProgressPercent }}%</span>
        </div>
        <div class="plan-progress-track">
          <div class="plan-progress-bar" :style="{ width: `${planProgressPercent}%` }"></div>
        </div>
      </div>

      <!-- 天数打卡足迹矩阵 (1..totalDays) -->
      <div class="plan-matrix-wrap">
        <div class="plan-matrix">
          <div
            v-for="d in activePlan.totalDays"
            :key="d"
            class="matrix-day-box"
            :class="{
              'is-completed': isDayCompleted(d),
              'is-today': d === currentDayIndex,
              'is-past': d < currentDayIndex && !isDayCompleted(d),
              'is-future': d > currentDayIndex,
            }"
            :title="planDayTitle(d)"
          >
            <span class="day-num">D{{ d }}</span>
            <span class="day-status-icon">
              {{ isDayCompleted(d) ? '✓' : d === currentDayIndex ? '●' : '○' }}
            </span>
          </div>
        </div>
      </div>

      <!-- 今日打卡任务看板 -->
      <div class="today-mission-box">
        <div class="today-mission-head">
          <div class="today-target-line">
            <span class="today-tag">🎯 今日目标 · {{ formatZhMd(todayStr) }}</span>
            <span class="today-count mono">
              已完成 <strong>{{ todayProgress.count }}</strong> / {{ activePlan.dailyGoal }} 题
            </span>
            <span
              v-if="todayProgress.completed"
              class="today-badge-ok"
            >
              ✨ 今日打卡已达标！
            </span>
            <span v-else class="today-badge-pending">
              ⏳ 还差 {{ Math.max(0, activePlan.dailyGoal - todayProgress.count) }} 题达标
            </span>
          </div>
        </div>

        <!-- 今日精选题目列表 -->
        <div class="today-problems-list" v-if="todayProblems.length > 0">
          <div
            v-for="p in todayProblems"
            :key="p.slug"
            class="today-problem-card"
          >
            <div class="tp-info">
              <span class="badge" :class="`badge-${p.difficulty}`">
                {{ p.difficulty === 'easy' ? '简单' : p.difficulty === 'medium' ? '中等' : '困难' }}
              </span>
              <span class="tp-title">{{ problemHeading(p) }}</span>
              <span class="tp-slug mono">{{ p.slug }}</span>
            </div>

            <div class="tp-actions">
              <span v-if="p.my_status === 'solved'" class="badge" style="color:var(--green)">
                ✓ 已解决
              </span>
              <RouterLink :to="`/problems/${p.slug}`" class="btn btn-sm btn-primary">
                {{ p.my_status === 'solved' ? '再刷一遍 →' : '去完成此题 →' }}
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 场景 B: 暂无激活计划，展示开启打卡引导横幅 -->
    <div v-else class="card plan-cta-card" @click="$emit('open-modal')">
      <div class="cta-left">
        <div class="cta-badge">🔥 自律冲刺</div>
        <h3 class="cta-title">制定你的 2 周 / 7 天刷题打卡冲刺计划</h3>
        <p class="cta-desc">
          设定专属学习周期，每日定量突破核心高频题，用持续打卡点亮你的算法成就墙！
        </p>
      </div>
      <button class="btn btn-primary cta-btn">
        🚀 选择 / 开启打卡计划
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { addDays, formatZhDate, formatZhMd, todayLocalDate } from '../dates'
import { useStudyPlan } from '../stores/plan'
import { useToast } from '../stores/toast'
import { problemHeading, type ProblemListItem } from '../types'

const props = defineProps<{
  problems: ProblemListItem[]
}>()

defineEmits<{
  (e: 'open-modal'): void
}>()

const toast = useToast()
const {
  activePlan,
  currentDayIndex,
  todayTargetSlugs,
  todayProgress,
  completedDaysCount,
  planProgressPercent,
  resetPlan,
} = useStudyPlan()

// 获取今日分配的真实题目对象
const todayStr = todayLocalDate()

const todayProblems = computed(() => {
  if (!todayTargetSlugs.value.length) return []
  return props.problems.filter((p) => todayTargetSlugs.value.includes(p.slug))
})

function planDayTitle(day: number): string {
  if (!activePlan.value) return `第 ${day} 天`
  const iso = addDays(activePlan.value.startDate, day - 1)
  return `${formatZhDate(iso)} · 第 ${day} 天`
}

// 判断某一特定天数是否达标
function isDayCompleted(day: number): boolean {
  if (!activePlan.value) return false
  const start = new Date(activePlan.value.startDate)
  const targetDate = new Date(start)
  targetDate.setDate(start.getDate() + (day - 1))
  const dateStr = `${targetDate.getFullYear()}-${String(targetDate.getMonth() + 1).padStart(2, '0')}-${String(targetDate.getDate()).padStart(2, '0')}`

  const rec = activePlan.value.punchRecords[dateStr]
  return !!rec?.completed
}

function handleReset() {
  if (window.confirm('确定要放弃当前打卡计划吗？')) {
    resetPlan()
    toast.info('已重置打卡计划')
  }
}
</script>
