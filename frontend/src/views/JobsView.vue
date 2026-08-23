<template>
  <div class="container">
    <div class="page-head">
      <div>
        <div class="kicker">Job Board</div>
        <h1 class="display">校招看板</h1>
      </div>
      <span class="sub">岗位 · 开投/截止 · JD · 投递入口</span>
    </div>
    <JobBoard />
  </div>
</template>

<script setup lang="ts">
import JobBoard from '../components/JobBoard.vue'
</script>
