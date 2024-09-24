<template>
  <v-chip
    :color="thestatus?.color"
    text-color="white"
    :title="thestatus?.description"
    label
    variant="flat"
    density="comfortable"
    :text="thestatus?.name"
    v-if="thestatus"
  />
  <v-chip color="primary" label v-else text="New" density="comfortable" />
</template>

<script setup lang="ts">
import type { Status } from '@/types'
import axios, { AxiosResponse } from 'axios'

const props = defineProps<{
  status?: number | null
}>()

const thestatus = ref<Status | null>(null)

watchEffect(() => {
  if (!props.status) {
    thestatus.value = null
    return
  }
  axios
    .get(`/api/tasks/statuses/${props.status}/`)
    .then((response: AxiosResponse) => {
      thestatus.value = response.data
    })
    .catch((err: Error) => {
      thestatus.value = null
      console.error(err)
    })
})
</script>
