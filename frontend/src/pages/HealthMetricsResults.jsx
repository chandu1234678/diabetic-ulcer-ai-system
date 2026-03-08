import { useNavigate, useLocation } from 'react-router-dom'
import DashboardHeader from '../components/DashboardHeader'

export default function HealthMetricsResults({ onLogout }) {
  const navigate = useNavigate()
  const location = useLocation()

  // Get assessment data from location state
  const assessment = location.state?.assessment || {}
  const healthMetrics = location.state?.healthMetrics || {}
  const previewImage = location.state?.previewImage || null

  const {
    risk_score = 0,
    risk_level = 'Unknown',
    details = {},
    recommendations = [],
  } = assessment

  // Determine colors and icons based on risk
  const getRiskColor = (score) => {
    if (score < 30) return { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-700', icon: 'verified', label: 'Low Risk' }
    if (score < 60) return { bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-700', icon: 'warning', label: 'Moderate Risk' }
    return { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700', icon: 'error', label: 'High Risk' }
  }

  const getRiskMeterColor = (score) => {
    if (score < 30) return 'bg-green-500'
    if (score < 60) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const riskColor = getRiskColor(risk_score)

  return (
    <div className="min-h-screen flex flex-col bg-background-light text-slate-900 font-display">
      <DashboardHeader 
        title="HealthScan AI" 
        showBackButton={true}
        backTo="/foot-scan-analysis"
        onLogout={onLogout}
      />

      <main className="flex-1 overflow-y-auto pb-24">
        <div className="mx-auto max-w-6xl p-4 lg:p-8">
          {/* Title Section */}
          <div className="mb-8 text-center">
            <h2 className="text-3xl font-extrabold tracking-tight sm:text-4xl text-slate-900">Health Metrics Assessment</h2>
            <p className="mt-3 text-lg text-slate-600">Your personalized risk assessment based on health data</p>
          </div>

          {/* Two Column Layout */}
          <div className="grid gap-8 lg:grid-cols-2">
            {/* Left Column - Images & Visual Metrics */}
            <div className="space-y-6">
              {/* Main Assessment Card */}
              <div className={`rounded-2xl border-2 p-8 ${riskColor.bg} ${riskColor.border} shadow-lg`}>
                <div className="space-y-6">
                  {/* Risk Header */}
                  <div className="flex items-center justify-between">
                    <div className="flex items-center gap-4">
                      <div className={`p-4 rounded-full ${riskColor.bg} border-2 ${riskColor.border}`}>
                        <span className="material-symbols-outlined text-3xl" style={{
                          color: risk_score < 30 ? '#22c55e' : risk_score < 60 ? '#eab308' : '#ef4444'
                        }}>
                          {riskColor.icon}
                        </span>
                      </div>
                      <div>
                        <p className={`text-xl font-bold ${riskColor.text}`}>
                          {riskColor.label}
                        </p>
                        <p className="text-sm text-slate-600">Overall Health Assessment</p>
                      </div>
                    </div>
                    <div className="text-right">
                      <p className={`text-4xl font-bold ${riskColor.text}`}>
                        {Math.round(risk_score)}%
                      </p>
                      <p className="text-xs text-slate-500">Risk Score</p>
                    </div>
                  </div>

                  {/* Risk Meter */}
                  <div className="space-y-3 pt-4 border-t-2" style={{ borderColor: risk_score < 30 ? '#dcfce7' : risk_score < 60 ? '#fef3c7' : '#fee2e2' }}>
                    <div className="flex items-center justify-between">
                      <span className="text-sm font-semibold text-slate-700">Risk Level</span>
                      <span className="text-sm text-slate-600">
                        {risk_score < 30 ? 'Safe' : risk_score < 60 ? 'Monitor' : 'Alert'}
                      </span>
                    </div>
                    <div className="h-4 rounded-full bg-slate-200 overflow-hidden">
                      <div
                        className={`h-full rounded-full transition-all duration-500 ${getRiskMeterColor(risk_score)} shadow-lg`}
                        style={{ width: `${risk_score}%` }}
                      ></div>
                    </div>
                  </div>

                  {/* Key Metrics Grid */}
                  {details && Object.keys(details).length > 0 && (
                    <div className="grid grid-cols-3 gap-3 pt-4 border-t-2" style={{ borderColor: risk_score < 30 ? '#dcfce7' : risk_score < 60 ? '#fef3c7' : '#fee2e2' }}>
                      {details.bmi_category && (
                        <div className="bg-white/50 rounded-lg p-3 text-center">
                          <p className="text-sm font-bold text-slate-800">{details.bmi_category}</p>
                          <p className="text-xs text-slate-600 mt-1">BMI Status</p>
                        </div>
                      )}
                      {details.sugar_level && (
                        <div className="bg-white/50 rounded-lg p-3 text-center">
                          <p className="text-sm font-bold text-slate-800">{details.sugar_level}</p>
                          <p className="text-xs text-slate-600 mt-1">Sugar Level</p>
                        </div>
                      )}
                      {details.age_group && (
                        <div className="bg-white/50 rounded-lg p-3 text-center">
                          <p className="text-sm font-bold text-slate-800">{details.age_group}</p>
                          <p className="text-xs text-slate-600 mt-1">Age Group</p>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>

              {/* Health Metrics Input Summary */}
              <div className="rounded-2xl border-2 border-slate-200 bg-white p-6 shadow-md">
                <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                  <span className="material-symbols-outlined text-primary">favorite</span>
                  Your Health Data
                </h3>
                <div className="grid grid-cols-3 gap-4">
                  <div className="flex flex-col items-center p-3 rounded-lg bg-slate-50">
                    <span className="text-2xl font-bold text-primary">{healthMetrics.age}</span>
                    <p className="text-xs text-slate-600 mt-2">Age (years)</p>
                  </div>
                  <div className="flex flex-col items-center p-3 rounded-lg bg-slate-50">
                    <span className="text-2xl font-bold text-primary">{healthMetrics.bmi?.toFixed(1)}</span>
                    <p className="text-xs text-slate-600 mt-2">BMI</p>
                  </div>
                  <div className="flex flex-col items-center p-3 rounded-lg bg-slate-50">
                    <span className="text-2xl font-bold text-primary">{healthMetrics.bloodSugar}</span>
                    <p className="text-xs text-slate-600 mt-2">Blood Sugar (mg/dL)</p>
                  </div>
                </div>
              </div>
            </div>

            {/* Right Column - Recommendations */}
            <div className="space-y-6">
              {/* Recommendations Card */}
              {recommendations && recommendations.length > 0 && (
                <div className="rounded-2xl border-2 border-blue-200 bg-blue-50 p-6 shadow-md">
                  <h3 className="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
                    <span className="material-symbols-outlined text-blue-600 text-2xl">lightbulb</span>
                    Health Recommendations
                  </h3>
                  <div className="space-y-3">
                    {recommendations.map((rec, idx) => (
                      <div key={idx} className="flex items-start gap-3 p-3 bg-white rounded-lg border border-blue-100">
                        <span className="text-blue-600 font-bold text-lg flex-shrink-0 mt-0.5">✓</span>
                        <p className="text-sm text-slate-700 leading-relaxed">{rec}</p>
                      </div>
                    ))}
                  </div>
                </div>
              )}

              {/* Guidance Card */}
              <div className="rounded-2xl border-2 border-purple-200 bg-purple-50 p-6 shadow-md">
                <h3 className="text-lg font-bold text-slate-900 mb-3 flex items-center gap-2">
                  <span className="material-symbols-outlined text-purple-600 text-2xl">info</span>
                  Next Steps
                </h3>
                <ul className="space-y-2 text-sm text-slate-700">
                  <li className="flex items-start gap-2">
                    <span className="text-purple-600 font-bold">1.</span>
                    <span>Review your health metrics regularly</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-purple-600 font-bold">2.</span>
                    <span>Follow the recommendations above</span>
                  </li>
                  <li className="flex items-start gap-2">
                    <span className="text-purple-600 font-bold">3.</span>
                    <span>Consult with healthcare provider if needed</span>
                  </li>
                  {risk_score >= 60 && (
                    <li className="flex items-start gap-2">
                      <span className="text-red-600 font-bold">⚠</span>
                      <span className="text-red-600 font-semibold">High risk: Schedule medical consultation</span>
                    </li>
                  )}
                </ul>
              </div>

              {/* CTA Buttons */}
              <div className="flex flex-col gap-3">
                <button
                  onClick={() => navigate('/foot-scan-analysis')}
                  className="flex items-center justify-center gap-2 px-6 py-3 rounded-lg bg-primary text-white font-semibold hover:bg-primary/90 transition-colors shadow-lg shadow-primary/30"
                >
                  <span className="material-symbols-outlined">camera</span>
                  Analyze Foot Image
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
