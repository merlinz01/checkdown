<template>
  <v-card title="Logging out..." />
</template>

<script setup lang="ts">
import { getResponseErrorMessage } from '@/plugins/axios'
import useNotify from '@/stores/notify'
import { useUserStore } from '@/stores/user'
import axios, { AxiosError } from 'axios'

const router = useRouter()
const notify = useNotify()
const user = useUserStore()

function logout() {
  axios
    .post('/api/tasks/logout/')
    .then(() => {
      user.user = null
      router.push({ path: '/login' })
    })
    .catch((err: AxiosError) => {
      err && notify.error(getResponseErrorMessage(err))
    })
}

onMounted(() => {
  logout()
})
</script>
