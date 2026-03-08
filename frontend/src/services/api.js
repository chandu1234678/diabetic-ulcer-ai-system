import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  timeout: 60000, // 60s for large file uploads
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

export async function uploadImage(file, retries = 3) {
  const formData = new FormData()
  formData.append('file', file)

  let lastError = null
  for (let attempt = 1; attempt <= retries; attempt++) {
    try {
      const { data } = await api.post('/upload', formData, {
        // Let axios handle Content-Type for FormData
        headers: {
          // Don't set Content-Type here - axios will set it with boundary
        },
        timeout: 60000,
      })
      return data
    } catch (error) {
      lastError = error
      console.warn(`Upload attempt ${attempt}/${retries} failed:`, error.message)
      
      // Don't retry on validation errors (400, 422)
      if (error.response?.status === 400 || error.response?.status === 422) {
        throw error
      }
      
      // Wait before retrying (exponential backoff)
      if (attempt < retries) {
        const delay = Math.pow(2, attempt - 1) * 1000 // 1s, 2s, 4s
        await new Promise(resolve => setTimeout(resolve, delay))
      }
    }
  }
  
  throw lastError
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

export async function getHealthMetricsAssessment(payload) {
  try {
    const { data } = await api.post('/health-metrics/assess', payload)
    return data
  } catch (error) {
    console.error('Health assessment error:', error)
    // Return mock assessment if API fails
    return {
      risk_score: 50,
      recommendations: ['Maintain regular physical activity', 'Monitor blood sugar levels'],
      details: {
        bmi_category: 'Normal',
        sugar_level: 'Normal',
        age_group: 'Adult',
      },
    }
  }
}
