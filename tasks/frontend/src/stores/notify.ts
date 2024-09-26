import { defineStore } from 'pinia'

export type NotificationType = 'success' | 'info' | 'warning' | 'error'

export type NotificationOptions = {
  timeout?: number
}

export type Notification = {
  message: string
  type: NotificationType
  options?: NotificationOptions
}

type NotificationWrapper = Notification & {
  id: string
}

const useNotify = defineStore('notify', () => {
  const notifications = ref<NotificationWrapper[]>([])

  function addNotification(notification: Notification) {
    const id = Math.random().toString(36).substring(2, 9)
    if (!notification.options) notification.options = {}
    if (notification.options.timeout === undefined) notification.options.timeout = 10000
    notifications.value.push({
      ...notification,
      id: id,
    })
    if (notification.options.timeout) {
      setTimeout(() => {
        removeNotification(id)
      }, notification.options.timeout)
    }
  }

  function removeNotification(id: string) {
    notifications.value = notifications.value.filter((n) => n.id !== id)
  }

  function notify(message: any, type: Notification['type'], options?: NotificationOptions) {
    var themessage = String(message)
    if (typeof message == 'object' && themessage === '[object Object]') {
      themessage = JSON.stringify(message)
    }
    addNotification({ message: themessage, type, options })
  }

  function success(message: any, options?: NotificationOptions) {
    notify(message, 'success', options)
  }

  function info(message: any, options?: NotificationOptions) {
    notify(message, 'info', options)
  }

  function warning(message: any, options?: NotificationOptions) {
    notify(message, 'warning', options)
  }

  function error(message: Error | any, options?: NotificationOptions) {
    notify(message?.message || message, 'error', options)
  }

  return {
    notifications,
    addNotification,
    removeNotification,
    notify,
    success,
    info,
    warning,
    error,
  }
})

export default useNotify
