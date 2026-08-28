<template>
  <div class="container links-page">
    <div v-if="error" class="error-banner">
      <span>{{ error }}</span>
      <button type="button" class="btn btn-sm" @click="loadLinks">重试</button>
    </div>
    <div class="page-head">
      <div>
        <div class="kicker">Interview Notes</div>
        <h1 class="display">八股笔记</h1>
      </div>
      <span class="sub">小林笔记 + 2026 Agent Harness / MCP / Skills 一手文档</span>
    </div>
    <div v-if="loading" class="empty">加载中…</div>
    <template v-else>
      <div v-for="(items, category) in grouped" :key="category" class="link-group">
        <h2>{{ category }}</h2>
        <div class="link-grid">
          <a v-for="item in items" :key="item.url + item.title" class="card link-card" :href="item.url" target="_blank" rel="noopener">
            <div class="link-title">{{ item.title }} <AppIcon name="arrow-right" :size="14" class="ext" /></div>
            <div v-if="item.note" class="link-note">{{ item.note }}</div>
          </a>
        </div>
      </div>
      <div v-if="!error && Object.keys(grouped).length === 0" class="empty">暂无链接</div>
    </template>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { api } from '../api'
import type { LinkItem } from '../types'
import AppIcon from '../components/AppIcon.vue'

const links = ref<LinkItem[]>([])
const loading = ref(true)
const error = ref('')

const grouped = computed(() => {
  const g: Record<string, LinkItem[]> = {}
  for (const item of links.value) {
    ;(g[item.category] ??= []).push(item)
  }
  return g
})

async function loadLinks() {
  loading.value = true
  try {
    links.value = await api.get<LinkItem[]>('/api/links')
    error.value = ''
  } catch {
    error.value = '加载失败，请检查网络后重试'
  } finally {
    loading.value = false
  }
}

onMounted(() => loadLinks())
</script>
