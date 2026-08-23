export type Theme = 'light' | 'dark' | 'cyber'

const KEY = 'leetpath-theme'

export function getTheme(): Theme {
  const current = document.documentElement.dataset.theme
  if (current === 'cyber') return 'cyber'
  if (current === 'dark') return 'dark'
  return 'light'
}

export function setTheme(t: Theme) {
  document.documentElement.dataset.theme = t
  localStorage.setItem(KEY, t)
}

export function toggleTheme(): Theme {
  const current = getTheme()
  let next: Theme = 'light'
  if (current === 'light') next = 'dark'
  else if (current === 'dark') next = 'cyber'
  else next = 'light'

  setTheme(next)
  return next
}

/** 应用挂载前调用：恢复用户上次选择 */
export function initTheme() {
  const saved = localStorage.getItem(KEY) as Theme | null
  if (saved === 'cyber' || saved === 'dark' || saved === 'light') {
    document.documentElement.dataset.theme = saved
  } else {
    document.documentElement.dataset.theme = 'light'
  }
}
