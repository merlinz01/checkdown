<template>
  <v-list density="compact">
    <v-list-item v-if="includeNull" @click="selectUser(null)">
      <v-list-item-title><v-chip text="None" color="grey" /></v-list-item-title>
    </v-list-item>
    <v-list-item v-for="status in users" :key="status.pk" @click="selectUser(status)">
      <v-list-item-title
        ><v-chip :text="status.username" prepend-icon="mdi-account" />
      </v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script setup lang="ts">
import type { User } from '@/types'
import axios, { AxiosResponse } from 'axios'

const users = ref<User[]>([])
const user = defineModel<number | null>()
defineProps<{ includeNull?: boolean }>()

onMounted(() => {
  axios
    .get('/api/tasks/users/')
    .then((response: AxiosResponse) => {
      users.value = response.data
    })
    .catch((err: Error) => {
      users.value = []
      console.error(err)
    })
})

function selectUser(selected: User | null) {
  user.value = selected?.pk || null
}
</script>
