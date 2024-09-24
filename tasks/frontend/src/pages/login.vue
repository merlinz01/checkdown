<template>
  <v-card>
    <v-card-title>Login</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="login">
        <v-text-field v-model="username" label="Username" />
        <v-text-field v-model="password" label="Password" type="password" />
        <v-btn type="submit">Login</v-btn>
      </v-form>
    </v-card-text>
  </v-card>
</template>

<script setup lang="ts">
import useNotify from '@/stores/notify'
import { useUserStore } from '@/stores/user'
import axios, { AxiosResponse } from 'axios'

const username = ref('')
const password = ref('')
const router = useRouter()
const notify = useNotify()
const user = useUserStore()

function login() {
  axios
    .post('/api/tasks/login/', undefined, {
      headers: {
        Authorization: `Basic ${btoa(username.value + ':' + password.value)}`,
      },
    })
    .then((response: AxiosResponse) => {
      router.push({ path: '/' })
      user.user = response.data.user
    })
    .catch((err: Error) => {
      err && notify.error(err)
    })
}

onMounted(() => {
  user.user = null
})
</script>

<style>
/* This allows Bitwarden to fill in the login form */
/* https://github.com/vuetifyjs/vuetify/issues/20218 */
.v-text-field input[type] {
  opacity: 1;
  transition: none;
}

.v-text-field input::placeholder {
  opacity: 0;
  transition: 0.15s opacity cubic-bezier(0.4, 0, 0.2, 1);
}

.v-text-field .v-field--no-label input::placeholder,
.v-text-field .v-field--active input::placeholder {
  opacity: 0.5;
}
</style>
