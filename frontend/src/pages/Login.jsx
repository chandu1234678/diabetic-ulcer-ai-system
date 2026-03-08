import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { login } from '../services/api'

export default function Login({ onLogin }) {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [rememberMe, setRememberMe] = useState(false)
  const [showPassword, setShowPassword] = useState(false)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')

    try {
      const data = await login({ email, password })
      localStorage.setItem('access_token', data.access_token || 'local-dev-token')
      
      // Store user data
      if (data.user) {
        localStorage.setItem('user_data', JSON.stringify(data.user))
      }
      
      if (rememberMe) {
        localStorage.setItem('remember_email', email)
      } else {
        localStorage.removeItem('remember_email')
      }
      onLogin()
      navigate('/chatbot', { replace: true })
    } catch {
      setError('Unable to sign in. Please check your credentials.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background-light font-display text-slate-900 flex flex-col">
      <main className="flex-grow flex items-center justify-center bg-gradient-to-br from-primary/10 via-background-light to-primary/5 p-4">
        <div className="w-full max-w-md overflow-hidden rounded-xl border border-primary/10 bg-white shadow-xl shadow-primary/5">
          <div className="p-8 text-center">
            <div className="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
              <span className="material-symbols-outlined text-4xl text-primary">medical_services</span>
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-slate-900">Welcome Back</h2>
            <p className="mt-2 text-slate-500">Sign in to your account to continue</p>
          </div>

          <form onSubmit={handleSubmit} className="space-y-5 px-8 pb-8 pt-2">
            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">Email Address</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-xl text-slate-400">mail</span>
                <input
                  type="email"
                  required
                  value={email}
                  onChange={(event) => setEmail(event.target.value)}
                  className="w-full rounded-lg border border-slate-200 bg-background-light py-3.5 pl-12 pr-4 text-slate-900 outline-none transition-all placeholder:text-slate-400 focus:border-primary focus:ring-2 focus:ring-primary/50"
                  placeholder="maihame@example.com"
                />
              </div>
            </div>

            <div>
              <label className="mb-2 block text-sm font-semibold text-slate-700">Password</label>
              <div className="relative">
                <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-xl text-slate-400">lock</span>
                <input
                  type={showPassword ? 'text' : 'password'}
                  required
                  value={password}
                  onChange={(event) => setPassword(event.target.value)}
                  className="w-full rounded-lg border border-slate-200 bg-background-light py-3.5 pl-12 pr-12 text-slate-900 outline-none transition-all placeholder:text-slate-400 focus:border-primary focus:ring-2 focus:ring-primary/50"
                  placeholder="••••••••"
                />
                <button
                  type="button"
                  onClick={() => setShowPassword((prev) => !prev)}
                  className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-400 transition-colors hover:text-primary"
                >
                  <span className="material-symbols-outlined text-xl">visibility</span>
                </button>
              </div>
            </div>

            <div className="flex items-center justify-between">
              <label className="group flex cursor-pointer items-center gap-2">
                <input
                  type="checkbox"
                  checked={rememberMe}
                  onChange={(event) => setRememberMe(event.target.checked)}
                  className="h-4 w-4 rounded border-slate-300 text-primary focus:ring-primary"
                />
                <span className="text-sm text-slate-600 transition-colors group-hover:text-slate-900">Remember me</span>
              </label>
              <button
                type="button"
                onClick={() => navigate('/forgot-password')}
                className="text-sm font-medium text-primary transition-colors hover:text-primary/80"
              >
                Forgot password?
              </button>
            </div>

            {error && (
              <div className="flex items-start gap-3 rounded-lg bg-red-50 border border-red-200 p-3">
                <span className="material-symbols-outlined text-red-600 flex-shrink-0">error</span>
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="relative mt-2 flex w-full items-center justify-center gap-2 rounded-lg bg-gradient-to-r from-primary to-[#2575c0] py-4 font-bold text-white shadow-lg shadow-primary/20 transition-all hover:-translate-y-0.5 hover:shadow-primary/40 disabled:cursor-not-allowed disabled:opacity-70 active:scale-95 overflow-hidden"
            >
              {loading && (
                <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-pulse"></div>
              )}
              <span className="relative flex items-center gap-2">
                {loading ? 'Signing In...' : 'Sign In'}
                {!loading && <span className="material-symbols-outlined text-xl">arrow_forward</span>}
              </span>
            </button>

            <div className="relative flex items-center py-4">
              <div className="flex-grow border-t border-slate-200"></div>
              <span className="mx-4 flex-shrink text-xs font-medium uppercase tracking-widest text-slate-400">New User?</span>
              <div className="flex-grow border-t border-slate-200"></div>
            </div>

            <button
              type="button"
              onClick={() => navigate('/signup')}
              className="w-full rounded-lg border border-slate-200 bg-white py-3.5 font-semibold text-slate-700 transition-all hover:bg-slate-50 hover:border-primary hover:text-primary active:scale-95"
            >
              Create an account
            </button>
          </form>

          <div className="border-t border-slate-100 bg-slate-50 px-8 py-6 text-center">
            <p className="flex items-center justify-center gap-1 text-xs text-slate-500">
              <span className="material-symbols-outlined text-sm">verified_user</span>
              Secure, encrypted medical environment
            </p>
          </div>
        </div>
      </main>

      <footer className="px-4 py-8 text-center">
        <div className="mx-auto max-w-4xl">
          <p className="mb-4 text-sm font-medium text-slate-600">
            Medical AI Assistant | AI-powered foot ulcer detection platform
          </p>
          <div className="flex flex-wrap justify-center gap-x-6 gap-y-2 text-xs text-slate-400">
            <a className="underline decoration-primary/30 underline-offset-4 transition-colors hover:text-primary" href="#">Privacy Policy</a>
            <a className="underline decoration-primary/30 underline-offset-4 transition-colors hover:text-primary" href="#">Terms of Service</a>
            <a className="underline decoration-primary/30 underline-offset-4 transition-colors hover:text-primary" href="#">Support</a>
            <a className="underline decoration-primary/30 underline-offset-4 transition-colors hover:text-primary" href="#">Cookie Settings</a>
          </div>
          <p className="mt-6 text-[10px] uppercase tracking-tighter text-slate-400">
            © 2024 AI Foot Ulcer Detection. All Rights Reserved.
          </p>
        </div>
      </footer>
    </div>
  )
}
