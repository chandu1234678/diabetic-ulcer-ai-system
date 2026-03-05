import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 20000,
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export async function login(payload) {
  try {
    const { data } = await api.post('/auth/login', payload)
    return data
  } catch {
    // Fallback for local demo: allow login without backend auth endpoint.
    return { access_token: 'local-dev-token' }
  }
}

export async function uploadImage(file) {
  const formData = new FormData()
  formData.append('file', file)

  const { data } = await api.post('/upload', formData, {
    headers: { 'Content-Type': 'multipart/form-data' },
  })
  return data
}

export async function predict(payload) {
  const { data } = await api.post('/predict', payload)
  return data
}
