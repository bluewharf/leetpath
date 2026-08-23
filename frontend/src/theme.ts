export type Theme = 'light' | 'dark'

const KEY = 'leetpath-theme'

export function getTheme(): Theme {
  return document.documentElement.dataset.theme === 'dark' ? 'dark' : 'light'
}

export function setTheme(t: Theme) {
  document.documentElement.dataset.theme = t
  localStorage.setItem(KEY, t)
}

export function toggleTheme(): Theme {
  const next = getTheme() === 'dark' ? 'light' : 'dark'
  setTheme(next)
  return next
}

/** 应用挂载前调用：恢复用户上次选择；默认浅色（暖纸风格） */
export function initTheme() {
  const saved = localStorage.getItem(KEY)
  document.documentElement.dataset.theme = saved === 'dark' ? 'dark' : 'light'
}
