<template>
  <div class="plan-wrap">
    <!-- 场景 A: 存在激活的打卡计划 -->
    <div v-if="activePlan" class="card active-plan-card">
      <!-- 计划头部 -->
      <div class="plan-header">
        <div class="plan-info">
          <div class="plan-badge-line">
            <span class="badge badge-source">{{ activePlan.badge }}</span>
            <span class="plan-day-tag mono">{{ phaseLabel }}</span>
          </div>
          <h2 class="plan-title">{{ activePlan.title }}</h2>
          <p class="plan-tagline">{{ activePlan.tagline }}</p>
          <p class="plan-date-range mono">
            {{ formatZhDate(activePlan.startDate) }} — {{ formatZhDate(planEndDate) }}
            · 每日 {{ activePlan.dailyGoal }} 题
          </p>
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
            :class="dayBoxClass(d)"
            :title="planDayTitle(d)"
          >
            <span class="day-date">{{ formatMdSlash(addDays(activePlan.startDate, d - 1)) }}</span>
            <span class="day-num">D{{ d }}</span>
          </div>
        </div>
      </div>

      <!-- 今日打卡任务看板 -->
      <div class="today-mission-box">
        <div class="today-mission-head">
          <div class="today-target-line">
            <span class="today-tag">{{ todayHeadline }}</span>
            <template v-if="planPhase === 'active'">
              <span class="today-count mono">
                已完成 <strong>{{ todayProgress.count }}</strong> / {{ todayQuota }} 题
              </span>
              <span v-if="todayProgress.completed" class="today-badge-ok">
                <AppIcon name="sparkle" :size="12" />
                今日打卡已达标！
              </span>
              <span v-else class="today-badge-pending">
                <AppIcon name="clock" :size="12" />
                还差 {{ Math.max(0, todayQuota - todayProgress.count) }} 题达标
              </span>
            </template>
          </div>
        </div>

        <div v-if="planPhase === 'upcoming'" class="empty">
          计划将于 {{ formatZhDate(activePlan.startDate) }} 开始，今天暂无打卡任务。
        </div>
        <div v-else-if="planPhase === 'ended'" class="empty">
          计划已于 {{ formatZhDate(planEndDate) }} 结束。可点右上角切换或重置后再开新计划。
        </div>
        <div v-else-if="todayProblems.length === 0" class="empty">
          今日没有编排题目（当天题量为 0）。
        </div>
        <div class="today-problems-list" v-else>
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
              <span v-if="p.my_status === 'solved'" class="tp-solved">
                <AppIcon name="check" :size="13" />
                已解决
              </span>
              <RouterLink :to="`/problems/${p.slug}`" class="btn btn-sm btn-primary">
                {{ p.my_status === 'solved' ? '再刷一遍' : '去完成此题' }}
                <AppIcon name="arrow-right" :size="13" />
              </RouterLink>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- 场景 B: 暂无激活计划，展示开启打卡引导横幅 -->
    <div v-else class="card plan-cta-card" @click="$emit('open-modal')">
      <div class="cta-left">
        <div class="cta-badge">
          <AppIcon name="flame" :size="12" />
          自律冲刺
        </div>
        <h3 class="cta-title">制定你的 2 周 / 7 天刷题打卡冲刺计划</h3>
        <p class="cta-desc">
          设定专属学习周期，每日定量突破核心高频题，用持续打卡点亮你的算法成就墙！
        </p>
      </div>
      <button class="btn btn-primary cta-btn">
        选择 / 开启打卡计划
        <AppIcon name="arrow-right" :size="15" />
      </button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import AppIcon from './AppIcon.vue'
import { addDays, formatMdSlash, formatZhDate, formatZhMd, todayLocalDate } from '../dates'
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
  planPhase,
  planEndDate,
  todayTargetSlugs,
  todayProgress,
  completedDaysCount,
  planProgressPercent,
  resetPlan,
} = useStudyPlan()

const todayStr = todayLocalDate()

const todayProblems = computed(() => {
  if (!todayTargetSlugs.value.length) return []
  const order = new Map(todayTargetSlugs.value.map((slug, i) => [slug, i]))
  return props.problems
    .filter((p) => order.has(p.slug))
    .sort((a, b) => (order.get(a.slug) ?? 0) - (order.get(b.slug) ?? 0))
})

const todayQuota = computed(() => {
  if (todayTargetSlugs.value.length > 0) return todayTargetSlugs.value.length
  return activePlan.value?.dailyGoal ?? 0
})

const phaseLabel = computed(() => {
  if (!activePlan.value) return ''
  if (planPhase.value === 'upcoming') return `未开始 · ${activePlan.value.totalDays} 天`
  if (planPhase.value === 'ended') return `已结束 · ${activePlan.value.totalDays} 天`
  return `第 ${currentDayIndex.value} / ${activePlan.value.totalDays} 天`
})

const todayHeadline = computed(() => {
  if (planPhase.value === 'upcoming') return `尚未开营 · ${formatZhMd(todayStr)}`
  if (planPhase.value === 'ended') return `计划已结束 · ${formatZhMd(todayStr)}`
  return `今日目标 · ${formatZhMd(todayStr)}`
})

function planDayTitle(day: number): string {
  if (!activePlan.value) return `第 ${day} 天`
  const iso = addDays(activePlan.value.startDate, day - 1)
  const n = activePlan.value.schedule[day]?.length ?? 0
  return `${formatZhDate(iso)} · 第 ${day} 天 · ${n} 题`
}

function isDayCompleted(day: number): boolean {
  if (!activePlan.value) return false
  const iso = addDays(activePlan.value.startDate, day - 1)
  return !!activePlan.value.punchRecords[iso]?.completed
}

function dayBoxClass(day: number) {
  const today = currentDayIndex.value
  const completed = isDayCompleted(day)
  if (planPhase.value === 'upcoming') {
    return { 'is-future': true }
  }
  if (planPhase.value === 'ended') {
    return { 'is-completed': completed, 'is-past': !completed }
  }
  return {
    'is-completed': completed,
    'is-today': today === day,
    'is-past': today != null && day < today && !completed,
    'is-future': today != null && day > today,
  }
}

function handleReset() {
  if (window.confirm('确定要放弃当前打卡计划吗？')) {
    resetPlan()
    toast.info('已重置打卡计划')
  }
}
</script>
