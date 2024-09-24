<template>
  <v-chip
    :title="theuser.first_name + ' ' + theuser.last_name"
    v-if="theuser"
    :text="theuser.username"
    prepend-icon="mdi-account"
  />
  <v-chip color="grey" variant="text" v-else text="None" />
</template>

<script setup lang="ts">
import type { User } from '@/types'
import axios, { AxiosResponse } from 'axios'

const props = defineProps<{
  user?: number
}>()

const theuser = ref<User | null>(null)

watchEffect(() => {
  if (!props.user) {
    theuser.value = null
    return
  }
  axios
    .get(`/api/tasks/users/${props.user}/`)
    .then((response: AxiosResponse) => {
      theuser.value = response.data
    })
    .catch((err: Error) => {
      theuser.value = null
      console.error(err)
    })
})
</script>
