<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card card">
      <div class="modal-head">
        <div>
          <h2>选择或制定你的刷题打卡计划</h2>
          <p class="modal-sub">自选开始 / 结束日期和每天题量，系统按日历把题目排进每一天</p>
        </div>
        <button class="close-btn" aria-label="关闭" @click="$emit('close')">
          <AppIcon name="x" :size="14" />
        </button>
      </div>

      <!-- 标签页：精选官方计划 vs 自定义计划 -->
      <div class="segmented modal-tabs">
        <button :class="{ active: tab === 'preset' }" @click="tab = 'preset'">
          <AppIcon name="sparkle" :size="13" />
          精选专题计划
        </button>
        <button :class="{ active: tab === 'custom' }" @click="tab = 'custom'">
          <AppIcon name="gear" :size="13" />
          自定义天数计划
        </button>
      </div>

      <!-- 选项卡 1: 精选计划列表 -->
      <div v-if="tab === 'preset'" class="preset-plans-grid">
        <div
          v-for="p in PRESET_PLANS"
          :key="p.id"
          class="preset-card card"
          :class="{ selected: selectedPresetId === p.id }"
          @click="selectedPresetId = p.id"
        >
          <div class="preset-top">
            <span class="badge badge-source">{{ p.badge }}</span>
            <span class="preset-duration mono">{{ p.totalDays }} 天周期 · 每日 {{ p.dailyGoal }} 题</span>
          </div>
          <div class="preset-title">{{ p.title }}</div>
          <div class="preset-desc">{{ p.tagline }}</div>
          <div class="preset-tags">
            <span v-for="tag in p.categoryTags" :key="tag" class="badge badge-tag">{{ tag }}</span>
          </div>
        </div>
      </div>

      <!-- 选项卡 2: 自定义计划表单 -->
      <div v-else class="custom-plan-form">
        <div class="form-group">
          <label>计划名称</label>
          <input
            v-model="customTitle"
            class="input"
            placeholder="例如：2周秋招大厂手撕冲刺计划 / 每日自律打卡"
          />
        </div>

        <div class="form-row">
          <div class="form-group flex-1">
            <label>开始日期</label>
            <input v-model="customStart" class="input" type="date" />
          </div>
          <div class="form-group flex-1">
            <label>结束日期</label>
            <input
              class="input"
              type="date"
              :min="customStart"
              :value="customEnd"
              @change="onEndChange"
            />
          </div>
        </div>

        <div class="form-row">
          <div class="form-group flex-1">
            <label>计划周期（天数）</label>
            <div class="pill-group">
              <button
                v-for="d in [7, 14, 21, 30]"
                :key="d"
                type="button"
                class="pill-btn"
                :class="{ active: daysSafe === d }"
                @click="customDays = d"
              >
                {{ d }} 天
              </button>
              <label class="pill-input-wrap">
                <input
                  class="input pill-number"
                  type="number"
                  min="1"
                  max="180"
                  v-model.number="customDays"
                  @blur="customDays = daysSafe"
                />
                <span>天</span>
              </label>
            </div>
          </div>

          <div class="form-group flex-1">
            <label>每日打卡目标（题数）</label>
            <div class="pill-group">
              <button
                v-for="g in [1, 2, 3, 5]"
                :key="g"
                type="button"
                class="pill-btn"
                :class="{ active: goalSafe === g }"
                @click="customGoal = g"
              >
                {{ g }} 题 / 天
              </button>
              <label class="pill-input-wrap">
                <input
                  class="input pill-number"
                  type="number"
                  min="1"
                  max="20"
                  v-model.number="customGoal"
                  @blur="customGoal = goalSafe"
                />
                <span>题 / 天</span>
              </label>
            </div>
          </div>
        </div>

        <div v-if="formError" class="form-err">{{ formError }}</div>
        <div class="custom-preview-tip">
          {{ formatZhDate(customStart) }} — {{ formatZhDate(customEnd) }}，共
          <strong>{{ daysSafe }}</strong> 天。
          每日 {{ goalSafe }} 题，共需 <strong>{{ requestedCount }}</strong> 题。
          <span v-if="problems.length === 0">题库为空，无法开启。</span>
          <span v-else-if="requestedCount <= problems.length">
            将从题库 {{ problems.length }} 道里优先抽未刷题目，每天恰好 {{ goalSafe }} 题。
          </span>
          <span v-else>
            题库现有 {{ problems.length }} 道，将均匀排进 {{ daysSafe }} 天（部分天不足 {{ goalSafe }} 题，不重复占用同一题）。
          </span>
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-ghost" @click="$emit('close')">取消</button>
        <button class="btn btn-primary" :disabled="!canStart" @click="handleStartPlan">
          立即开启打卡计划
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, ref } from 'vue'
import AppIcon from './AppIcon.vue'
import { formatZhDate, todayLocalDate } from '../dates'
import {
  PRESET_PLANS,
  clampPlanDays,
  clampPlanGoal,
  daysFromRange,
  endDateFromStart,
  useStudyPlan,
} from '../stores/plan'
import { useToast } from '../stores/toast'
import type { ProblemListItem } from '../types'

const props = defineProps<{
  problems: ProblemListItem[]
}>()

const emit = defineEmits<{
  (e: 'close'): void
  (e: 'started'): void
}>()

const toast = useToast()
const { activatePreset, createCustomPlan } = useStudyPlan()

const tab = ref<'preset' | 'custom'>('custom')
const selectedPresetId = ref(PRESET_PLANS[0].id)
const customTitle = ref('2周自律刷题打卡冲刺')
const customStart = ref(todayLocalDate())
const customDays = ref(14)
const customGoal = ref(2)
const formError = ref('')

const daysSafe = computed(() => clampPlanDays(Number(customDays.value)))
const goalSafe = computed(() => clampPlanGoal(Number(customGoal.value)))
const customEnd = computed(() => endDateFromStart(customStart.value, daysSafe.value))
const requestedCount = computed(() => daysSafe.value * goalSafe.value)
const canStart = computed(() => {
  if (tab.value === 'preset') return props.problems.length > 0
  return props.problems.length > 0 && Boolean(customStart.value)
})

function onEndChange(e: Event) {
  const end = (e.target as HTMLInputElement).value
  if (!end || !customStart.value) return
  if (end < customStart.value) {
    customDays.value = 1
    return
  }
  customDays.value = daysFromRange(customStart.value, end)
}

function handleStartPlan() {
  formError.value = ''
  if (props.problems.length === 0) {
    formError.value = '题库为空，无法制定计划'
    toast.error('题库为空，无法制定计划')
    return
  }
  if (tab.value === 'preset') {
    const preset = PRESET_PLANS.find((p) => p.id === selectedPresetId.value) || PRESET_PLANS[0]
    activatePreset(preset, props.problems)
    toast.success(`已成功开启【${preset.title}】！加油！`)
  } else {
    if (!customStart.value) {
      formError.value = '请选择开始日期'
      return
    }
    const result = createCustomPlan(
      customTitle.value,
      daysSafe.value,
      goalSafe.value,
      props.problems,
      customStart.value,
    )
    if (!result.ok) {
      formError.value = result.message
      toast.error(result.message)
      return
    }
    toast.success(
      `已开启【${customTitle.value || '自定义打卡计划'}】：${formatZhDate(customStart.value)} 至 ${formatZhDate(customEnd.value)}，共 ${daysSafe.value} 天`,
    )
  }
  emit('started')
  emit('close')
}
</script>
