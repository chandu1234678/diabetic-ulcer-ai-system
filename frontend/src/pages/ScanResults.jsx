import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { logout } from '../services/api'

export default function ScanResults({ onLogout }) {
  const navigate = useNavigate()
  const location = useLocation()
  const [activeNav, setActiveNav] = useState('scans')

  const handleLogout = () => {
    if (onLogout) {
      onLogout()
    }
    navigate('/login', { replace: true })
  }

  // Get the uploaded image and prediction from navigation state
  const previewImage = location.state?.previewImage
  const prediction = location.state?.prediction || {}

  // Extract prediction data with defaults
  const {
    prediction: predictionLabel = 'ulcer',
    confidence = 0.98,
    risk_level = 'High',
    severity = 'Severe',
    explanation_text = 'AI model detected potential diabetic foot ulcer',
    recommendations = ['Schedule consultation with podiatrist', 'Monitor foot daily'],
    affected_area = 0,
    gradcam_overlay = null
  } = prediction

  // Determine alert color and icon based on prediction
  const isUlcer = predictionLabel.toLowerCase() === 'ulcer'
  const alertColor = isUlcer ? 'red' : 'green'
  const alertText = isUlcer ? 'Urgent Attention' : 'Normal'
  const resultTitle = isUlcer ? 'Ulcer Detected' : 'No Ulcer Detected'

  return (
    <div className="min-h-screen flex flex-col bg-light text-slate-900 font-display">
      {/* Header Navigation */}
      <header className="flex items-center bg-white p-4 border-b border-slate-200 sticky top-0 z-10 justify-between">
        <button
          onClick={() => navigate('/foot-scan-analysis')}
          className="text-primary flex size-10 items-center justify-center cursor-pointer hover:bg-slate-100 rounded-lg transition-colors"
        >
          <span className="material-symbols-outlined">arrow_back</span>
        </button>
        <h2 className="text-slate-900 text-lg font-bold leading-tight flex-1 text-center">Scan Results</h2>
        <div className="flex items-center gap-2">
          <button className="text-slate-900 hover:bg-slate-100 rounded-lg p-2 transition-colors">
            <span className="material-symbols-outlined">share</span>
          </button>
          <button
            onClick={handleLogout}
            className="text-slate-600 hover:bg-slate-100 rounded-lg p-2 transition-colors"
            title="Logout"
          >
            <span className="material-symbols-outlined">logout</span>
          </button>
        </div>
      </header>

      <main className="flex-1 overflow-y-auto pb-24">
        {/* Visual Comparison Section */}
        <div className="grid grid-cols-2 gap-3 p-4">
          <div className="flex flex-col gap-2">
            <div
              className="w-full aspect-square bg-slate-200 rounded-xl bg-cover bg-center"
              style={{
                backgroundImage: previewImage ? `url('${previewImage}')` : 'none'
              }}
            ></div>
            <p className="text-slate-600 text-sm font-medium text-center">Original Photo</p>
          </div>
          <div className="flex flex-col gap-2">
            <div
              className="w-full aspect-square bg-slate-200 rounded-xl bg-cover bg-center relative overflow-hidden"
              style={{
                backgroundImage: gradcam_overlay ? `url('${gradcam_overlay}')` : previewImage ? `url('${previewImage}')` : 'none'
              }}
            >
              {/* Heatmap Overlay Effect (only if ulcer detected) */}
              {isUlcer && (
                <>
                  <div className="absolute inset-0 bg-gradient-to-tr from-red-500/40 via-yellow-400/20 to-transparent mix-blend-overlay"></div>
                  <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-16 h-16 bg-red-500/60 blur-xl rounded-full animate-pulse"></div>
                </>
              )}
            </div>
            <p className="text-slate-600 text-sm font-medium text-center">AI Heatmap</p>
          </div>
        </div>

        {/* Detection Status */}
        <div className="px-4 text-center mt-4">
          <div className={`inline-flex items-center gap-2 px-3 py-1 rounded-full ${
            isUlcer ? 'bg-red-100 text-red-600' : 'bg-green-100 text-green-600'
          } mb-2`}>
            <span className="material-symbols-outlined text-sm">
              {isUlcer ? 'warning' : 'check_circle'}
            </span>
            <span className="text-xs font-bold uppercase tracking-wider">{alertText}</span>
          </div>
          <h1 className="text-slate-900 text-3xl font-extrabold tracking-tight">{resultTitle}</h1>
        </div>

        {/* Metric Cards */}
        <div className="grid grid-cols-2 gap-4 p-4 mt-2">
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <p className="text-slate-500 text-xs font-semibold uppercase tracking-wider mb-1">Confidence</p>
            <div className="flex items-baseline gap-1">
              <p className="text-slate-900 text-2xl font-bold">{Math.round(confidence * 100)}%</p>
              <span className={`material-symbols-outlined text-lg ${confidence > 0.8 ? 'text-primary' : 'text-slate-400'}`}>
                {confidence > 0.8 ? 'verified' : 'info'}
              </span>
            </div>
          </div>
          <div className="bg-white p-5 rounded-xl border border-slate-200 shadow-sm hover:shadow-md transition-shadow">
            <p className="text-slate-500 text-xs font-semibold uppercase tracking-wider mb-1">Risk Level</p>
            <div className="flex items-center gap-2">
              <p className={`text-2xl font-bold ${
                risk_level === 'High' || risk_level === 'Very High' ? 'text-red-600' :
                risk_level === 'Moderate' ? 'text-yellow-600' : 'text-green-600'
              }`}>{risk_level}</p>
              <div className="flex gap-1">
                {[1, 2, 3].map((i) => (
                  <div
                    key={i}
                    className={`w-2 h-4 rounded-full ${
                      (risk_level === 'High' && i >= 3) || 
                      (risk_level === 'Very High' && i >= 2) ||
                      (risk_level === 'Moderate' && i === 3)
                        ? 'bg-red-500' : 'bg-slate-200'
                    }`}
                  ></div>
                ))}
              </div>
            </div>
          </div>
        </div>

        {/* Additional Metrics */}
        {isUlcer && affected_area > 0 && (
          <div className="px-4 mt-2">
            <div className="bg-white p-4 rounded-xl border border-slate-200">
              <p className="text-slate-500 text-xs font-semibold uppercase tracking-wider mb-1">Affected Area</p>
              <p className="text-slate-900 text-xl font-bold">{affected_area.toFixed(1)}% of foot</p>
            </div>
          </div>
        )}

        {/* Severity Badge */}
        <div className="px-4 mt-4">
          <div className="bg-slate-100 p-3 rounded-lg">
            <p className="text-slate-700 text-sm">
              <span className="font-semibold">Severity Level:</span> {severity}
            </p>
          </div>
        </div>

        {/* AI Explanation Text */}
        <div className="px-4 pb-8 mt-4">
          <div className={`${isUlcer ? 'bg-red-50 border-red-100' : 'bg-green-50 border-green-100'} p-5 rounded-xl border`}>
            <div className="flex items-center gap-2 mb-3">
              <span className="material-symbols-outlined text-primary">auto_awesome</span>
              <h3 className="text-slate-900 font-bold">AI Analysis Summary</h3>
            </div>
            <p className="text-slate-700 text-sm leading-relaxed">
              {explanation_text}
            </p>

            {/* Recommendations */}
            {recommendations && recommendations.length > 0 && (
              <div className="mt-4 pt-4 border-t border-slate-200">
                <p className="text-slate-900 font-semibold text-sm mb-2">Recommendations:</p>
                <ul className="space-y-2">
                  {recommendations.map((rec, idx) => (
                    <li key={idx} className="flex gap-2 text-sm text-slate-700">
                      <span className="material-symbols-outlined text-sm text-primary flex-shrink-0">check</span>
                      {rec}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {isUlcer && (
              <button className="mt-4 w-full bg-primary text-white font-bold py-3 rounded-lg flex items-center justify-center gap-2 shadow-lg shadow-primary/30 hover:bg-primary/90 transition-colors">
                <span className="material-symbols-outlined">calendar_today</span>
                Book Appointment
              </button>
            )}
          </div>
        </div>
      </main>

      {/* Bottom Navigation Bar */}
      <nav className="bg-white border-t border-slate-200 pb-6 pt-2 px-4 shadow-[0_-4px_12px_rgba(0,0,0,0.05)] fixed bottom-0 left-0 right-0">
        <div className="flex justify-between items-center max-w-md mx-auto">
          <button
            onClick={() => {
              setActiveNav('home')
              navigate('/dashboard')
            }}
            className="flex flex-col items-center gap-1 text-slate-400 hover:text-slate-900 transition-colors"
          >
            <span className="material-symbols-outlined">home</span>
            <span className="text-[10px] font-bold uppercase">Home</span>
          </button>
          <button
            onClick={() => setActiveNav('scans')}
            className="flex flex-col items-center gap-1 text-primary"
          >
            <span className="material-symbols-outlined">camera</span>
            <span className="text-[10px] font-bold uppercase">Scans</span>
          </button>
          <button className="flex flex-col items-center gap-1 text-slate-400 hover:text-slate-900 transition-colors">
            <span className="material-symbols-outlined">bar_chart</span>
            <span className="text-[10px] font-bold uppercase">Reports</span>
          </button>
          <button className="flex flex-col items-center gap-1 text-slate-400 hover:text-slate-900 transition-colors">
            <span className="material-symbols-outlined">person</span>
            <span className="text-[10px] font-bold uppercase">Profile</span>
          </button>
        </div>
      </nav>
    </div>
  )
}
