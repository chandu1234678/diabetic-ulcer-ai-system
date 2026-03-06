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
  const { data } = await api.post('/auth/login', payload)
  return data
}

export async function register(payload) {
  const { data } = await api.post('/auth/register', payload)
  return data
}

export async function uploadImage(file) {
  const formData = new FormData()
  formData.append('file', file)

  const { data } = await api.post('/upload', formData)
  return data
}

export async function predict(payload) {
  const { data } = await api.post('/predict', payload)
  return data
}

export async function getCurrentUser() {
  try {
    const { data } = await api.get('/auth/me')
    return data
  } catch {
    // Return stored user data if API fails
    const storedUser = localStorage.getItem('user_data')
    return storedUser ? JSON.parse(storedUser) : null
  }
}

export async function requestPasswordReset(payload) {
  const { data } = await api.post('/auth/forgot-password', payload)
  return data
}

export async function resetPassword(payload) {
  const { data } = await api.post('/auth/reset-password', payload)
  return data
}

export function logout() {
  localStorage.removeItem('access_token')
  localStorage.removeItem('user_data')
  localStorage.removeItem('patient_profile')
}
