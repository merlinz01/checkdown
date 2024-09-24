/**
 * plugins/index.ts
 *
 * Automatically included in `./src/main.ts`
 */

// Plugins
import vuetify from './vuetify'
import pinia from '../stores'
import router from '../router'

// Types
import type { App } from 'vue'
import { registerAxios } from './axios'

export function registerPlugins(app: App) {
  registerAxios(router)
  app.use(vuetify).use(router).use(pinia)
}
