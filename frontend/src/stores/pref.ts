import { ref } from 'vue'
import type { Language } from '../types'

const saved = localStorage.getItem('leetpath_lang_pref') as Language | null
const langPref = ref<Language>(saved === 'cpp' ? 'cpp' : 'python3')

export function useLangPref() {
  function setLang(l: Language) {
    langPref.value = l
    localStorage.setItem('leetpath_lang_pref', l)
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
