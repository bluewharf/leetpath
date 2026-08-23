<template>
  <div class="container">
    <div class="hero">
      <div class="kicker">LeetPath · 个人刷题站</div>
      <h1>空余间隙，<span class="grad">刷一道题</span>。</h1>
      <p class="lede">热题 100 + 面经高频手撕，Python3 / C++ 在线评测立刻出对错，草稿入库多端同步——手机和电脑，随时随地保持手感。</p>
      <div class="hero-stats">
        <div class="hstat">
          <span class="num grad-num">{{ solvedCount }}<span style="font-size:16px;color:var(--text-faint)"> / {{ problemCount }}</span></span>
          <span class="lbl">已通过题目</span>
        </div>
        <div class="hstat">
          <span class="num">2</span>
          <span class="lbl">评测语言</span>
        </div>
        <div class="hstat">
          <span class="num">{{ jobCount }}</span>
          <span class="lbl">在招岗位</span>
        </div>
      </div>
      <div class="hero-actions">
        <RouterLink class="btn btn-primary" to="/problems">进入题库 →</RouterLink>
        <RouterLink class="btn" to="/jobs">校招看板</RouterLink>
        <RouterLink class="btn" to="/links">大模型八股 ↗</RouterLink>
      </div>
    </div>

    <div class="section-title">
      <h2>校招看板</h2>
      <RouterLink to="/jobs">查看全部 →</RouterLink>
    </div>
    <JobBoard :limit="6" />
  </div>
</template>

<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { api } from '../api'
import type { Job, ProblemListItem } from '../types'
import JobBoard from '../components/JobBoard.vue'

const problemCount = ref(0)
const solvedCount = ref(0)
const jobCount = ref(0)

onMounted(async () => {
  try {
    const [problems, jobs] = await Promise.all([
      api.get<ProblemListItem[]>('/api/problems'),
      api.get<Job[]>('/api/jobs'),
    ])
    problemCount.value = problems.length
    solvedCount.value = problems.filter((p) => p.my_status === 'solved').length
    jobCount.value = jobs.filter((j) => j.status !== 'closed' && (j.days_left === null || j.days_left >= 0)).length
  } catch {
    /* 统计失败不影响页面 */
  }
})
</script>
