import { ref } from 'vue'
import type { Language } from '../types'

export type FontSize = 'sm' | 'md' | 'lg'

const LANG_KEY = 'leetpath_lang_pref'
const savedLang = localStorage.getItem(LANG_KEY) as Language | null
const langPref = ref<Language>(savedLang === 'cpp' ? 'cpp' : 'python3')

export function useLangPref() {
  function setLang(l: Language) {
    langPref.value = l
    localStorage.setItem(LANG_KEY, l)
  }

  function toggleLang() {
    setLang(langPref.value === 'python3' ? 'cpp' : 'python3')
  }

  return {
    langPref,
    setLang,
    toggleLang,
  }
}

const FONT_KEY = 'leetpath_font_size'
const savedFontSize = (localStorage.getItem(FONT_KEY) as FontSize | null) || 'md'
const fontSize = ref<FontSize>(savedFontSize)

export function initFontSize() {
  const current = (localStorage.getItem(FONT_KEY) as FontSize | null) || 'md'
  fontSize.value = current
  document.documentElement.dataset.fontSize = current
}

export function useFontSize() {
  function setFontSize(size: FontSize) {
    fontSize.value = size
    localStorage.setItem(FONT_KEY, size)
    document.documentElement.dataset.fontSize = size
  }

  function cycleFontSize() {
    let next: FontSize = 'md'
    if (fontSize.value === 'sm') next = 'md'
    else if (fontSize.value === 'md') next = 'lg'
    else next = 'sm'
    setFontSize(next)
  }

  return {
    fontSize,
    setFontSize,
    cycleFontSize,
  }
}
