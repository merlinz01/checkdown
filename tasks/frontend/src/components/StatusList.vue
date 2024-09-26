<template>
  <v-list density="compact">
    <v-list-item v-for="status in statuses" :key="status.pk" @click="selectStatus(status)">
      <v-list-item-title
        ><v-chip
          label
          :text="status.name"
          :color="status.color"
          variant="elevated"
          density="comfortable"
      /></v-list-item-title>
    </v-list-item>
  </v-list>
</template>

<script setup lang="ts">
import type { Status } from '@/types'
import { AxiosResponse } from 'axios'
import axios from '@/plugins/axios'

const statuses = ref<Status[]>([])
const status = defineModel<number>()

onMounted(() => {
  axios
    .get('/api/tasks/statuses/')
    .then((response: AxiosResponse) => {
      statuses.value = response.data
    })
    .catch((err: Error) => {
      statuses.value = []
      console.error(err)
    })
})

function selectStatus(selected: Status) {
  status.value = selected.pk
}
</script>
