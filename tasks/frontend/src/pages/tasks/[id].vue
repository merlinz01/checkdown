<template>
  <TaskDetails v-if="task" :task="task" />
  <v-alert v-else-if="err" type="error">{{ err }}</v-alert>
  <v-alert v-else type="info">Loading...</v-alert>
</template>

<script setup lang="ts">
import type { Task } from '@/types'
import { useDate } from 'vuetify'

const route = useRoute<'/tasks/[id]'>()
const task = ref<Task | null>(null)
const err = ref<string | null>(null)
const date = useDate()

watchEffect(async () => {
  const taskid = route.params.id
  err.value = null
  try {
    const response = await fetch(`/api/tasks/tasks/${taskid}/`)
    if (!response.ok) {
      throw new Error(`${response.status} ${response.statusText} ${await response.text()}`)
    }
    task.value = await response.json()
    if (task.value && task.value.due_date) {
      task.value._due_date = date.parseISO(task.value.due_date) as Date
    }
  } catch (error) {
    err.value = String(error)
  }
})
</script>
