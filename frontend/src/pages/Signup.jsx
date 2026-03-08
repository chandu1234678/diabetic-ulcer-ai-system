import { useMemo, useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { register } from '../services/api'
import HealthMetricsForm from '../components/HealthMetricsForm'

function getStrength(password) {
  if (password.length >= 12) return 4
  if (password.length >= 9) return 3
  if (password.length >= 6) return 2
  if (password.length >= 1) return 1
  return 0
}

export default function Signup({ onLogin }) {
  const navigate = useNavigate()
  const [fullName, setFullName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [age, setAge] = useState('')
  const [bmi, setBmi] = useState('')
  const [sugarBeforeFast, setSugarBeforeFast] = useState('')
  const [diabetesDuration, setDiabetesDuration] = useState('')
  const [acceptedTerms, setAcceptedTerms] = useState(false)
  const [showPassword, setShowPassword] = useState(false)
  const [showConfirmPassword, setShowConfirmPassword] = useState(false)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [submitSuccess, setSubmitSuccess] = useState(false)

  const strength = useMemo(() => getStrength(password), [password])

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError('')

    if (!fullName.trim()) {
      setError('Full name is required')
      return
    }

    if (!email.trim()) {
      setError('Email is required')
      return
    }

    if (!age) {
      setError('Age is required')
      return
    }

    if (!bmi) {
      setError('BMI is required')
      return
    }

    if (!sugarBeforeFast) {
      setError('Blood sugar level is required')
      return
    }

    if (password !== confirmPassword) {
      setError('Passwords do not match.')
      return
    }

    if (password.length < 8) {
      setError('Password must be at least 8 characters long')
      return
    }

    if (!acceptedTerms) {
      setError('Please accept Terms of Service and Privacy Policy.')
      return
    }

    setLoading(true)

    try {
      const data = await register({ email, password })
      localStorage.setItem('access_token', data.access_token || '')
      localStorage.setItem('patient_profile', JSON.stringify({
        full_name: fullName,
        email,
        age: parseInt(age),
        bmi: parseFloat(bmi),
        blood_sugar: parseInt(sugarBeforeFast),
        diabetes_duration: diabetesDuration,
      }))
      localStorage.setItem('user_data', JSON.stringify({
        full_name: fullName,
        email,
      }))
      setSubmitSuccess(true)
      setTimeout(() => {
        onLogin()
        navigate('/dashboard', { replace: true })
      }, 1500)
    } catch {
      setError('Unable to create account. This email may already be registered.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-background-light p-4">
      <div className="fixed inset-0 z-0 bg-gradient-to-br from-primary/10 via-background-light to-primary/5"></div>

      <div className="relative z-10 mx-auto w-full max-w-[520px]">
        <div className="overflow-hidden rounded-xl border border-primary/10 bg-white shadow-2xl">
          <div className="p-8">
            <div className="mb-8 flex flex-col items-center text-center">
              <div className="mb-4 flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
                <span className="material-symbols-outlined text-4xl text-primary">health_metrics</span>
              </div>
              <h1 className="text-3xl font-extrabold tracking-tight text-slate-900">Create Your Account</h1>
              <p className="mt-2 text-base text-slate-500">Join the AI Foot Ulcer Detection Platform</p>
            </div>

            <form onSubmit={handleSubmit} className="space-y-5">
              <div className="flex flex-col">
                <label className="mb-1.5 ml-1 text-sm font-semibold text-slate-700">Full Name</label>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-xl text-slate-400">person</span>
                  <input
                    type="text"
                    required
                    value={fullName}
                    onChange={(event) => setFullName(event.target.value)}
                    className="w-full rounded-lg border border-slate-200 bg-slate-50 py-3.5 pl-12 pr-4 text-slate-900 outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/50"
                    placeholder="John Doe"
                  />
                </div>
              </div>

              <div className="flex flex-col">
                <label className="mb-1.5 ml-1 text-sm font-semibold text-slate-700">Email Address</label>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-xl text-slate-400">mail</span>
                  <input
                    type="email"
                    required
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    className="w-full rounded-lg border border-slate-200 bg-slate-50 py-3.5 pl-12 pr-4 text-slate-900 outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/50"
                    placeholder="name@company.com"
                  />
                </div>
              </div>

              <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <div className="flex flex-col">
                  <label className="mb-1.5 ml-1 text-sm font-semibold text-slate-700">Password</label>
                  <div className="relative">
                    <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-xl text-slate-400">lock</span>
                    <input
                      type={showPassword ? 'text' : 'password'}
                      required
                      value={password}
                      onChange={(event) => setPassword(event.target.value)}
                      className="w-full rounded-lg border border-slate-200 bg-slate-50 py-3.5 pl-12 pr-10 text-slate-900 outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/50"
                      placeholder="••••••••"
                    />
                    <button
                      type="button"
                      onClick={() => setShowPassword((prev) => !prev)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-primary"
                    >
                      <span className="material-symbols-outlined text-xl">{showPassword ? 'visibility_off' : 'visibility'}</span>
                    </button>
                  </div>
                </div>

                <div className="flex flex-col">
                  <label className="mb-1.5 ml-1 text-sm font-semibold text-slate-700">Confirm Password</label>
                  <div className="relative">
                    <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-xl text-slate-400">shield</span>
                    <input
                      type={showConfirmPassword ? 'text' : 'password'}
                      required
                      value={confirmPassword}
                      onChange={(event) => setConfirmPassword(event.target.value)}
                      className="w-full rounded-lg border border-slate-200 bg-slate-50 py-3.5 pl-12 pr-10 text-slate-900 outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/50"
                      placeholder="••••••••"
                    />
                    <button
                      type="button"
                      onClick={() => setShowConfirmPassword((prev) => !prev)}
                      className="absolute right-3 top-1/2 -translate-y-1/2 text-slate-400 hover:text-primary"
                    >
                      <span className="material-symbols-outlined text-xl">{showConfirmPassword ? 'visibility_off' : 'visibility'}</span>
                    </button>
                  </div>
                </div>
              </div>

              <div className="px-1">
                <div className="mb-1.5 flex h-1.5 gap-1">
                  {[1, 2, 3, 4].map((bar) => (
                    <div
                      key={bar}
                      className={`flex-1 rounded-full ${strength >= bar ? 'bg-primary' : 'bg-slate-200'}`}
                    ></div>
                  ))}
                </div>
                <p className="text-[11px] font-medium text-slate-500">
                  Password Strength: <span className="text-primary">{strength >= 3 ? 'Medium-Strong' : 'Weak'}</span>
                </p>
              </div>

              {/* Health Metrics */}
              <div className="rounded-2xl bg-gradient-to-br from-primary/5 to-blue-50 border-2 border-primary/20 p-6 space-y-4">
                <div className="flex items-center gap-3 pb-3 border-b-2 border-primary/10">
                  <div className="p-2.5 rounded-lg bg-primary/10">
                    <span className="material-symbols-outlined text-lg text-primary">favorite</span>
                  </div>
                  <div>
                    <h3 className="text-sm font-bold text-slate-900">Health Metrics</h3>
                    <p className="text-xs text-slate-600">We&apos;ll use this for personalized risk assessment</p>
                  </div>
                </div>
                <HealthMetricsForm
                  age={age}
                  setAge={setAge}
                  bmi={bmi}
                  setBmi={setBmi}
                  sugarBeforeFast={sugarBeforeFast}
                  setSugarBeforeFast={setSugarBeforeFast}
                  compact={true}
                />
              </div>

              <div className="flex flex-col">
                <label className="mb-1.5 ml-1 text-sm font-semibold text-slate-700">
                  Diabetes Duration <span className="font-normal opacity-60">(Optional)</span>
                </label>
                <div className="relative">
                  <span className="material-symbols-outlined absolute left-4 top-1/2 -translate-y-1/2 text-xl text-slate-400">
                    calendar_month
                  </span>
                  <input
                    type="text"
                    value={diabetesDuration}
                    onChange={(event) => setDiabetesDuration(event.target.value)}
                    className="w-full rounded-lg border border-slate-200 bg-slate-50 px-12 py-3.5 text-slate-900 outline-none transition-all focus:border-primary focus:ring-2 focus:ring-primary/50"
                    placeholder="e.g. 5 years"
                  />
                </div>
              </div>

              <div className="flex items-start gap-3 py-2">
                <input
                  id="terms"
                  type="checkbox"
                  checked={acceptedTerms}
                  onChange={(event) => setAcceptedTerms(event.target.checked)}
                  className="mt-1 h-5 w-5 cursor-pointer rounded border-slate-300 text-primary focus:ring-primary/20"
                />
                <label htmlFor="terms" className="cursor-pointer text-sm leading-snug text-slate-600">
                  I agree to the <a className="font-medium text-primary hover:underline" href="#">Terms of Service</a> and{' '}
                  <a className="font-medium text-primary hover:underline" href="#">Privacy Policy</a> regarding medical data usage.
                </label>
              </div>

              {error && (
                <div className="flex items-start gap-3 rounded-lg bg-red-50 border border-red-200 p-4">
                  <span className="material-symbols-outlined text-red-600 flex-shrink-0">error</span>
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              )}

              {submitSuccess && (
                <div className="flex items-start gap-3 rounded-lg bg-green-50 border border-green-200 p-4">
                  <span className="material-symbols-outlined text-green-600 flex-shrink-0">check_circle</span>
                  <p className="text-sm text-green-700">Account created successfully! Redirecting to dashboard...</p>
                </div>
              )}

              <button
                type="submit"
                disabled={loading || submitSuccess}
                className="relative w-full rounded-lg bg-gradient-to-r from-primary to-[#2575c0] py-4 font-bold text-white shadow-lg shadow-primary/30 transition-all duration-300 hover:-translate-y-0.5 hover:shadow-primary/50 disabled:cursor-not-allowed disabled:opacity-70 disabled:hover:translate-y-0 flex items-center justify-center gap-2 overflow-hidden"
              >
                {loading && (
                  <div className="absolute inset-0 bg-gradient-to-r from-transparent via-white/20 to-transparent animate-shimmer"></div>
                )}
                <span className={submitSuccess ? 'invisible' : ''}>
                  {loading ? 'Creating Account...' : submitSuccess ? 'Account Created!' : 'Create Account'}
                </span>
                {submitSuccess && (
                  <span className="material-symbols-outlined absolute">check</span>
                )}
                {!loading && !submitSuccess && (
                  <span className="material-symbols-outlined text-lg">arrow_forward</span>
                )}
              </button>
            </form>

            <div className="mt-8 border-t border-slate-100 pt-6 text-center">
              <p className="text-sm text-slate-600">
                Already have an account?
                <button
                  type="button"
                  onClick={() => navigate('/login')}
                  className="ml-1 font-bold text-primary hover:underline"
                >
                  Log In
                </button>
              </p>
            </div>
          </div>

          <div className="flex items-center justify-center gap-2 bg-primary/5 px-8 py-4">
            <span className="material-symbols-outlined text-lg text-primary">verified_user</span>
            <p className="text-xs font-semibold uppercase tracking-wider text-primary/80">Your health information is securely protected.</p>
          </div>
        </div>

        <div className="mt-8 px-4 text-center">
          <div className="mb-4 flex justify-center gap-6 opacity-50 grayscale contrast-125">
            <div className="flex items-center gap-1.5 text-slate-600">
              <span className="material-symbols-outlined text-xl">encrypted</span>
              <span className="text-xs font-bold uppercase tracking-widest">HIPAA</span>
            </div>
            <div className="flex items-center gap-1.5 text-slate-600">
              <span className="material-symbols-outlined text-xl">gpp_good</span>
              <span className="text-xs font-bold uppercase tracking-widest">SSL 256-BIT</span>
            </div>
          </div>
          <p className="text-[11px] leading-relaxed text-slate-400">
            © 2024 AI Medical Foot Detection. All rights reserved. Professional healthcare diagnostics tool.
          </p>
        </div>
      </div>
    </div>
  )
}
