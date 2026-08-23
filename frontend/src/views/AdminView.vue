<template>
  <div class="container">
    <div class="page-head">
      <div>
        <div class="kicker">Admin</div>
        <h1 class="display">管理后台</h1>
      </div>
    </div>

    <div class="admin-tabs">
      <button :class="{ active: tab === 'problems' }" @click="tab = 'problems'">题目管理</button>
      <button :class="{ active: tab === 'jobs' }" @click="tab = 'jobs'">看板管理</button>
    </div>

    <!-- 题目管理 -->
    <div v-show="tab === 'problems'" class="card">
      <div style="padding:12px 14px;border-bottom:1px solid var(--border);display:flex;gap:10px;align-items:center">
        <button class="btn btn-sm btn-primary" :disabled="seeding" @click="reloadSeed">
          {{ seeding ? '导入中…' : '重新导入种子题库' }}
        </button>
        <span v-if="seedMsg" style="font-size:13px;color:var(--text-dim)">{{ seedMsg }}</span>
      </div>
      <div v-if="problems.length === 0" class="empty">暂无题目，点上方按钮导入种子</div>
      <div v-for="p in problems" :key="p.id" class="admin-row">
        <span class="badge" :class="`badge-${p.difficulty}`" style="flex:none">{{ p.difficulty }}</span>
        <span class="grow">{{ p.title }} <span style="color:var(--text-faint);font-size:12px">{{ p.slug }}</span></span>
        <label style="display:flex;align-items:center;gap:6px;font-size:13px;color:var(--text-dim);flex:none">
          <input type="checkbox" :checked="p.is_published" @change="togglePublish(p)" /> 上架
        </label>
      </div>
    </div>

    <!-- 看板管理 -->
    <div v-show="tab === 'jobs'">
      <div class="card" style="padding:18px 20px;margin-bottom:14px">
        <h3 style="margin-top:0">{{ editingJob ? '编辑岗位' : '新增岗位' }}</h3>
        <div v-if="jobError" class="form-error">{{ jobError }}</div>
        <form @submit.prevent="saveJob">
          <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:0 14px">
            <div class="field"><label>公司 *</label><input v-model="jobForm.company" class="input" required /></div>
            <div class="field"><label>岗位 *</label><input v-model="jobForm.position" class="input" required /></div>
            <div class="field"><label>批次</label><input v-model="jobForm.batch" class="input" placeholder="如 2026秋招" /></div>
            <div class="field"><label>开投日期</label><input v-model="jobForm.open_at" class="input" type="date" /></div>
            <div class="field"><label>截止日期</label><input v-model="jobForm.deadline_at" class="input" type="date" /></div>
            <div class="field"><label>投递链接</label><input v-model="jobForm.apply_url" class="input" type="url" placeholder="https://" /></div>
            <div class="field">
              <label>规模</label>
              <select v-model="jobForm.tier" class="select">
                <option value="big">大厂</option>
                <option value="mid">中厂</option>
                <option value="small">小厂</option>
              </select>
            </div>
            <div class="field">
              <label>状态</label>
              <select v-model="jobForm.status" class="select">
                <option value="open">进行中</option>
                <option value="closed">已关闭</option>
              </select>
            </div>
          </div>
          <div class="field"><label>JD 摘要</label><textarea v-model="jobForm.jd_text" class="textarea" rows="3"></textarea></div>
          <div style="display:flex;gap:8px">
            <button class="btn btn-primary btn-sm" type="submit">{{ editingJob ? '保存修改' : '添加岗位' }}</button>
            <button v-if="editingJob" class="btn btn-sm" type="button" @click="resetForm">取消编辑</button>
          </div>
        </form>
      </div>

      <div class="card">
        <div v-if="jobs.length === 0" class="empty">暂无岗位</div>
        <div v-for="j in jobs" :key="j.id" class="admin-row">
          <span class="grow"><b>{{ j.company }}</b> · {{ j.position }}
            <span style="color:var(--text-faint);font-size:12px">{{ j.deadline_at ? ` 截止 ${j.deadline_at}` : '' }}</span>
          </span>
          <button class="btn btn-sm" @click="editJob(j)">编辑</button>
          <button class="btn btn-sm" style="color:var(--red)" @click="deleteJob(j)">删除</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { api } from '../api'
import type { Job, ProblemListItem } from '../types'

interface AdminProblem extends ProblemListItem {
  is_published: boolean
}

const tab = ref<'problems' | 'jobs'>('problems')

// 题目管理
const problems = ref<AdminProblem[]>([])
const seeding = ref(false)
const seedMsg = ref('')

async function loadProblems() {
  problems.value = await api.get<AdminProblem[]>('/api/admin/problems')
}

async function togglePublish(p: AdminProblem) {
  await api.put(`/api/admin/problems/${p.id}`, { is_published: !p.is_published })
  p.is_published = !p.is_published
}

async function reloadSeed() {
  seeding.value = true
  seedMsg.value = ''
  try {
    const res = await api.post<{ imported: number }>('/api/admin/seed/reload')
    seedMsg.value = `已导入 ${res.imported} 道题`
    await loadProblems()
  } catch (e) {
    seedMsg.value = e instanceof Error ? e.message : '导入失败'
  } finally {
    seeding.value = false
  }
}

// 看板管理
const jobs = ref<Job[]>([])
const editingJob = ref<Job | null>(null)
const jobError = ref('')
const jobForm = reactive({
  company: '',
  position: '',
  tier: 'small',
  batch: '',
  open_at: '',
  deadline_at: '',
  apply_url: '',
  jd_text: '',
  status: 'open',
})

async function loadJobs() {
  jobs.value = await api.get<Job[]>('/api/jobs')
}

function resetForm() {
  editingJob.value = null
  jobError.value = ''
  Object.assign(jobForm, {
    company: '', position: '', tier: 'small', batch: '', open_at: '', deadline_at: '',
    apply_url: '', jd_text: '', status: 'open',
  })
}

function editJob(j: Job) {
  editingJob.value = j
  Object.assign(jobForm, {
    company: j.company,
    position: j.position,
    tier: j.tier ?? 'small',
    batch: j.batch ?? '',
    open_at: j.open_at ?? '',
    deadline_at: j.deadline_at ?? '',
    apply_url: j.apply_url ?? '',
    jd_text: j.jd_text ?? '',
    status: j.status,
  })
}

async function saveJob() {
  jobError.value = ''
  const body = {
    company: jobForm.company,
    position: jobForm.position,
    tier: jobForm.tier,
    batch: jobForm.batch || null,
    open_at: jobForm.open_at || null,
    deadline_at: jobForm.deadline_at || null,
    apply_url: jobForm.apply_url || null,
    jd_text: jobForm.jd_text || null,
    status: jobForm.status,
  }
  try {
    if (editingJob.value) {
      await api.put(`/api/jobs/${editingJob.value.id}`, body)
    } else {
      await api.post('/api/jobs', body)
    }
    resetForm()
    await loadJobs()
  } catch (e) {
    jobError.value = e instanceof Error ? e.message : '保存失败'
  }
}

async function deleteJob(j: Job) {
  if (!confirm(`确认删除「${j.company} · ${j.position}」？`)) return
  await api.del(`/api/jobs/${j.id}`)
  await loadJobs()
}

onMounted(() => {
  loadProblems()
  loadJobs()
})
</script>
