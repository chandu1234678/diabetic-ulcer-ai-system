import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { applyDarkMode, toggleDarkMode } from '../utils/darkMode'
import { logout } from '../services/api'

export default function AccountSettings({ onLogout }) {
  const navigate = useNavigate()
  const [darkMode, setDarkMode] = useState(false)
  const [emailNotif, setEmailNotif] = useState(true)
  const [smsNotif, setSmsNotif] = useState(false)
  const [marketingNotif, setMarketingNotif] = useState(false)
  const [twoFactorEnabled, setTwoFactorEnabled] = useState(true)
  
  // Get user data from localStorage
  const storedUser = JSON.parse(localStorage.getItem('user_data') || '{}')
  const [fullName, setFullName] = useState(storedUser.full_name || 'User')
  const [email, setEmail] = useState(storedUser.email || 'user@example.com')
  const [role] = useState(storedUser.role || 'Patient')
  const [memberSince] = useState(storedUser.member_since || 'May 2023')
  const [showDropdown, setShowDropdown] = useState(false)
  const [showPasswordModal, setShowPasswordModal] = useState(false)
  const [currentPassword, setCurrentPassword] = useState('')
  const [newPassword, setNewPassword] = useState('')
  const [confirmPassword, setConfirmPassword] = useState('')
  const [passwordError, setPasswordError] = useState('')
  const [passwordSuccess, setPasswordSuccess] = useState('')
  const [saveSuccess, setSaveSuccess] = useState('')
  const [saveError, setSaveError] = useState('')
  const [isSaving, setIsSaving] = useState(false)
  const [passwordLoading, setPasswordLoading] = useState(false)
  
  // Health Metrics States
  const [age, setAge] = useState('')
  const [bmi, setBmi] = useState('')
  const [bloodSugar, setBloodSugar] = useState('')
  const [diabetesDuration, setDiabetesDuration] = useState('')
  const [metricsError, setMetricsError] = useState('')
  const [metricsSuccess, setMetricsSuccess] = useState('')
  const [metricsLoading, setMetricsLoading] = useState(false)

  const userName = fullName

  // Apply dark mode on mount
  useEffect(() => {
    applyDarkMode()
    const isDark = localStorage.getItem('darkMode') === 'true'
    setDarkMode(isDark)
    
    // Load health metrics defaults from localStorage
    const savedMetrics = JSON.parse(localStorage.getItem('health_metrics_defaults') || '{}')
    if (savedMetrics.age) setAge(savedMetrics.age)
    if (savedMetrics.bmi) setBmi(savedMetrics.bmi)
    if (savedMetrics.blood_sugar) setBloodSugar(savedMetrics.blood_sugar)
    if (savedMetrics.diabetes_duration) setDiabetesDuration(savedMetrics.diabetes_duration)
  }, [])

  const handleChangePassword = async () => {
    setPasswordError('')
    setPasswordSuccess('')

    if (!currentPassword || !newPassword || !confirmPassword) {
      setPasswordError('All fields are required')
      return
    }

    if (newPassword.length < 8) {
      setPasswordError('New password must be at least 8 characters')
      return
    }

    if (newPassword !== confirmPassword) {
      setPasswordError('Passwords do not match')
      return
    }

    setPasswordLoading(true)

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1500))
      setPasswordSuccess('Password changed successfully!')
      setTimeout(() => {
        setCurrentPassword('')
        setNewPassword('')
        setConfirmPassword('')
        setShowPasswordModal(false)
        setPasswordSuccess('')
        setPasswordLoading(false)
      }, 2000)
    } catch (err) {
      setPasswordError('Failed to change password. Please try again.')
      setPasswordLoading(false)
    }
  }

  const handleSaveChanges = async () => {
    setSaveError('')
    setSaveSuccess('')

    if (!fullName.trim()) {
      setSaveError('Full name is required')
      return
    }

    if (!email.trim()) {
      setSaveError('Email is required')
      return
    }

    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
    if (!emailRegex.test(email)) {
      setSaveError('Please enter a valid email address')
      return
    }

    setIsSaving(true)

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1500))
      
      // Update local storage
      const userData = JSON.parse(localStorage.getItem('user_data') || '{}')
      userData.full_name = fullName
      userData.email = email
      localStorage.setItem('user_data', JSON.stringify(userData))
      
      setSaveSuccess('Settings saved successfully!')
      setTimeout(() => {
        setSaveSuccess('')
        setIsSaving(false)
      }, 2000)
    } catch (err) {
      setSaveError('Failed to save settings. Please try again.')
      setIsSaving(false)
    }
  }

  const handleLogout = () => {
    if (onLogout) {
      onLogout()
    }
    navigate('/login', { replace: true })
  }

  const handleSaveMetrics = async () => {
    setMetricsError('')
    setMetricsSuccess('')

    // Validation
    if (!age || !bmi || !bloodSugar) {
      setMetricsError('Please fill in all health metrics fields')
      return
    }

    const ageNum = parseFloat(age)
    const bmiNum = parseFloat(bmi)
    const bloodSugarNum = parseFloat(bloodSugar)
    const durationNum = diabetesDuration ? parseFloat(diabetesDuration) : null

    if (ageNum < 1 || ageNum > 150) {
      setMetricsError('Age must be between 1 and 150')
      return
    }

    if (bmiNum < 10 || bmiNum > 60) {
      setMetricsError('BMI must be between 10 and 60')
      return
    }

    if (bloodSugarNum < 70 || bloodSugarNum > 400) {
      setMetricsError('Blood Sugar must be between 70 and 400 mg/dL')
      return
    }

    setMetricsLoading(true)

    try {
      // Simulate API call
      await new Promise((resolve) => setTimeout(resolve, 1000))
      
      // Save to localStorage
      const metricsData = {
        age: ageNum,
        bmi: bmiNum,
        blood_sugar: bloodSugarNum,
        diabetes_duration: durationNum,
        saved_at: new Date().toISOString()
      }
      localStorage.setItem('health_metrics_defaults', JSON.stringify(metricsData))
      
      setMetricsSuccess('Health metrics saved successfully!')
      setTimeout(() => {
        setMetricsSuccess('')
        setMetricsLoading(false)
      }, 2000)
    } catch (err) {
      setMetricsError('Failed to save health metrics. Please try again.')
      setMetricsLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-light font-display">
      {/* Top Nav */}
      <nav className="sticky top-0 z-50 bg-light border-b border-slate-200 px-4 md:px-8 h-16 flex items-center justify-between">
        <button 
          onClick={() => navigate('/dashboard')} 
          className="flex items-center gap-2 hover:opacity-80 transition-opacity"
        >
          <div className="bg-primary p-2 rounded-lg">
            <span className="material-symbols-outlined text-white">health_metrics</span>
          </div>
          <span className="font-bold text-xl tracking-tight text-slate-900">MedVision AI</span>
        </button>
        <div className="flex items-center gap-4">
          <button className="p-2 hover:bg-slate-200 rounded-full transition-colors text-slate-600">
            <span className="material-symbols-outlined">notifications</span>
          </button>
          <div className="relative">
            <button
              onClick={() => setShowDropdown(!showDropdown)}
              className="flex items-center gap-2 p-1 pr-3 hover:bg-slate-200 rounded-full transition-colors"
            >
              <div
                className="size-8 rounded-full bg-cover bg-center"
                style={{
                  backgroundImage: `url('https://lh3.googleusercontent.com/aida-public/AB6AXuDYtqx3cn4LBM0J1hwrfuVJ6da9gEyciZna679_yWpCQyRMelVv7fAv5Dzm92U2ms7_0_GBYtCECF1Edwn_MKQAerEe6O-qTYqXTMq-sf1bw8cEUsbsCjVegDetNqFm_wH1CqMk_-ippA3eHIe0wEx0TvDaILzq-YkpoCnFIeapsWZdpzfy-pQSZtaGfZ0HfRh-h5Bz7-fencldhHTYYhuDHhDSsxlTbLKxmM9Q23i40TnyJ6IfCSDJ3n9tE_P8X-tiJMgnEZP5oFY')`
                }}
              ></div>
              <span className="text-sm font-semibold hidden md:block text-slate-900">{userName}</span>
              <span className="material-symbols-outlined text-sm text-slate-600">expand_more</span>
            </button>
            {/* Dropdown */}
            {showDropdown && (
              <div className="absolute right-0 mt-2 w-48 bg-white border border-slate-200 rounded-xl shadow-xl py-2 z-50">
                <button className="w-full flex items-center gap-3 px-4 py-2 hover:bg-slate-100 transition-colors text-left">
                  <span className="material-symbols-outlined text-lg text-slate-600">person</span>
                  <span className="text-sm text-slate-900">Profile</span>
                </button>
                <button
                  onClick={() => {
                    setShowDropdown(false)
                    navigate('/account-settings')
                  }}
                  className="w-full flex items-center gap-3 px-4 py-2 hover:bg-slate-100 transition-colors text-primary text-left"
                >
                  <span className="material-symbols-outlined text-lg">settings</span>
                  <span className="text-sm font-bold">Settings</span>
                </button>
                <hr className="my-1 border-slate-200" />
                <button
                  onClick={handleLogout}
                  className="w-full flex items-center gap-3 px-4 py-2 hover:bg-slate-100 transition-colors text-red-500 text-left"
                >
                  <span className="material-symbols-outlined text-lg">logout</span>
                  <span className="text-sm">Logout</span>
                </button>
              </div>
            )}
          </div>
        </div>
      </nav>

      <main className="max-w-4xl mx-auto p-4 md:p-8">
        {/* Settings Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-extrabold mb-2 text-slate-900">Account Settings</h1>
          <p className="text-slate-500">Manage your profile, security, and notification preferences.</p>
        </div>

        {/* Profile Section */}
        <section className="bg-white rounded-xl border border-slate-200 overflow-hidden mb-6">
          <div className="p-6 border-b border-slate-100">
            <h2 className="text-lg font-bold text-slate-900">Profile Information</h2>
          </div>
          <div className="p-6 flex flex-col md:flex-row gap-6 items-center md:items-start">
            <div className="relative">
              <div
                className="size-24 rounded-full bg-cover bg-center border-4 border-primary/20"
                style={{
                  backgroundImage: `url('https://lh3.googleusercontent.com/aida-public/AB6AXuDlQtA2HqSgjMXfj9VgVzmhQj9oH0oUKQa4QI6Cntvxs0IAtXW10_PRQtJkZcSYcEDMx9kfzEAgZmWlT_xI0Bp6dGhSao--FLjbYDQfk1T2DwWDGP-iJxHZVwTrFHaFguIUvNEhVwRv5n8aXYyBLsxtQEXGwnc1NgN9GxxAWLJkvgPtWDQbSsPU5QHuy8asHBFcy_XWVYp25WY2pdHb2Hcq26m_xH94A9bky_ZqMwTZ_zRJcqSmBTMn2SvMAp_nQqOSCXeU7IKy43w')`
                }}
              ></div>
                <button className="absolute bottom-0 right-0 bg-primary text-white p-1.5 rounded-full border-2 border-white hover:bg-primary/90 transition-colors">
                <span className="material-symbols-outlined text-sm">edit</span>
              </button>
            </div>
            <div className="flex-1 w-full grid md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-slate-500 mb-1">Full Name</label>
                <input
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent text-slate-900"
                  type="text"
                  value={fullName}
                  onChange={(e) => setFullName(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-500 mb-1">Email Address</label>
                <input
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent text-slate-900"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-500 mb-1">Role</label>
                <p className="px-4 py-2 bg-slate-100 rounded-lg text-slate-600">Patient</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-500 mb-1">Member Since</label>
                <p className="px-4 py-2 bg-slate-100 rounded-lg text-slate-600">May 2023</p>
              </div>
            </div>
          </div>
        </section>

        {/* Security & Dark Mode */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <section className="bg-white rounded-xl border border-slate-200 p-6">
            <div className="flex items-center gap-3 mb-6">
              <span className="material-symbols-outlined text-primary">security</span>
              <h2 className="text-lg font-bold text-slate-900">Security</h2>
            </div>
            <button
              onClick={() => setShowPasswordModal(true)}
              className="w-full flex items-center justify-between p-4 bg-slate-50 hover:bg-primary/10 transition-colors rounded-lg mb-4 group"
            >
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-slate-400">lock</span>
                <span className="font-medium text-slate-900">Change Password</span>
              </div>
              <span className="material-symbols-outlined text-slate-400 group-hover:text-primary">chevron_right</span>
            </button>
            <button
              onClick={() => setTwoFactorEnabled(!twoFactorEnabled)}
              className="w-full flex items-center justify-between p-4 bg-slate-50 hover:bg-primary/10 transition-colors rounded-lg group"
            >
              <div className="flex items-center gap-3">
                <span className="material-symbols-outlined text-slate-400">fingerprint</span>
                <span className="font-medium text-slate-900">Two-Factor Auth</span>
              </div>
              <span className={`px-2 py-0.5 text-xs font-bold rounded uppercase ${
                twoFactorEnabled 
                  ? 'bg-green-100 text-green-700' 
                  : 'bg-slate-200 text-slate-600'
              }`}>
                {twoFactorEnabled ? 'On' : 'Off'}
              </span>
            </button>
          </section>
          <section className="bg-white rounded-xl border border-slate-200 p-6">
            <div className="flex items-center gap-3 mb-6">
              <span className="material-symbols-outlined text-primary">palette</span>
              <h2 className="text-lg font-bold text-slate-900">Appearance</h2>
            </div>
            <p className="text-slate-600">Light theme is always enabled for optimal visibility.</p>
          </section>
        </div>

        {/* Notification Preferences */}
        <section className="bg-white rounded-xl border border-slate-200 overflow-hidden mb-12">
          <div className="p-6 border-b border-slate-100">
            <div className="flex items-center gap-3">
              <span className="material-symbols-outlined text-primary">notifications_active</span>
              <h2 className="text-lg font-bold text-slate-900">Notification Preferences</h2>
            </div>
          </div>
          <div className="p-6 space-y-4">
            <div className="flex items-center justify-between">
              <div>
                <p className="font-bold text-slate-900">Email Notifications</p>
                <p className="text-sm text-slate-500">Receive appointment reminders and lab results via email.</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={emailNotif}
                  onChange={(e) => setEmailNotif(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
            <hr className="border-slate-100" />
            <div className="flex items-center justify-between">
              <div>
                <p className="font-bold text-slate-900">SMS Notifications</p>
                <p className="text-sm text-slate-500">Receive urgent updates and login codes via text.</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={smsNotif}
                  onChange={(e) => setSmsNotif(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
            <hr className="border-slate-100" />
            <div className="flex items-center justify-between">
              <div>
                <p className="font-bold text-slate-900">Marketing & Offers</p>
                <p className="text-sm text-slate-500">Receive updates on new healthcare services and health tips.</p>
              </div>
              <label className="relative inline-flex items-center cursor-pointer">
                <input
                  type="checkbox"
                  checked={marketingNotif}
                  onChange={(e) => setMarketingNotif(e.target.checked)}
                  className="sr-only peer"
                />
                <div className="w-11 h-6 bg-slate-200 peer-focus:outline-none rounded-full peer peer-checked:after:translate-x-full peer-checked:after:border-white after:content-[''] after:absolute after:top-[2px] after:left-[2px] after:bg-white after:border-gray-300 after:border after:rounded-full after:h-5 after:w-5 after:transition-all peer-checked:bg-primary"></div>
              </label>
            </div>
          </div>
        </section>

        {/* Health Metrics Defaults */}
        <section className="bg-white rounded-xl border border-slate-200 overflow-hidden mb-12">
          <div className="p-6 border-b border-slate-100">
            <div className="flex items-center gap-3 mb-2">
              <span className="material-symbols-outlined text-primary">favorite</span>
              <h2 className="text-lg font-bold text-slate-900">Health Metrics Defaults</h2>
            </div>
            <p className="text-sm text-slate-500 ml-10">Set default values that will auto-fill when uploading foot scan images.</p>
          </div>
          <div className="p-6">
            {metricsError && (
              <div className="flex items-start gap-3 rounded-lg bg-red-50 border border-red-200 p-4 mb-4">
                <span className="material-symbols-outlined text-red-600 flex-shrink-0">error</span>
                <p className="text-sm text-red-700">{metricsError}</p>
              </div>
            )}

            {metricsSuccess && (
              <div className="flex items-start gap-3 rounded-lg bg-green-50 border border-green-200 p-4 mb-4">
                <span className="material-symbols-outlined text-green-600 flex-shrink-0">check_circle</span>
                <p className="text-sm text-green-700">{metricsSuccess}</p>
              </div>
            )}

            <div className="grid md:grid-cols-2 gap-4 mb-6">
              <div>
                <label className="block text-sm font-medium text-slate-500 mb-2">Age <span className="text-red-500">*</span></label>
                <input
                  type="number"
                  min="1"
                  max="150"
                  value={age}
                  onChange={(e) => setAge(e.target.value)}
                  placeholder="e.g., 45"
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent text-slate-900 placeholder-slate-400"
                />
                <p className="text-xs text-slate-400 mt-1">Range: 1-150 years</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-500 mb-2">BMI <span className="text-red-500">*</span></label>
                <input
                  type="number"
                  min="10"
                  max="60"
                  step="0.1"
                  value={bmi}
                  onChange={(e) => setBmi(e.target.value)}
                  placeholder="e.g., 28.5"
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent text-slate-900 placeholder-slate-400"
                />
                <p className="text-xs text-slate-400 mt-1">Range: 10-60 kg/m²</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-500 mb-2">Fasting Blood Sugar <span className="text-red-500">*</span></label>
                <input
                  type="number"
                  min="70"
                  max="400"
                  value={bloodSugar}
                  onChange={(e) => setBloodSugar(e.target.value)}
                  placeholder="e.g., 140"
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent text-slate-900 placeholder-slate-400"
                />
                <p className="text-xs text-slate-400 mt-1">Range: 70-400 mg/dL</p>
              </div>
              <div>
                <label className="block text-sm font-medium text-slate-500 mb-2">Diabetes Duration <span className="text-slate-400">(optional)</span></label>
                <input
                  type="number"
                  min="0"
                  max="100"
                  value={diabetesDuration}
                  onChange={(e) => setDiabetesDuration(e.target.value)}
                  placeholder="e.g., 5"
                  className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent text-slate-900 placeholder-slate-400"
                />
                <p className="text-xs text-slate-400 mt-1">Years since diagnosis</p>
              </div>
            </div>

            <button
              onClick={handleSaveMetrics}
              disabled={metricsLoading}
              className="w-full px-6 py-3 rounded-lg bg-gradient-to-r from-primary to-[#2575c0] text-white font-semibold hover:shadow-lg hover:shadow-primary/30 hover:-translate-y-0.5 transition-all active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2 relative overflow-hidden"
            >
              {metricsLoading && (
                <span className="animate-spin material-symbols-outlined text-lg">hourglass_bottom</span>
              )}
              <span>{metricsLoading ? 'Saving Metrics...' : 'Save Health Metrics'}</span>
            </button>
          </div>
        </section>

        {/* Save Changes */}
        <div className="space-y-4 mb-8">
          {saveError && (
            <div className="flex items-start gap-3 rounded-lg bg-red-50 border border-red-200 p-4">
              <span className="material-symbols-outlined text-red-600 flex-shrink-0">error</span>
              <p className="text-sm text-red-700">{saveError}</p>
            </div>
          )}

          {saveSuccess && (
            <div className="flex items-start gap-3 rounded-lg bg-green-50 border border-green-200 p-4">
              <span className="material-symbols-outlined text-green-600 flex-shrink-0">check_circle</span>
              <p className="text-sm text-green-700">{saveSuccess}</p>
            </div>
          )}

          <div className="flex justify-end gap-4">
            <button
              onClick={handleCancel}
              disabled={isSaving}
              className="px-6 py-2.5 rounded-lg border border-slate-300 font-semibold text-slate-900 hover:bg-slate-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button
              onClick={handleSaveChanges}
              disabled={isSaving}
              className="px-6 py-2.5 rounded-lg bg-gradient-to-r from-primary to-[#2575c0] text-white font-semibold hover:shadow-lg hover:shadow-primary/30 hover:-translate-y-0.5 transition-all active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed flex items-center gap-2 relative overflow-hidden"
            >
              {isSaving && (
                <span className="animate-spin material-symbols-outlined text-lg">hourglass_bottom</span>
              )}
              <span>{isSaving ? 'Saving...' : saveSuccess ? 'Saved!' : 'Save Changes'}</span>
            </button>
          </div>
        </div>

        {/* Change Password Modal */}
        {showPasswordModal && (
          <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
            <div className="bg-white rounded-xl border border-slate-200 max-w-md w-full p-6 shadow-2xl">
              <div className="flex items-center justify-between mb-4">
                <h2 className="text-xl font-bold text-slate-900 flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">lock</span>
                  Change Password
                </h2>
                <button
                  onClick={() => {
                    setShowPasswordModal(false)
                    setPasswordError('')
                    setPasswordSuccess('')
                  }}
                  className="text-slate-600 hover:text-slate-900"
                >
                  <span className="material-symbols-outlined">close</span>
                </button>
              </div>

              {passwordError && (
                <div className="mb-4 p-3 bg-red-100 text-red-700 rounded-lg text-sm">
                  {passwordError}
                </div>
              )}

              {passwordSuccess && (
                <div className="mb-4 p-3 bg-green-100 text-green-700 rounded-lg text-sm flex items-center gap-2">
                  <span className="material-symbols-outlined text-sm">check_circle</span>
                  {passwordSuccess}
                </div>
              )}

              <div className="space-y-4 mb-6">
                <div>
                  <label className="block text-sm font-medium text-slate-500 mb-1">Current Password</label>
                  <input
                    type="password"
                    value={currentPassword}
                    onChange={(e) => setCurrentPassword(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent text-slate-900"
                    placeholder="Enter current password"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-500 mb-1">New Password</label>
                  <input
                    type="password"
                    value={newPassword}
                    onChange={(e) => setNewPassword(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent text-slate-900"
                    placeholder="Enter new password (min 8 characters)"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-slate-500 mb-1">Confirm Password</label>
                  <input
                    type="password"
                    value={confirmPassword}
                    onChange={(e) => setConfirmPassword(e.target.value)}
                    className="w-full bg-slate-50 border border-slate-200 rounded-lg px-4 py-2 focus:ring-2 focus:ring-primary focus:border-transparent text-slate-900"
                    placeholder="Confirm new password"
                  />
                </div>
              </div>

              <div className="flex gap-3">
                <button
                  onClick={() => {
                    setShowPasswordModal(false)
                    setCurrentPassword('')
                    setNewPassword('')
                    setConfirmPassword('')
                    setPasswordError('')
                  }}
                  disabled={passwordLoading}
                  className="flex-1 px-4 py-2 rounded-lg border border-slate-300 font-semibold text-slate-900 hover:bg-slate-100 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                >
                  Cancel
                </button>
                <button
                  onClick={handleChangePassword}
                  disabled={passwordLoading}
                  className="flex-1 px-4 py-2 rounded-lg bg-gradient-to-r from-primary to-[#2575c0] text-white font-semibold hover:shadow-lg hover:shadow-primary/30 hover:-translate-y-0.5 transition-all active:scale-95 disabled:opacity-70 disabled:cursor-not-allowed flex items-center justify-center gap-2 relative overflow-hidden"
                >
                  {passwordLoading && (
                    <span className="animate-spin material-symbols-outlined">hourglass_bottom</span>
                  )}
                  {!passwordLoading && (
                    <span className="material-symbols-outlined text-[20px]">check</span>
                  )}
                  <span>{passwordLoading ? 'Updating...' : 'Update Password'}</span>
                </button>
              </div>
            </div>
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="mt-20 border-t border-slate-200 bg-white">
        <div className="max-w-7xl mx-auto px-4 py-12 grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <div className="bg-primary p-1 rounded">
                <span className="material-symbols-outlined text-white text-sm">health_metrics</span>
              </div>
              <span className="font-bold text-lg text-slate-900">MedVision AI</span>
            </div>
            <p className="text-slate-500 text-sm">Empowering patients with seamless health management tools and personalized care insights.</p>
          </div>
          <div>
            <h4 className="font-bold mb-4 text-slate-900">Product</h4>
            <ul className="text-sm space-y-2 text-slate-500">
              <li><a className="hover:text-primary transition-colors" href="#">Find Doctors</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">Health Plans</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">Telehealth</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">Pricing</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-4 text-slate-900">Support</h4>
            <ul className="text-sm space-y-2 text-slate-500">
              <li><a className="hover:text-primary transition-colors" href="#">Help Center</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">Contact Us</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">FAQs</a></li>
              <li><a className="hover:text-primary transition-colors" href="#">Privacy Policy</a></li>
            </ul>
          </div>
          <div>
            <h4 className="font-bold mb-4 text-slate-900">Download App</h4>
            <div className="flex flex-col gap-2">
              <button className="flex items-center gap-2 bg-slate-900 text-white px-4 py-2 rounded-lg border border-slate-700 hover:bg-slate-800 transition-colors">
                <span className="material-symbols-outlined">phone_iphone</span>
                <div className="text-left">
                  <p className="text-[10px] uppercase leading-none">Download on the</p>
                  <p className="text-sm font-bold leading-none">App Store</p>
                </div>
              </button>
              <button className="flex items-center gap-2 bg-slate-900 text-white px-4 py-2 rounded-lg border border-slate-700 hover:bg-slate-800 transition-colors">
                <span className="material-symbols-outlined">play_arrow</span>
                <div className="text-left">
                  <p className="text-[10px] uppercase leading-none">Get it on</p>
                  <p className="text-sm font-bold leading-none">Google Play</p>
                </div>
              </button>
            </div>
          </div>
        </div>
        <div className="border-t border-slate-200 p-6 text-center text-sm text-slate-500">
          © 2024 MedVision AI Services Inc. All rights reserved.
        </div>
      </footer>
    </div>
  )
}
