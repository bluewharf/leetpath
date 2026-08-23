<template>
  <div class="skeleton-wrap">
    <div
      v-for="i in count"
      :key="i"
      class="skeleton"
      :style="{
        height: height || '22px',
        width: width || '100%',
        borderRadius: radius || '8px',
        marginBottom: gap || '10px',
      }"
    ></div>
  </div>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    count?: number
    height?: string
    width?: string
    radius?: string
    gap?: string
  }>(),
  {
    count: 1,
    height: '22px',
    width: '100%',
    radius: '8px',
    gap: '10px',
  },
)
</script>
