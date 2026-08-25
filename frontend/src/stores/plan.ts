import { computed, ref } from 'vue'
import { addDays, diffDays, todayLocalDate } from '../dates'
import type { ProblemListItem } from '../types'

export interface StudyPlan {
  id: string
  title: string
  tagline: string
  badge: string
  totalDays: number
  dailyGoal: number
  startDate: string // YYYY-MM-DD，含当天
  endDate: string // YYYY-MM-DD，含当天
  // 每天分配的题目 slug 列表 (1-indexed, day 1..totalDays)
  schedule: Record<number, string[]>
  // 打卡记录：key 为 "YYYY-MM-DD"
  punchRecords: Record<string, { solvedSlugs: string[]; completed: boolean }>
}

export type PlanPhase = 'idle' | 'upcoming' | 'active' | 'ended'

export const PLAN_DAYS_MIN = 1
export const PLAN_DAYS_MAX = 180
export const PLAN_GOAL_MIN = 1
export const PLAN_GOAL_MAX = 20

export function clampPlanDays(n: number): number {
  if (!Number.isFinite(n)) return 14
  return Math.min(PLAN_DAYS_MAX, Math.max(PLAN_DAYS_MIN, Math.round(n)))
}

export function clampPlanGoal(n: number): number {
  if (!Number.isFinite(n)) return 2
  return Math.min(PLAN_GOAL_MAX, Math.max(PLAN_GOAL_MIN, Math.round(n)))
}

export function endDateFromStart(startDate: string, totalDays: number): string {
  return addDays(startDate, clampPlanDays(totalDays) - 1)
}

export function daysFromRange(startDate: string, endDate: string): number {
  return clampPlanDays(diffDays(startDate, endDate) + 1)
}

/** 计划第几天（1-indexed）。日期落在区间外则 null。 */
export function dayIndexOn(startDate: string, totalDays: number, iso: string): number | null {
  const d = diffDays(startDate, iso) + 1
  if (d < 1 || d > totalDays) return null
  return d
}

function statusRank(p: ProblemListItem): number {
  if (p.my_status === 'solved') return 2
  if (p.my_status === 'attempted') return 1
  return 0
}

export function pickPlanSlugs(allProblems: ProblemListItem[], needed: number, preferred: string[] = []): string[] {
  const existing = new Set(allProblems.map((p) => p.slug))
  const chosen: string[] = []
  for (const slug of preferred) {
    if (existing.has(slug) && !chosen.includes(slug)) chosen.push(slug)
    if (chosen.length >= needed) return chosen
  }
  const rest = [...allProblems]
    .filter((p) => !chosen.includes(p.slug))
    .sort((a, b) => statusRank(a) - statusRank(b) || a.id - b.id)
  for (const p of rest) {
    chosen.push(p.slug)
    if (chosen.length >= needed) break
  }
  return chosen
}

/** 把题目均匀排进每一天，每天不超过 dailyGoal，不循环复用同一题。 */
export function buildSchedule(
  slugs: string[],
  totalDays: number,
  dailyGoal: number,
): Record<number, string[]> {
  const days = Math.max(0, totalDays)
  const cap = Math.max(0, dailyGoal)
  const schedule: Record<number, string[]> = {}
  const use = Math.min(slugs.length, days * cap)
  const counts = Array<number>(days).fill(0)
  if (days > 0 && use > 0) {
    const base = Math.floor(use / days)
    let extra = use % days
    for (let i = 0; i < days; i++) {
      counts[i] = base + (extra > 0 ? 1 : 0)
      if (extra > 0) extra -= 1
    }
  }
  let ptr = 0
  for (let day = 1; day <= days; day++) {
    const n = counts[day - 1] ?? 0
    schedule[day] = slugs.slice(ptr, ptr + n)
    ptr += n
  }
  return schedule
}

export interface PresetPlanConfig {
  id: string
  title: string
  tagline: string
  badge: string
  totalDays: number
  dailyGoal: number
  categoryTags: string[]
  recommendedSlugs: string[]
}

