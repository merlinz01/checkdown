<template>
  <v-app :theme="colorTheme">
    <v-app-bar app height="48" class="align-center">
      <v-img src="./assets/logo.png" height="36" width="36" class="flex-grow-0 mx-4" />
      <v-app-bar-title class="flex-0-0 mx-auto">Checkdown Tasks</v-app-bar-title>
    </v-app-bar>
    <v-main class="bg-surface-light">
      <v-container>
        <v-responsive class="align-center mx-auto" max-width="900">
          <router-view />
        </v-responsive>
      </v-container>
    </v-main>
    <v-footer app height="40">
      <v-btn
        icon="mdi-theme-light-dark"
        @click="toggleTheme"
        density="comfortable"
        title="Toggle color theme"
        class="my-0"
        :rounded="false"
        color="primary"
        variant="text"
      />
      <v-btn
        href="/admin/"
        icon="mdi-cog"
        density="comfortable"
        variant="tonal"
        color="secondary"
        title="Checkdown Administration"
      />
      <v-spacer />
      <v-menu v-if="user.user">
        <template #activator="{ props }">
          <v-chip :text="user.user.username" prepend-icon="mdi-account" v-bind="props" />
        </template>
        <v-list>
          <v-list-item title="Logout" to="/logout" />
        </v-list>
      </v-menu>
    </v-footer>
    <v-snackbar
      v-for="(n, i) of notify.notifications"
      :color="n.type"
      :model-value="true"
      :text="n.message"
      :timeout="-1"
      :style="{
        transform: `translateY(${(notify.notifications.length - i - 1) * -50}px)`,
      }"
      :key="n.id"
    >
      <template #actions="{ isActive }">
        <v-btn
          v-bind="isActive"
          @click="notify.removeNotification(n.id)"
          color="white"
          icon="mdi-close"
          density="comfortable"
        />
      </template>
    </v-snackbar>
  </v-app>
</template>

<script setup lang="ts">
import useNotify from '@/stores/notify'
import { useUserStore } from './stores/user'
import axios, { AxiosResponse } from 'axios'

const notify = useNotify()
const user = useUserStore()
const colorTheme = ref('dark')
const toggleTheme = () => {
  colorTheme.value = colorTheme.value === 'light' ? 'dark' : 'light'
  document.documentElement.style.colorScheme = colorTheme.value
  localStorage.setItem('colorTheme', colorTheme.value)
}

onMounted(() => {
  colorTheme.value =
    localStorage.getItem('colorTheme') ||
    (window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light')
  document.documentElement.style.colorScheme = colorTheme.value
  axios.get('/api/tasks/whoami').then((response: AxiosResponse) => {
    user.user = response.data
  })
})
</script>
