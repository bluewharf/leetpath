import { ref } from 'vue'

export type ToastType = 'success' | 'error' | 'info'

export interface ToastItem {
  id: number
  type: ToastType
  message: string
  duration?: number
}

const toasts = ref<ToastItem[]>([])
let nextId = 1

export function useToast() {
  function show(message: string, type: ToastType = 'info', duration = 3000) {
    const id = nextId++
    toasts.value.push({ id, type, message, duration })
    if (duration > 0) {
      setTimeout(() => {
        dismiss(id)
      }, duration)
    }
    return id
  }

  function success(message: string, duration = 3000) {
    return show(message, 'success', duration)
  }

  function error(message: string, duration = 4000) {
    return show(message, 'error', duration)
  }

  function info(message: string, duration = 3000) {
    return show(message, 'info', duration)
  }

  function dismiss(id: number) {
    toasts.value = toasts.value.filter((t) => t.id !== id)
  }

  return {
    toasts,
    show,
    success,
    error,
    info,
    dismiss,
  }
}