export const PRESET_PLANS: PresetPlanConfig[] = [
  {
    id: 'autumn-14',
    title: '⚡ 14 天秋招手撕核心突击计划',
    tagline: '精选高频双指针、链表、二叉树与经典动态规划，每天 2~3 题夯实手撕基础',
    badge: '🔥 秋招爆款',
    totalDays: 14,
    dailyGoal: 2,
    categoryTags: ['双指针', '二叉树', '动态规划', '链表', '回溯'],
    recommendedSlugs: [
      'two-sum', '3sum', 'container-with-most-water', 'move-zeroes',
      'reverse-linked-list', 'merge-two-sorted-lists', 'linked-list-cycle', 'linked-list-cycle-ii',
      'binary-tree-inorder-traversal', 'maximum-depth-of-binary-tree', 'invert-binary-tree', 'diameter-of-binary-tree',
      'binary-tree-level-order-traversal', 'lowest-common-ancestor-of-a-binary-tree', 'path-sum-iii', 'binary-tree-maximum-path-sum',
      'climbing-stairs', 'house-robber', 'coin-change', 'longest-increasing-subsequence',
      'permutations', 'subsets', 'combination-sum', 'word-search',
      'valid-parentheses', 'daily-temperatures', 'number-of-islands', 'top-k-frequent-elements',
    ],
  },
  {
    id: 'dp-7',
    title: '🧠 7 天经典动态规划攻坚专训',
    tagline: '从基础递推、背包状态转移到区间与子序列 DP，一举拿下面试最难骨头',
    badge: '🎯 专题攻坚',
    totalDays: 7,
    dailyGoal: 2,
    categoryTags: ['动态规划'],
    recommendedSlugs: [
      'climbing-stairs', 'min-cost-climbing-stairs',
      'house-robber', 'house-robber-ii',
      'coin-change', 'partition-equal-subset-sum',
      'longest-increasing-subsequence', 'longest-common-subsequence',
      'word-break', 'perfect-squares',
      'unique-paths', 'maximum-subarray',
      'best-time-to-buy-and-sell-stock', 'maximum-product-subarray',
    ],
  },
  {
    id: 'tree-10',
    title: '🌳 10 天二叉树与图论深度特训',
    tagline: 'DFS/BFS 遍历模式框架化，彻底掌握递归回溯与拓扑排序',
    badge: '🌲 树与图论',
    totalDays: 10,
    dailyGoal: 2,
    categoryTags: ['二叉树', '图论'],
    recommendedSlugs: [
      'binary-tree-inorder-traversal', 'maximum-depth-of-binary-tree',
      'invert-binary-tree', 'symmetric-tree',
      'diameter-of-binary-tree', 'balanced-binary-tree',
      'binary-tree-level-order-traversal', 'binary-tree-right-side-view',
      'construct-binary-tree-from-preorder-and-inorder-traversal', 'flatten-binary-tree-to-linked-list',
      'validate-binary-search-tree', 'kth-smallest-element-in-a-bst',
      'lowest-common-ancestor-of-a-binary-tree', 'path-sum-iii',
      'number-of-islands', 'rotting-oranges',
      'course-schedule', 'course-schedule-ii',
      'implement-trie-prefix-tree', 'binary-tree-maximum-path-sum',
    ],
  },
  {
    id: 'hot100-30',
    title: '🏆 30 天力扣热题 100 完整轮刷',
    tagline: '全量 100 道大厂必考热题地毯式通关，从零基础稳步进阶斩获大厂 Offer',
    badge: '👑 全量通关',
    totalDays: 30,
    dailyGoal: 3,
    categoryTags: ['全部'],
    recommendedSlugs: [],
  },
]

const STORAGE_KEY = 'leetpath_active_study_plan'

function normalizePlan(raw: StudyPlan): StudyPlan {
  const totalDays = clampPlanDays(raw.totalDays)
  const startDate = raw.startDate || todayLocalDate()
  return {
    ...raw,
    totalDays,
    dailyGoal: clampPlanGoal(raw.dailyGoal),
    startDate,
    endDate: raw.endDate || endDateFromStart(startDate, totalDays),
    schedule: raw.schedule || {},
    punchRecords: raw.punchRecords || {},
  }
}

function loadSavedPlan(): StudyPlan | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return normalizePlan(JSON.parse(raw) as StudyPlan)
  } catch {
    return null
  }
}

const activePlan = ref<StudyPlan | null>(loadSavedPlan())

