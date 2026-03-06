import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { requestPasswordReset } from '../services/api'

export default function ForgotPassword() {
  const navigate = useNavigate()
  const [email, setEmail] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [success, setSuccess] = useState(false)
  const [resetLink, setResetLink] = useState('')
  const [devNote, setDevNote] = useState('')

  const handleSubmit = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    setResetLink('')
    setDevNote('')

    try {
      const response = await requestPasswordReset({ email })
      setSuccess(true)
      
      // If response contains reset link (development mode)
      if (response.reset_link) {
        setResetLink(response.reset_link)
        setDevNote(response.note || '')
      }
    } catch {
      setError('Unable to send reset email. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleCopyLink = () => {
    if (resetLink) {
      navigator.clipboard.writeText(resetLink)
      alert('Reset link copied to clipboard!')
    }
  }

  return (
    <div className="min-h-screen bg-background-light p-4">
      <main className="flex min-h-screen items-center justify-center bg-gradient-to-br from-primary/10 via-background-light to-primary/5">
        <div className="w-full max-w-md overflow-hidden rounded-xl border border-primary/10 bg-white shadow-xl shadow-primary/5">
          <div className="p-8 text-center">
            <div className="mb-6 inline-flex h-16 w-16 items-center justify-center rounded-full bg-primary/10">
              <span className="material-symbols-outlined text-4xl text-primary">lock_reset</span>
            </div>
            <h2 className="text-2xl font-bold tracking-tight text-slate-900">Forgot Password</h2>
            <p className="mt-2 text-slate-500">We will send you a reset link to your email address.</p>
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
                  placeholder="name@example.com"
                />
              </div>
            </div>

            {error && <p className="text-sm text-red-600">{error}</p>}

            {success && (
              <div className="space-y-4">
                <p className="text-sm text-green-700 font-medium">
                  ✓ If this email exists, a reset link has been sent. Check inbox and spam folder.
                </p>
                
                {resetLink && (
                  <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 space-y-3">
                    <p className="text-sm font-semibold text-blue-900">{devNote}</p>
                    <div className="bg-white p-3 rounded border border-blue-200 break-all">
                      <p className="text-xs text-slate-600 mb-2">Reset Link:</p>
                      <p className="text-xs font-mono text-blue-600">{resetLink}</p>
                    </div>
                    <button
                      type="button"
                      onClick={handleCopyLink}
                      className="w-full rounded-lg bg-blue-600 py-2 font-semibold text-white transition-all hover:bg-blue-700 text-sm"
                    >
                      Copy Link
                    </button>
                    <button
                      type="button"
                      onClick={() => navigate(`/reset-password?token=${resetLink.split('token=')[1]}`)}
                      className="w-full rounded-lg bg-green-600 py-2 font-semibold text-white transition-all hover:bg-green-700 text-sm"
                    >
                      Go to Reset Password
                    </button>
                  </div>
                )}
              </div>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full rounded-lg bg-primary py-4 font-bold text-white shadow-lg shadow-primary/20 transition-all hover:bg-primary/90 disabled:cursor-not-allowed disabled:opacity-70"
            >
              {loading ? 'Sending...' : 'Send Reset Link'}
            </button>

            <button
              type="button"
              onClick={() => navigate('/login')}
              className="w-full rounded-lg border border-slate-200 bg-white py-3.5 font-semibold text-slate-700 transition-colors hover:bg-slate-50"
            >
              Back to Login
            </button>
          </form>
        </div>
      </main>
    </div>
  )
}
