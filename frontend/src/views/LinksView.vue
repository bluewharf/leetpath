<template>
  <div class="container">
    <div class="page-head">
      <div>
        <div class="kicker">Interview Notes</div>
        <h1 class="display">八股笔记</h1>
      </div>
      <span class="sub">内容不自建，跳转小林面试笔记</span>
    </div>
    <div v-if="loading" class="empty">加载中…</div>
    <template v-else>
      <div v-for="(items, category) in grouped" :key="category" class="link-group">
        <h2>{{ category }}</h2>
        <div class="link-grid">
          <a v-for="item in items" :key="item.url + item.title" class="card link-card" :href="item.url" target="_blank" rel="noopener">
            <div class="link-title">{{ item.title }} <span class="ext">↗</span></div>
            <div v-if="item.note" class="link-note">{{ item.note }}</div>
          </a>
        </div>
      </div>
      <div v-if="Object.keys(grouped).length === 0" class="empty">暂无链接</div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { api } from '../api'
import type { LinkItem } from '../types'

const links = ref<LinkItem[]>([])
const loading = ref(true)

const grouped = computed(() => {
  const g: Record<string, LinkItem[]> = {}
  for (const item of links.value) {
    ;(g[item.category] ??= []).push(item)
  }
  return g
})

onMounted(async () => {
  try {
    links.value = await api.get<LinkItem[]>('/api/links')
  } finally {
    loading.value = false
  }
})
</script>
