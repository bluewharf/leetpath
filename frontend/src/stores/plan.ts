import { computed, ref } from 'vue'
import type { ProblemListItem } from '../types'

export interface StudyPlan {
  id: string
  title: string
  tagline: string
  badge: string
  totalDays: number
  dailyGoal: number
  startDate: string // YYYY-MM-DD
  // 每天分配的题目 slug 列表 (1-indexed, day 1..totalDays)
  schedule: Record<number, string[]>
  // 打卡记录：key 为 "YYYY-MM-DD"
  punchRecords: Record<string, { solvedSlugs: string[]; completed: boolean }>
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

function loadSavedPlan(): StudyPlan | null {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw) as StudyPlan
  } catch {
    return null
  }
}

const activePlan = ref<StudyPlan | null>(loadSavedPlan())

export function useStudyPlan() {
  function getTodayDateStr(): string {
    const d = new Date()
    return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, '0')}-${String(d.getDate()).padStart(2, '0')}`
  }

  function savePlan() {
    if (activePlan.value) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(activePlan.value))
    } else {
      localStorage.removeItem(STORAGE_KEY)
    }
  }

  // 创建/激活预设计划
  function activatePreset(preset: PresetPlanConfig, allProblems: ProblemListItem[]) {
    const schedule: Record<number, string[]> = {}
    let slugsToUse = [...preset.recommendedSlugs]

    // 如果推荐列表不足，从题库中按对应标签补齐
    if (slugsToUse.length < preset.totalDays * preset.dailyGoal) {
      const candidates = allProblems
        .filter((p) => !slugsToUse.includes(p.slug))
        .map((p) => p.slug)
      slugsToUse = [...slugsToUse, ...candidates]
    }

    let ptr = 0
    for (let day = 1; day <= preset.totalDays; day++) {
      schedule[day] = []
      for (let g = 0; g < preset.dailyGoal; g++) {
        if (ptr < slugsToUse.length) {
          schedule[day].push(slugsToUse[ptr++])
        }
      }
    }

    activePlan.value = {
      id: preset.id,
      title: preset.title,
      tagline: preset.tagline,
      badge: preset.badge,
      totalDays: preset.totalDays,
      dailyGoal: preset.dailyGoal,
      startDate: getTodayDateStr(),
      schedule,
      punchRecords: {},
    }
    savePlan()
  }

  // 创建自定义计划
  function createCustomPlan(
    title: string,
    totalDays: number,
    dailyGoal: number,
    allProblems: ProblemListItem[],
  ) {
    const schedule: Record<number, string[]> = {}
    const slugs = allProblems.map((p) => p.slug)
    let ptr = 0

    for (let day = 1; day <= totalDays; day++) {
      schedule[day] = []
      for (let g = 0; g < dailyGoal; g++) {
        if (slugs.length > 0) {
          schedule[day].push(slugs[ptr % slugs.length])
          ptr++
        }
      }
    }

    activePlan.value = {
      id: `custom-${Date.now()}`,
      title: title || `🎯 我的 ${totalDays} 天打卡计划`,
      tagline: `每日目标 ${dailyGoal} 题，坚持 ${totalDays} 天突破算法瓶颈！`,
      badge: '✨ 自定义计划',
      totalDays,
      dailyGoal,
      startDate: getTodayDateStr(),
      schedule,
      punchRecords: {},
    }
    savePlan()
  }

  // 放弃/重置当前计划
  function resetPlan() {
    activePlan.value = null
    savePlan()
  }

  // 当用户通过一道题目时，记录打卡
  function recordSolvedProblem(slug: string) {
    if (!activePlan.value) return
    const todayStr = getTodayDateStr()
    const rec = activePlan.value.punchRecords[todayStr] || {
      solvedSlugs: [],
      completed: false,
    }

    if (!rec.solvedSlugs.includes(slug)) {
      rec.solvedSlugs.push(slug)
    }

    // 检查是否达到今日目标
    if (rec.solvedSlugs.length >= activePlan.value.dailyGoal) {
      rec.completed = true
    }

    activePlan.value.punchRecords[todayStr] = rec
    savePlan()
  }

  // 计算当前处于计划的第几天 (1-indexed)
  const currentDayIndex = computed(() => {
    if (!activePlan.value) return 1
    const start = new Date(activePlan.value.startDate).getTime()
    const today = new Date(getTodayDateStr()).getTime()
    const diffDays = Math.floor((today - start) / (1000 * 60 * 60 * 24)) + 1
    return Math.max(1, Math.min(diffDays, activePlan.value.totalDays))
  })

  // 今日分配的题目 slugs
  const todayTargetSlugs = computed(() => {
    if (!activePlan.value) return []
    return activePlan.value.schedule[currentDayIndex.value] || []
  })

  // 今日已完成打卡题数
  const todayProgress = computed(() => {
    if (!activePlan.value) return { count: 0, completed: false }
    const todayStr = getTodayDateStr()
    const rec = activePlan.value.punchRecords[todayStr]
    if (!rec) return { count: 0, completed: false }
    return {
      count: rec.solvedSlugs.length,
      completed: rec.completed,
    }
  })

  // 累计达标天数
  const completedDaysCount = computed(() => {
    if (!activePlan.value) return 0
    return Object.values(activePlan.value.punchRecords).filter((r) => r.completed).length
  })

  // 计划完成百分比 (已达标天数 / 总天数)
  const planProgressPercent = computed(() => {
    if (!activePlan.value || activePlan.value.totalDays <= 0) return 0
    return Math.min(100, Math.round((completedDaysCount.value / activePlan.value.totalDays) * 100))
  })

  return {
    activePlan,
    currentDayIndex,
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
