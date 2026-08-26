<template>
  <span class="user-avatar" :class="`user-avatar-${size}`" :title="username">
    <img
      v-if="avatarUrl && !broken"
      :src="avatarUrl"
      :alt="username"
      @error="broken = true"
    />
    <span v-else class="user-avatar-fallback">{{ letter }}</span>
  </span>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'

const props = withDefaults(
  defineProps<{
    username: string
    avatarUrl?: string | null
    size?: 'sm' | 'md'
  }>(),
  { size: 'sm', avatarUrl: null },
)

const broken = ref(false)
watch(
  () => props.avatarUrl,
  () => {
    broken.value = false
  },
)

const letter = computed(() => (props.username.slice(0, 1) || '?').toUpperCase())
</script>
