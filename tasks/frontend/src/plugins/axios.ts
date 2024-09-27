import { AxiosError } from 'axios'
import axios_module from 'axios'
import { setupCache } from 'axios-cache-interceptor'
import { Router } from 'vue-router'

const axios = setupCache(axios_module.create({}), {
  ttl: 5000,
})

export default axios

export function registerAxios(router: Router) {
  axios.defaults.xsrfCookieName = 'csrftoken'
  axios.defaults.xsrfHeaderName = 'x-csrftoken'

  // Redirect to login page on 401 or 403
  axios.interceptors.response.use(undefined, (error: AxiosError<any, any>) => {
    if (error.response && (error.response.status == 401 || error.response?.status == 403)) {
      router.push('/login')
      return Promise.reject(null)
    }
    return Promise.reject(getResponseErrorMessage(error))
  })
}

export function getResponseErrorMessage(error: AxiosError<any, any>) {
  if (!error.response) {
    return error
  }
  if (!error.response.data) {
    return error.toJSON()
  }
  if (!error.response.data.detail) {
    return error.response.data
  }
  return error.response.data.detail
}