export function useStudyPlan() {
  function getTodayDateStr(): string {
    return todayLocalDate()
  }

  function savePlan() {
    if (activePlan.value) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(activePlan.value))
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }

  function activatePreset(
    preset: PresetPlanConfig,
    allProblems: ProblemListItem[],
    startDate = todayLocalDate(),
  ) {
    const totalDays = clampPlanDays(preset.totalDays)
    const dailyGoal = clampPlanGoal(preset.dailyGoal)
    const needed = totalDays * dailyGoal
    const slugs = pickPlanSlugs(allProblems, needed, preset.recommendedSlugs)
    const schedule = buildSchedule(slugs, totalDays, dailyGoal)

    activePlan.value = {
      id: preset.id,
      title: preset.title,
      tagline: preset.tagline,
      badge: preset.badge,
      totalDays,
      dailyGoal,
      startDate,
      endDate: endDateFromStart(startDate, totalDays),
      schedule,
      punchRecords: {},
    }
    savePlan()
  }

  function createCustomPlan(
    title: string,
    totalDays: number,
    dailyGoal: number,
    allProblems: ProblemListItem[],
    startDate = todayLocalDate(),
  ): { ok: boolean; message: string } {
    if (allProblems.length === 0) {
      return { ok: false, message: '题库为空，无法制定计划' }
    }
    const days = clampPlanDays(totalDays)
    const goal = clampPlanGoal(dailyGoal)
    const start = startDate || todayLocalDate()
    const needed = days * goal
    const slugs = pickPlanSlugs(allProblems, needed)
    const schedule = buildSchedule(slugs, days, goal)
    const endDate = endDateFromStart(start, days)

    activePlan.value = {
      id: `custom-${Date.now()}`,
      title: title.trim() || `🎯 我的 ${days} 天打卡计划`,
      tagline: `每日目标 ${goal} 题，坚持 ${days} 天突破算法瓶颈！`,
      badge: '✨ 自定义计划',
      totalDays: days,
      dailyGoal: goal,
      startDate: start,
      endDate,
      schedule,
      punchRecords: {},
    }
    savePlan()
    return { ok: true, message: '' }
  }

  function resetPlan() {
    activePlan.value = null
    savePlan()
  }

  function recordSolvedProblem(slug: string) {
    if (!activePlan.value) return
    const todayStr = todayLocalDate()
    const dayIdx = dayIndexOn(activePlan.value.startDate, activePlan.value.totalDays, todayStr)
    if (dayIdx == null) return
    const rec = activePlan.value.punchRecords[todayStr] || {
      solvedSlugs: [],
      completed: false,
    }

    if (!rec.solvedSlugs.includes(slug)) {
      rec.solvedSlugs.push(slug)
    }

    const todayQuota = activePlan.value.schedule[dayIdx] || []
    const quota = todayQuota.length > 0 ? todayQuota.length : activePlan.value.dailyGoal
    rec.completed = quota > 0 && rec.solvedSlugs.length >= quota

    activePlan.value.punchRecords[todayStr] = rec
    savePlan()
  }

  const planEndDate = computed(() => {
    if (!activePlan.value) return ''
    return activePlan.value.endDate || endDateFromStart(activePlan.value.startDate, activePlan.value.totalDays)
  })

  const planPhase = computed<PlanPhase>(() => {
    if (!activePlan.value) return 'idle'
    const today = todayLocalDate()
    if (today < activePlan.value.startDate) return 'upcoming'
    if (today > planEndDate.value) return 'ended'
    return 'active'
  })

  const currentDayIndex = computed(() => {
    if (!activePlan.value) return null
    return dayIndexOn(activePlan.value.startDate, activePlan.value.totalDays, todayLocalDate())
  })

  const todayTargetSlugs = computed(() => {
    if (!activePlan.value || currentDayIndex.value == null) return []
    return activePlan.value.schedule[currentDayIndex.value] || []
  })

  const todayProgress = computed(() => {
    if (!activePlan.value) return { count: 0, completed: false }
    const rec = activePlan.value.punchRecords[todayLocalDate()]
    if (!rec) return { count: 0, completed: false }
    return {
      count: rec.solvedSlugs.length,
      completed: rec.completed,
    }
  })

  const completedDaysCount = computed(() => {
    if (!activePlan.value) return 0
    const start = activePlan.value.startDate
    const days = activePlan.value.totalDays
    return Object.entries(activePlan.value.punchRecords).filter(([iso, rec]) => {
      return rec.completed && dayIndexOn(start, days, iso) != null
    }).length
  })

  const planProgressPercent = computed(() => {
    if (!activePlan.value || activePlan.value.totalDays <= 0) return 0
    return Math.min(100, Math.round((completedDaysCount.value / activePlan.value.totalDays) * 100))
  })

  return {
    activePlan,
    currentDayIndex,
    planPhase,
    planEndDate,
    todayTargetSlugs,
    todayProgress,
    completedDaysCount,
    planProgressPercent,
    activatePreset,
    createCustomPlan,
    resetPlan,
    recordSolvedProblem,
    getTodayDateStr,
  }
}
