import { User } from '@/types'
import { defineStore } from 'pinia'

export const useUserStore = defineStore('user', () => {
  const user = ref<User | null>()
  return { user }
})
