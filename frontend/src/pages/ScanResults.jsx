import { useState } from 'react'
import { useNavigate, useLocation } from 'react-router-dom'
import { logout } from '../services/api'
import DashboardHeader from '../components/DashboardHeader'

export default function ScanResults({ onLogout }) {
  const navigate = useNavigate()
  const location = useLocation()

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
      <DashboardHeader 
        title="Scan Results" 
        showBackButton={true}
        backTo="/foot-scan-analysis"
        onLogout={onLogout}
      />

      <main className="flex-1 overflow-y-auto pb-24">
        <div className="mx-auto max-w-6xl p-4 lg:p-8">
          {/* Title Section */}
          <div className="mb-8 text-center">
            <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl text-slate-900">Foot Scan Analysis</h2>
            <p className="mt-3 text-lg text-slate-600">AI-powered diagnostic results and recommendations</p>
          </div>

          {/* Two Column Layout */}
          <div className="grid gap-8 lg:grid-cols-2">
            {/* Left Column - Images */}
            <div className="space-y-6">
              {/* Images Section */}
              <div className="space-y-4">
                <h3 className="text-lg font-bold text-slate-900">Image Analysis</h3>
                <div className="grid grid-cols-2 gap-4">
                  <div className="flex flex-col gap-3">
                    <div
                      className="w-full aspect-square bg-slate-200 rounded-xl bg-cover bg-center border-2 border-slate-200 overflow-hidden"
                      style={{
                        backgroundImage: previewImage ? `url('${previewImage}')` : 'none'
                      }}
                    ></div>
                    <p className="text-slate-600 text-sm font-semibold text-center">Original Image</p>
                  </div>
                  <div className="flex flex-col gap-3">
                    <div
                      className="w-full aspect-square bg-slate-200 rounded-xl bg-cover bg-center border-2 border-slate-200 overflow-hidden relative"
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
                    <p className="text-slate-600 text-sm font-semibold text-center">AI Heatmap</p>
                  </div>
                </div>
              </div>

              {/* Key Metrics */}
              <div className="rounded-2xl border-2 border-slate-200 bg-white p-6 shadow-md">
                <h3 className="text-lg font-bold text-slate-900 mb-4">Analysis Metrics</h3>
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 border border-slate-200">
                    <div>
                      <p className="text-sm text-slate-600 font-medium">Confidence Score</p>
                      <p className="text-2xl font-bold text-slate-900 mt-1">{Math.round(confidence * 100)}%</p>
                    </div>
                    <span className={`material-symbols-outlined text-3xl ${confidence > 0.8 ? 'text-primary' : 'text-slate-400'}`}>
                      {confidence > 0.8 ? 'verified' : 'info'}
                    </span>
                  </div>
                  <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 border border-slate-200">
                    <div>
                      <p className="text-sm text-slate-600 font-medium">Risk Level</p>
                      <p className={`text-2xl font-bold mt-1 ${
                        risk_level === 'High' || risk_level === 'Very High' ? 'text-red-600' :
                        risk_level === 'Moderate' ? 'text-yellow-600' : 'text-green-600'
                      }`}>{risk_level}</p>
                    </div>
                    <span className="material-symbols-outlined text-3xl" style={{
                      color: risk_level === 'High' || risk_level === 'Very High' ? '#ef4444' :
                             risk_level === 'Moderate' ? '#eab308' : '#22c55e'
                    }}>
                      {risk_level === 'High' || risk_level === 'Very High' ? 'error' :
                       risk_level === 'Moderate' ? 'warning' : 'check_circle'}
                    </span>
                  </div>
                  {isUlcer && affected_area > 0 && (
                    <div className="flex items-center justify-between p-4 rounded-lg bg-slate-50 border border-slate-200">
                      <div>
                        <p className="text-sm text-slate-600 font-medium">Affected Area</p>
                        <p className="text-2xl font-bold text-slate-900 mt-1">{affected_area.toFixed(1)}%</p>
                      </div>
                      <span className="material-symbols-outlined text-3xl text-orange-500">location_on</span>
                    </div>
                  )}
                </div>
              </div>
            </div>

            {/* Right Column - Details & Recommendations */}
            <div className="space-y-6">
              {/* Detection Status Card */}
              <div className={`rounded-2xl border-2 p-6 shadow-lg ${
                isUlcer ? 'border-red-200 bg-red-50' : 'border-green-200 bg-green-50'
              }`}>
                <div className="flex items-start gap-4">
                  <div className={`p-3 rounded-full flex-shrink-0 ${isUlcer ? 'bg-red-100' : 'bg-green-100'}`}>
                    <span className="material-symbols-outlined text-2xl" style={{
                      color: isUlcer ? '#ef4444' : '#22c55e'
                    }}>
                      {isUlcer ? 'warning' : 'check_circle'}
                    </span>
                  </div>
                  <div>
                    <p className={`text-sm font-bold uppercase tracking-wider ${isUlcer ? 'text-red-600' : 'text-green-600'}`}>
                      {alertText}
                    </p>
                    <h1 className="text-2xl font-extrabold text-slate-900 mt-2">{resultTitle}</h1>
                    <p className={`text-sm mt-2 ${isUlcer ? 'text-red-700' : 'text-green-700'}`}>
                      {`Severity: ${severity}`}
                    </p>
                  </div>
                </div>
              </div>

              {/* AI Analysis Summary */}
              <div className="rounded-2xl border-2 border-blue-200 bg-blue-50 p-6 shadow-md">
                <h3 className="text-lg font-bold text-slate-900 mb-3 flex items-center gap-2">
                  <span className="material-symbols-outlined text-blue-600 text-2xl">auto_awesome</span>
                  AI Analysis
                </h3>
                <p className="text-slate-700 leading-relaxed text-sm">
                  {explanation_text}
                </p>
              </div>

              {/* Recommendations */}
              {recommendations && recommendations.length > 0 && (
                <div className="rounded-2xl border-2 border-purple-200 bg-purple-50 p-6 shadow-md">
                  <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <span className="material-symbols-outlined text-purple-600 text-2xl">lightbulb</span>
                    Recommendations
                  </h3>
                  <ul className="space-y-3">
                    {recommendations.map((rec, idx) => (
                      <li key={idx} className="flex items-start gap-3 p-3 bg-white rounded-lg border border-purple-100">
                        <span className="text-purple-600 font-bold text-lg flex-shrink-0 mt-0.5">✓</span>
                        <span className="text-sm text-slate-700">{rec}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              )}

              {/* CTA Buttons */}
              <div className="flex flex-col gap-3">
                {isUlcer && (
                  <button className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-red-600 text-white font-semibold hover:bg-red-700 transition-colors shadow-lg shadow-red-600/30">
                    <span className="material-symbols-outlined">calendar_today</span>
                    Book Appointment
                  </button>
                )}
                <button
                  onClick={() => navigate('/foot-scan-analysis')}
                  className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-primary text-white font-semibold hover:bg-primary/90 transition-colors shadow-lg shadow-primary/30"
                >
                  <span className="material-symbols-outlined">camera</span>
                  New Analysis
                </button>
                <button
                  onClick={() => navigate('/dashboard')}
                  className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-slate-200 text-slate-900 font-semibold hover:bg-slate-300 transition-colors"
                >
                  <span className="material-symbols-outlined">dashboard</span>
                  Back to Dashboard
                </button>
              </div>
            </div>
          </div>
        </div>
      </main>
    </div>
  )
}
