<template>
  <div class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-card card">
      <div class="modal-head">
        <div>
          <h2>选择或制定你的刷题打卡计划</h2>
          <p class="modal-sub">设定清晰的目标周期，每日定量打卡，告别碎片化刷题</p>
        </div>
        <button class="btn btn-ghost btn-xs close-btn" @click="$emit('close')">✕</button>
      </div>

      <!-- 标签页：精选官方计划 vs 自定义计划 -->
      <div class="modal-tabs">
        <button :class="{ active: tab === 'preset' }" @click="tab = 'preset'">
          🌟 精选专题计划
        </button>
        <button :class="{ active: tab === 'custom' }" @click="tab = 'custom'">
          🛠️ 自定义天数计划
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
            <label>计划周期 (天数)</label>
            <div class="pill-group">
              <button
                v-for="d in [7, 14, 21, 30]"
                :key="d"
                type="button"
                class="pill-btn"
                :class="{ active: customDays === d }"
                @click="customDays = d"
              >
                {{ d }} 天
              </button>
            </div>
          </div>

          <div class="form-group flex-1">
            <label>每日打卡目标 (题数)</label>
            <div class="pill-group">
              <button
                v-for="g in [1, 2, 3, 5]"
                :key="g"
                type="button"
                class="pill-btn"
                :class="{ active: customGoal === g }"
                @click="customGoal = g"
              >
                {{ g }} 题 / 天
              </button>
            </div>
          </div>
        </div>

        <div class="custom-preview-tip">
          💡 系统将自动从力扣热题 100 与高频面经中为你编排每日任务，共计约 <strong>{{ customDays * customGoal }}</strong> 道核心好题。
        </div>
      </div>

      <div class="modal-actions">
        <button class="btn btn-ghost" @click="$emit('close')">取消</button>
        <button class="btn btn-primary" @click="handleStartPlan">
          🚀 立即开启打卡计划
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { PRESET_PLANS, useStudyPlan } from '../stores/plan'
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

const tab = ref<'preset' | 'custom'>('preset')
const selectedPresetId = ref(PRESET_PLANS[0].id)
const customTitle = ref('2周自律刷题打卡冲刺')
const customDays = ref(14)
const customGoal = ref(2)

function handleStartPlan() {
  if (tab.value === 'preset') {
    const preset = PRESET_PLANS.find((p) => p.id === selectedPresetId.value) || PRESET_PLANS[0]
    activatePreset(preset, props.problems)
    toast.success(`已成功开启【${preset.title}】！加油！`)
  } else {
    createCustomPlan(customTitle.value, customDays.value, customGoal.value, props.problems)
    toast.success(`已成功开启【${customTitle.value || '自定义打卡计划'}】！`)
  }
  emit('started')
  emit('close')
}
</script>
