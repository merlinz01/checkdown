import axios, { AxiosError } from 'axios'
import { Router } from 'vue-router'

export function registerAxios(router: Router) {
  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'x-csrftoken'

  // Redirect to login page on 401 or 403
  axios.interceptors.response.use(undefined, (error: AxiosError<any, any>) => {
    if (
      error.response &&
      (error.response.status == 401 || error.response?.status == 403) &&
      error.response.config.url?.indexOf('login') === -1
    ) {
      router.push('/login')
      return Promise.reject(null)
    }
    if (!error.response) {
      return Promise.reject(error)
    }
    if (!error.response.data) {
      return Promise.reject(error.toJSON())
    }
    if (!error.response.data.detail) {
      return Promise.reject(error.response.data)
    }
    return Promise.reject(error.response.data.detail)
  })
}
