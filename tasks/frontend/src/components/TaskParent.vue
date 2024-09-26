<template>
  <v-breadcrumbs class="py-1 px-0 v-label flex-wrap" divider=">" :items="breadcrumbs" />
</template>

<script setup lang="ts">
import type { Task } from '@/types'
import axios from '@/plugins/axios'

const parentTasks = ref<Task[]>([])
const breadcrumbs = computed(() => {
  const b: any[] = parentTasks.value.map((task) => ({
    title: task.name,
    to: `/tasks/${task.pk}/`,
  }))
  b.unshift({ title: 'Tasks', to: '/tasks/' })
  b.push({ title: props.task.name })
  return b
})
const props = defineProps<{
  task: Task
}>()

watchEffect(async () => {
  var parent = props.task.parent
  while (parent) {
    const response = await axios.get(`/api/tasks/tasks/${parent}/`)
    const data = response.data
    parentTasks.value.unshift(data)
    parent = data.parent
  }
})
</script>
