import { defineStore } from 'pinia'
import { api, ApiError } from '../api'
import type { User } from '../types'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    me: null as User | null,
    loaded: false,
  }),
  actions: {
    async fetchMe() {
      try {
        this.me = await api.get<User>('/api/auth/me')
      } catch {
        this.me = null
      } finally {
        this.loaded = true
      }
    },
    async login(username: string, password: string) {
      this.me = await api.post<User>('/api/auth/login', { username, password })
      this.loaded = true
    },
    async register(username: string, password: string, inviteCode: string, email?: string) {
      this.me = await api.post<User>('/api/auth/register', {
        username,
        password,
        email: email || undefined,
        invite_code: inviteCode,
      })
      this.loaded = true
    },
    async logout() {
      await api.post('/api/auth/logout')
      this.me = null
    },
  },
})
