export type Theme = 'light' | 'dark' | 'cyber' | 'sepia'

const KEY = 'leetpath-theme'
const THEMES: Theme[] = ['light', 'dark', 'cyber', 'sepia']

export function getTheme(): Theme {
  const current = document.documentElement.dataset.theme
  if (current === 'cyber') return 'cyber'
  if (current === 'dark') return 'dark'
  if (current === 'sepia') return 'sepia'
  return 'light'
}

export function setTheme(t: Theme) {
  document.documentElement.dataset.theme = t
  localStorage.setItem(KEY, t)
}

export function toggleTheme(): Theme {
  const current = getTheme()
  const next = THEMES[(THEMES.indexOf(current) + 1) % THEMES.length]

  setTheme(next)
  return next
}

/** 应用挂载前调用：恢复用户上次选择 */
export function initTheme() {
  const saved = localStorage.getItem(KEY) as Theme | null
  if (saved && THEMES.includes(saved)) {
    document.documentElement.dataset.theme = saved
  } else {
    // 首访跟随系统深浅色偏好
    const prefersDark = window.matchMedia?.('(prefers-color-scheme: dark)').matches
    document.documentElement.dataset.theme = prefersDark ? 'dark' : 'light'
  }
}
