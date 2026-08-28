<template>
  <div class="toast-container" v-if="toasts.length > 0">
    <transition-group name="toast-slide">
      <div
        v-for="t in toasts"
        :key="t.id"
        class="toast-item"
        :class="`toast-${t.type}`"
        @click="dismiss(t.id)"
      >
        <span class="toast-icon"><AppIcon :name="iconMap[t.type]" :size="15" /></span>
        <span class="toast-msg">{{ t.message }}</span>
      </div>
    </transition-group>
  </div>
</template>

<script setup lang="ts">
import AppIcon from './AppIcon.vue'
import { useToast } from '../stores/toast'

const { toasts, dismiss } = useToast()

const iconMap = {
  success: 'check',
  error: 'x',
  info: 'sparkle',
} as const
</script>
