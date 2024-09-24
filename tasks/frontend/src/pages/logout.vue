<template>
  <v-card title="Logging out..." />
</template>

<script setup lang="ts">
import useNotify from '@/stores/notify'
import { useUserStore } from '@/stores/user'
import axios, { AxiosResponse } from 'axios'

const router = useRouter()
const notify = useNotify()
const user = useUserStore()

function logout() {
  axios
    .post('/api/tasks/logout/')
    .then((response: AxiosResponse) => {
      user.user = null
      router.push({ path: '/login' })
    })
    .catch((err: Error) => {
      err && notify.error(err)
    })
}

onMounted(() => {
  logout()
})
</script>
