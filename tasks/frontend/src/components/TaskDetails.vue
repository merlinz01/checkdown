<template>
  <v-card>
    <v-card-title>
      <div class="d-flex flex-column">
        <TaskParent :task="task" />
        <div class="d-flex flex-wrap">
          <div
            v-text="task.name"
            v-if="!editingName"
            @click="editingName = true"
            class="ma-1 text-wrap"
          ></div>
          <v-form v-else @submit.prevent="saveName" class="d-flex w-100 ga-2 align-center">
            <label for="name">Edit name:</label>
            <v-text-field
              v-model="newName"
              density="compact"
              @keydown.escape="editingName = false"
              hide-details
            >
              <template #append>
                <v-btn type="submit" icon="mdi-check" density="comfortable" />
                <v-btn @click="editingName = false" icon="mdi-close" density="comfortable" />
              </template>
            </v-text-field>
          </v-form>
          <v-menu offset-y v-if="!editingName">
            <template #activator="{ props }">
              <StatusChip :status="task.status" v-bind="props" class="mx-4 my-1" />
            </template>
            <StatusList
              v-model="task.status"
              @update:model-value="saveStatus"
              class="bg-surface-light"
            />
          </v-menu>
          <v-btn
            icon="mdi-trash-can-outline"
            @click="deleteTask"
            v-if="!editingName"
            class="ms-auto"
            title="Delete task"
            color="red"
            variant="text"
            density="comfortable"
          />
        </div>
        <v-divider class="mt-2" />
      </div>
    </v-card-title>
    <v-card-text>
      <div class="d-flex flex-column ga-3 ma-2">
        <v-label
          for="description"
          v-if="!editingDescription"
          @click="editingDescription = !editingDescription"
          text="Description"
          class="mt-2"
        />
        <vue-showdown
          :markdown="task.description"
          v-if="!editingDescription"
          @click="editingDescription = true"
          id="description"
          class="mx-4 my-2 markdown-content"
        />
        <v-form v-else @submit.prevent="editingDescription = false" class="d-flex flex-column ga-2">
          <div class="d-flex w-100 align-center">
            <v-label for="description" class="me-auto">Description</v-label>
            <v-btn type="submit" icon="mdi-check" density="comfortable" @click="saveDescription" />
            <v-btn @click="editingDescription = false" icon="mdi-close" density="comfortable" />
          </div>
          <div class="d-flex">
            <v-textarea
              v-model="newDescription"
              class="mb-2"
              @keydown.escape="editingDescription = false"
              hide-details
              id="description"
              density="comfortable"
              style="flex-basis: 50%"
              auto-grow
              placeholder="Enter task description"
            />
            <vue-showdown
              :markdown="newDescription"
              class="markdown-content"
              style="flex-basis: 50%"
            />
          </div>
        </v-form>
        <div class="d-flex align-center">
          <v-label for="due_date" text="Due Date:" class="me-4" />
          <v-menu offset-y :close-on-content-click="false" v-model="editingDueDate">
            <template #activator="{ props }">
              <v-btn
                v-text="task._due_date?.toDateString() || 'No due date'"
                class="mx-4 cursor-pointer text-none"
                v-bind="props"
                variant="flat"
                color="grey"
              ></v-btn>
            </template>
            <v-form class="d-flex flex-column" @submit.prevent="saveDueDate()">
              <v-date-picker
                v-model="newDueDate"
                id="due_date"
                show-adjacent-months
                header="No due date"
                color="surface-light"
              >
                <template #title>
                  <div class="d-flex align-center">
                    <v-btn
                      text="Remove"
                      variant="flat"
                      @click="newDueDate = undefined"
                      v-if="newDueDate"
                    />
                    <v-btn type="submit" icon="mdi-check" density="comfortable" class="ms-auto" />
                  </div>
                </template>
              </v-date-picker>
            </v-form>
          </v-menu>
        </div>
        <div class="d-flex align-center">
          <v-label for="assignee" text="Assignee:" class="me-4" />
          <v-menu offset-y v-if="!editingName">
            <template #activator="{ props }">
              <UserChip :user="task.assignee" v-bind="props" class="mx-4 me-auto" id="assignee" />
            </template>
            <UserList v-model="task.assignee" @update:model-value="saveAssignee" include-null />
          </v-menu>
        </div>
        <div class="d-flex align-center">
          <v-label for="priority" text="Priority:" class="me-8" />
          <v-select
            v-model="task.priority"
            :items="priorities"
            id="priority"
            density="compact"
            class="mx-4 flex-grow-0"
            hide-details
            :style="{ color: priorities.find((p) => p.value === task.priority)?.color }"
            @update:model-value="savePriority"
          />
        </div>
        <v-divider class="my-1" />
        <TaskList :parent="task.pk" title="Subtasks" />
      </div>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import getCSRFToken from '@/csrftoken'
import { priorities, type Task } from '@/types'
import { VueShowdown } from 'vue-showdown'

const props = defineProps<{
  task: Task
}>()
const editingName = ref(false)
const newName = ref(props.task.name)
const editingDescription = ref(false)
const newDescription = ref(props.task.description)
const editingDueDate = ref(false)
const newDueDate = ref(props.task._due_date)
const router = useRouter()

function saveStatus(status: number) {
  fetch(`/api/tasks/tasks/${props.task.pk}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({ status }),
  })
}

function saveName() {
  fetch(`/api/tasks/tasks/${props.task.pk}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({ name: newName.value }),
  }).then(() => {
    editingName.value = false
    props.task.name = newName.value
  })
}

function saveDescription() {
  fetch(`/api/tasks/tasks/${props.task.pk}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({ description: newDescription.value }),
  }).then(() => {
    editingDescription.value = false
    props.task.description = newDescription.value
  })
}

function saveDueDate() {
  fetch(`/api/tasks/tasks/${props.task.pk}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({
      due_date: newDueDate.value?.toISOString().substring(0, 10) || null,
    }),
  }).then(() => {
    editingDueDate.value = false
    props.task._due_date = newDueDate.value
    props.task.due_date = newDueDate.value?.toISOString().substring(0, 10)
  })
}

function saveAssignee(assignee: number | null) {
  fetch(`/api/tasks/tasks/${props.task.pk}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({ assignee }),
  })
}

function savePriority(priority: number) {
  fetch(`/api/tasks/tasks/${props.task.pk}/`, {
    method: 'PATCH',
    headers: {
      'Content-Type': 'application/json',
      'X-CSRFToken': getCSRFToken(),
    },
    body: JSON.stringify({ priority }),
  })
}

function deleteTask() {
  if (!confirm('Are you sure you want to delete this task and all sub-tasks?')) {
    return
  }
  fetch(`/api/tasks/tasks/${props.task.pk}/`, {
    method: 'DELETE',
    headers: {
      'X-CSRFToken': getCSRFToken(),
    },
  }).then(() => {
    router.push('/')
  })
}
</script>

<style>
.markdown-content {
  font-size: 1rem;
  margin: 1em;
}
.markdown-content ol li,
.markdown-content ul li {
  margin-left: 1.5em;
}
</style>
