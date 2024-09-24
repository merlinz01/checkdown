<template>
  <div class="d-flex flex-column ga-2">
    <div class="d-flex align-center">
      <v-label for="task-table" :text="title" class="mt-1" />
      <v-text-field
        v-if="items.length > 0"
        v-model="search"
        label="Search"
        prepend-inner-icon="mdi-magnify"
        hide-details
        single-line
        density="compact"
        @keydown.escape="search = ''"
        class="mx-4"
        max-width="300"
      />
      <v-checkbox
        v-model="showClosedSwitch"
        label="Show closed"
        v-if="showClosed === null"
        hide-details
      />
      <div class="mx-auto"></div>
      <v-btn
        v-if="!showNewTask"
        prepend-icon="mdi-plus"
        @click="showNewTask = true"
        color="primary"
        text="New"
        v-bind="props"
      />
      <v-form
        @submit.prevent="saveNewTask"
        v-if="showNewTask"
        class="d-flex ga-2 align-center"
        @keydown.escape="showNewTask = false"
      >
        <v-label text="Enter new task name:" class="mt-1" />
        <v-text-field
          v-model="newTaskName"
          id="new-task-name"
          label="Name"
          required
          min-width="200"
          density="compact"
          hide-details
          single-line
        />
        <v-btn
          type="submit"
          color="success"
          icon="mdi-check"
          density="comfortable"
          :disabled="!newTaskName"
        />
      </v-form>
    </div>
    <v-data-table
      id="task-table"
      :headers="headers"
      :items="items"
      :items-per-page="-1"
      class="elevation-1"
      hide-default-footer
      :hide-default-header="items.length === 0"
      no-data-text="No tasks found."
      @click:row="rowClick"
      density="comfortable"
      :search="search"
      item-value="pk"
      v-model:sort-by="sortby"
    >
      <template #item.status="{ item }">
        <StatusChip :status="item.status" />
      </template>
      <template #item.assignee="{ item }">
        <UserChip :user="item.assignee" v-if="item.assignee" />
      </template>
      <template #item.priority="{ item, value }">
        <span :style="{ color: priorities.find((p) => p.value === item.priority)?.color }">{{
          value
        }}</span>
      </template>
      <template v-slot:group-header="{ item, columns, toggleGroup, isGroupOpen }">
        <tr>
          <td :colspan="columns.length">
            <VBtn
              :icon="isGroupOpen(item) ? '$expand' : '$next'"
              size="small"
              variant="text"
              @click="toggleGroup(item)"
            ></VBtn>
            <StatusChip :status="item.value" />
          </td>
        </tr>
      </template>
    </v-data-table>
  </div>
</template>

<script setup lang="ts">
import { priorities, type Task } from '@/types'
import StatusChip from './StatusChip.vue'
import axios, { AxiosError } from 'axios'
import useNotify from '@/stores/notify'

const props = withDefaults(
  defineProps<{
    parent?: number
    title?: string
    showClosed?: boolean | null
  }>(),
  {
    title: 'Tasks',
    showClosed: null,
  }
)
const router = useRouter()
const headers: any[] = [
  { key: 'name', title: 'Task' },
  { key: 'status', title: 'Status' },
  { key: 'assignee', title: 'Assignee' },
  {
    key: 'priority',
    title: 'Priority',
    value: (t: Task) => priorities.find((p) => p.value === t.priority)?.title,
    sortRaw: (a: Task, b: Task) => a.priority - b.priority,
  },
  { key: 'due_date', title: 'Due Date' },
]
const items = ref<Task[]>([])
const showNewTask = ref(false)
const newTaskName = ref('')
const search = ref('')
const sortby = ref([{ key: 'priority', order: 'desc' }] as any[])
const notify = useNotify()
const showClosedSwitch = ref(false)

watchEffect(() => {
  var sc
  if (props.showClosed !== null) {
    sc = props.showClosed
  }
  sc = showClosedSwitch.value
  axios
    .get('/api/tasks/tasks/', {
      params: {
        parent: props.parent,
        closed: sc ? undefined : false,
      },
    })
    .then((response) => {
      items.value = response.data
    })
    .catch((err: AxiosError) => {
      items.value = []
      err && notify.error(err.message)
    })
})

function rowClick(event: MouseEvent, row: any) {
  const task = row.item as Task
  router.push(`/tasks/${task.pk}`)
}

function saveNewTask() {
  if (!newTaskName.value) {
    return
  }
  axios
    .post('/api/tasks/tasks/', {
      name: newTaskName.value,
      parent: props.parent,
    })
    .then((response) => {
      items.value.push(response.data)
      showNewTask.value = false
      notify.success(`Task "${newTaskName.value}" created.`)
      newTaskName.value = ''
    })
    .catch((err: Error) => {
      notify.error(String(err))
    })
}
</script>
