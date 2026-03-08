import { useNavigate } from 'react-router-dom'
import { useState } from 'react'

export default function DashboardHeader({ title, showBackButton = false, backTo = null, onLogout }) {
  const navigate = useNavigate()
  const [showProfileMenu, setShowProfileMenu] = useState(false)
  const patientProfile = JSON.parse(localStorage.getItem('patient_profile') || '{}')
  const userName = patientProfile.full_name || 'Patient'

  const handleLogout = () => {
    setShowProfileMenu(false)
    if (onLogout) {
      onLogout()
    }
    navigate('/login', { replace: true })
  }

  return (
    <>
      <header className="sticky top-0 z-40 w-full border-b border-slate-200 bg-white shadow-sm">
        <div className="flex h-16 items-center justify-between px-4 lg:px-8">
          <div className="flex items-center gap-4">
            {showBackButton && backTo && (
              <button
                onClick={() => navigate(backTo)}
                className="flex size-10 items-center justify-center rounded-lg hover:bg-slate-100 transition-colors text-slate-600"
                title="Go Back"
              >
                <span className="material-symbols-outlined">arrow_back</span>
              </button>
            )}
            <div className="flex items-center gap-4">
              <div className="flex size-10 items-center justify-center rounded-xl bg-primary text-white">
                <span className="material-symbols-outlined">health_metrics</span>
              </div>
              <div>
                <h1 className="text-xl font-bold tracking-tight text-slate-900">{title}</h1>
                {userName && userName !== 'Patient' && (
                  <p className="text-xs text-slate-500 font-medium mt-0.5">Welcome back, {userName.split(' ')[0]}</p>
                )}
              </div>
            </div>
          </div>
          <div className="flex items-center gap-2 lg:gap-4">
            <button
              onClick={() => navigate('/dashboard')}
              className="flex size-10 items-center justify-center rounded-full hover:bg-slate-100 transition-colors text-slate-600"
              title="Dashboard"
            >
              <span className="material-symbols-outlined">dashboard</span>
            </button>
            <button
              onClick={() => navigate('/history')}
              className="flex size-10 items-center justify-center rounded-full hover:bg-slate-100 transition-colors text-slate-600"
              title="View History"
            >
              <span className="material-symbols-outlined">history</span>
            </button>
            <button className="flex size-10 items-center justify-center rounded-full hover:bg-slate-100 transition-colors text-slate-600">
              <span className="material-symbols-outlined">notifications</span>
            </button>
            <div className="h-8 w-px bg-slate-200 hidden lg:block"></div>
            
            {/* Profile Popup */}
            <div className="relative">
              <button
                onClick={() => setShowProfileMenu(!showProfileMenu)}
                className="flex items-center gap-3 px-2 lg:px-3 py-1.5 rounded-full hover:bg-slate-100 transition-colors"
              >
                <div className="text-right hidden sm:block">
                  <p className="text-sm font-semibold text-slate-900">{userName}</p>
                  <p className="text-xs text-slate-500">Premium Member</p>
                </div>
                <div className="size-10 rounded-full border-2 border-primary/20 overflow-hidden flex-shrink-0">
                  <img
                    className="h-full w-full object-cover"
                    alt="User profile avatar"
                    src="https://lh3.googleusercontent.com/aida-public/AB6AXuDgKFZ3-0WTUhN7tWkpJxVUxE3Bv8oIKMLrHqq30LW_R1rbpXUI8QFBeI1pHpJbeGwnbT0Gue3XNusn-dFKRq3VDRU9VW_OO87v6PJZ5uE-SxnhujWj6g3-pttFOUt9WhkLCV14lzJX0r25oFF-K2NjHcO4tCInRzCEUfJ-iGVG5UsurmaSyFl1mx47tvyy205CFHyy4chetFNBM746uuSo80k76MRH5Jpjrgyz9zZiWR3qvyZvIZf9WBGkeeSKEcq5jJZ1tGlS3D0"
                  />
                </div>
              </button>

              {/* Profile Dropdown Menu */}
              {showProfileMenu && (
                <div className="absolute right-0 mt-2 w-56 bg-white rounded-xl border border-slate-200 shadow-lg z-50">
                  {/* Header */}
                  <div className="px-4 py-3 border-b border-slate-200 bg-gradient-to-r from-primary/10 to-blue-500/10">
                    <p className="text-sm font-semibold text-slate-900">{userName}</p>
                    <p className="text-xs text-slate-600 mt-1">{patientProfile.email || 'patient@email.com'}</p>
                  </div>

                  {/* Menu Items */}
                  <div className="p-2">
                    <button
                      onClick={() => {
                        navigate('/account-settings')
                        setShowProfileMenu(false)
                      }}
                      className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-700 hover:bg-slate-100 transition-colors text-left text-sm font-medium"
                    >
                      <span className="material-symbols-outlined text-lg">person</span>
                      Profile Settings
                    </button>
                    <button
                      onClick={() => {
                        navigate('/dashboard')
                        setShowProfileMenu(false)
                      }}
                      className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-700 hover:bg-slate-100 transition-colors text-left text-sm font-medium"
                    >
                      <span className="material-symbols-outlined text-lg">dashboard</span>
                      Dashboard
                    </button>
                    <button
                      onClick={() => {
                        navigate('/history')
                        setShowProfileMenu(false)
                      }}
                      className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-700 hover:bg-slate-100 transition-colors text-left text-sm font-medium"
                    >
                      <span className="material-symbols-outlined text-lg">history</span>
                      Scan History
                    </button>
                    <button className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-slate-700 hover:bg-slate-100 transition-colors text-left text-sm font-medium">
                      <span className="material-symbols-outlined text-lg">settings</span>
                      Settings
                    </button>

                    <div className="my-2 h-px bg-slate-200"></div>

                    <button
                      onClick={handleLogout}
                      className="w-full flex items-center gap-3 px-3 py-2.5 rounded-lg text-red-600 hover:bg-red-50 transition-colors text-left text-sm font-medium"
                    >
                      <span className="material-symbols-outlined text-lg">logout</span>
                      Logout
                    </button>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Click outside to close menu */}
      {showProfileMenu && (
        <div
          className="fixed inset-0 z-30"
          onClick={() => setShowProfileMenu(false)}
        ></div>
      )}
    </>
  )
}
