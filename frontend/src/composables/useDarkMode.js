import { ref } from 'vue'

const STORAGE_KEY = 'theme'

function prefersDark() {
  return window.matchMedia('(prefers-color-scheme: dark)').matches
}

function getInitial() {
  const stored = localStorage.getItem(STORAGE_KEY)
  if (stored === 'dark') return true
  if (stored === 'light') return false
  return prefersDark()
}

export const isDark = ref(getInitial())

function apply(value) {
  document.documentElement.classList.toggle('dark', value)
}

apply(isDark.value)

export function toggleDark() {
  isDark.value = !isDark.value
  localStorage.setItem(STORAGE_KEY, isDark.value ? 'dark' : 'light')
  apply(isDark.value)
}

export function useDarkMode() {
  return { isDark, toggleDark }
}
