import { useState, useEffect, useRef, useCallback, memo } from 'react'
import { getHealthMetricsAssessment } from '../services/api'

// Memoize MetricCard to prevent unnecessary re-renders that cause focus loss
const MetricCard = memo(({ icon, label, value, placeholder, onChange, error, min, max, step, focusedField, setFocusedField, isRequired }) => (
  <div className="flex flex-col">
    <div className={`flex items-center gap-2 mb-2 transition-all ${focusedField === label ? 'scale-105' : ''}`}>
      <div className={`p-2 rounded-lg transition-all ${
        focusedField === label
          ? 'bg-primary/20 text-primary'
          : 'bg-slate-100 text-slate-500'
      }`}>
        <span className="material-symbols-outlined text-lg">{icon}</span>
      </div>
      <label className={`font-semibold transition-all uppercase tracking-wide ${
        focusedField === label
          ? 'text-primary text-sm'
          : 'text-slate-700 text-xs'
      }`}>
        {label}
        {isRequired && <span className="text-slate-400 ml-1">*</span>}
        {!isRequired && <span className="text-slate-400 ml-1 text-[10px]">(optional)</span>}
      </label>
    </div>
    <input
      type="number"
      min={min}
      max={max}
      step={step}
      value={value}
      onChange={(e) => onChange(e.target.value)}
      onFocus={() => setFocusedField(label)}
      onBlur={() => setFocusedField(null)}
      className={`w-full rounded-xl border-2 px-4 py-3 text-slate-900 outline-none transition-all font-semibold text-center ${
        focusedField === label
          ? 'border-primary/50 bg-primary/5 shadow-lg shadow-primary/20'
          : 'border-slate-200 bg-white hover:border-slate-300'
      }`}
      placeholder={placeholder}
    />
    {error && (
      <p className="text-xs text-red-600 mt-2 flex items-center gap-1">
        <span className="material-symbols-outlined text-sm">error</span>
        {error}
      </p>
    )}
  </div>
))

MetricCard.displayName = 'MetricCard'

export default function HealthMetricsForm({
  age,
  setAge,
  bmi,
  setBmi,
  sugarBeforeFast,
  setSugarBeforeFast,
  showOptional = true,
  isRequired = true,  // NEW: Make fields required only during prediction
  compact = false,
  className = '',
}) {
  const [ageError, setAgeError] = useState('')
  const [bmiError, setBmiError] = useState('')
  const [sugarError, setSugarError] = useState('')
  const [assessment, setAssessment] = useState(null)
  const [isLoading, setIsLoading] = useState(false)
  const [focusedField, setFocusedField] = useState(null)
  const debounceTimer = useRef(null)

  // Use useCallback to prevent function recreation on every render
  const handleAgeChange = useCallback((value) => {
    setAgeError('')
    const numValue = parseInt(value)
    // Only validate if required or if value is provided
    if (value && (isNaN(numValue) || numValue < 1 || numValue > 150)) {
      setAgeError('Age must be between 1 and 150')
    }
    setAge(value)
  }, [setAge])

  const handleBmiChange = useCallback((value) => {
    setBmiError('')
    const numValue = parseFloat(value)
    // Only validate if required or if value is provided
    if (value && (isNaN(numValue) || numValue < 10 || numValue > 60)) {
      setBmiError('BMI should be between 10 and 60')
    }
    setBmi(value)
  }, [setBmi])

  const handleSugarChange = useCallback((value) => {
    setSugarError('')
    const numValue = parseInt(value)
    // Only validate if required or if value is provided
    if (value && (isNaN(numValue) || numValue < 40 || numValue > 500)) {
      setSugarError('Blood sugar should be between 40 and 500 mg/dL')
    }
    setSugarBeforeFast(value)
  }, [setSugarBeforeFast])

  const fetchAssessment = useCallback(async () => {
    setIsLoading(true)
    try {
      const result = await getHealthMetricsAssessment({
        age: parseInt(age),
        bmi: parseFloat(bmi),
        blood_sugar: parseInt(sugarBeforeFast),
      })
      setAssessment(result)
    } catch (error) {
      console.error('Assessment error:', error)
    } finally {
      setIsLoading(false)
    }
  }, [age, bmi, sugarBeforeFast])

  // Calculate assessment when metrics change (with debounce to prevent API spam)
  // Only fetch if:
  // 1. All fields have values AND
  // 2. Either isRequired=false (optional mode, only fetch if user provided values)
  //    OR isRequired=true (required mode, always fetch if values exist)
  useEffect(() => {
    // Clear previous timeout
    if (debounceTimer.current) {
      clearTimeout(debounceTimer.current)
    }

    // Only fetch if all fields have values
    if (age && bmi && sugarBeforeFast) {
      // Delay API call by 500ms to allow smooth typing without triggering API calls
      debounceTimer.current = setTimeout(() => {
        fetchAssessment()
      }, 500)
    } else if (isRequired === false) {
      // In optional mode, clear assessment if fields are empty
      setAssessment(null)
    }

    // Cleanup on unmount
    return () => {
      if (debounceTimer.current) {
        clearTimeout(debounceTimer.current)
      }
    }
  }, [age, bmi, sugarBeforeFast, fetchAssessment, isRequired])

  const getRiskColor = (riskScore) => {
    if (riskScore < 30) return { bg: 'bg-green-50', border: 'border-green-200', text: 'text-green-700', label: 'Low Risk' }
    if (riskScore < 60) return { bg: 'bg-yellow-50', border: 'border-yellow-200', text: 'text-yellow-700', label: 'Moderate Risk' }
    return { bg: 'bg-red-50', border: 'border-red-200', text: 'text-red-700', label: 'High Risk' }
  }

  const getRiskMeterColor = (riskScore) => {
    if (riskScore < 30) return 'bg-green-500'
    if (riskScore < 60) return 'bg-yellow-500'
    return 'bg-red-500'
  }

  const containerClass = compact
    ? 'grid grid-cols-1 gap-3 sm:grid-cols-3'
    : 'grid grid-cols-1 gap-5 sm:grid-cols-3'

  return (
    <div className={`space-y-6 ${className}`}>
      {/* Main Metrics Grid */}
      <div className={containerClass}>
        <MetricCard
          icon="calendar_today"
          label="Age"
          value={age}
          placeholder="25"
          onChange={handleAgeChange}
          error={ageError}
          min={1}
          max={150}
          step={1}
          focusedField={focusedField}
          setFocusedField={setFocusedField}
          isRequired={isRequired}
        />
        <MetricCard
          icon="monitor_weight"
          label="BMI"
          value={bmi}
          placeholder="22.5"
          onChange={handleBmiChange}
          error={bmiError}
          min={10}
          max={60}
          step={0.1}
          focusedField={focusedField}
          setFocusedField={setFocusedField}
          isRequired={isRequired}
        />
        <MetricCard
          icon="local_florist"
          label="Blood Sugar"
          value={sugarBeforeFast}
          placeholder="120"
          onChange={handleSugarChange}
          error={sugarError}
          min={40}
          max={500}
          step={1}
          focusedField={focusedField}
          setFocusedField={setFocusedField}
          isRequired={isRequired}
        />
      </div>

      {/* Assessment Card */}
      {assessment && !isLoading && (
        <div className={`rounded-2xl border-2 p-5 transition-all ${getRiskColor(assessment.risk_score).bg} ${getRiskColor(assessment.risk_score).border}`}>
          <div className="space-y-4">
            {/* Risk Header */}
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <div className={`p-3 rounded-full ${getRiskColor(assessment.risk_score).bg} border-2 ${getRiskColor(assessment.risk_score).border}`}>
                  <span className="material-symbols-outlined text-xl" style={{ color: assessment.risk_score < 30 ? '#22c55e' : assessment.risk_score < 60 ? '#eab308' : '#ef4444' }}>
                    {assessment.risk_score < 30 ? 'verified' : assessment.risk_score < 60 ? 'warning' : 'error'}
                  </span>
                </div>
                <div>
                  <p className={`text-sm font-bold ${getRiskColor(assessment.risk_score).text}`}>
                    {getRiskColor(assessment.risk_score).label}
                  </p>
                  <p className="text-xs text-slate-600">Overall Health Assessment</p>
                </div>
              </div>
              <div className="text-right">
                <p className={`text-2xl font-bold ${getRiskColor(assessment.risk_score).text}`}>
                  {Math.round(assessment.risk_score)}%
                </p>
                <p className="text-xs text-slate-500">Risk Score</p>
              </div>
            </div>

            {/* Risk Meter */}
            <div className="space-y-2">
              <div className="flex items-center justify-between">
                <span className="text-xs font-semibold text-slate-600">Risk Level</span>
                <span className="text-xs text-slate-500">
                  {assessment.risk_score < 30 ? 'Safe' : assessment.risk_score < 60 ? 'Monitor' : 'Alert'}
                </span>
              </div>
              <div className="h-3 rounded-full bg-slate-200 overflow-hidden">
                <div
                  className={`h-full rounded-full transition-all duration-500 ${getRiskMeterColor(assessment.risk_score)} shadow-lg`}
                  style={{ width: `${assessment.risk_score}%` }}
                ></div>
              </div>
            </div>

            {/* Key Metrics */}
            {assessment.details && (
              <div className="grid grid-cols-3 gap-3 pt-2 border-t-2" style={{ borderColor: assessment.risk_score < 30 ? '#dcfce7' : assessment.risk_score < 60 ? '#fef3c7' : '#fee2e2' }}>
                {assessment.details.bmi_category && (
                  <div className="text-center">
                    <p className="text-xs font-bold text-slate-700">{assessment.details.bmi_category}</p>
                    <p className="text-[10px] text-slate-600">BMI Status</p>
                  </div>
                )}
                {assessment.details.sugar_level && (
                  <div className="text-center">
                    <p className="text-xs font-bold text-slate-700">{assessment.details.sugar_level}</p>
                    <p className="text-[10px] text-slate-600">Sugar Level</p>
                  </div>
                )}
                {assessment.details.age_group && (
                  <div className="text-center">
                    <p className="text-xs font-bold text-slate-700">{assessment.details.age_group}</p>
                    <p className="text-[10px] text-slate-600">Age Group</p>
                  </div>
                )}
              </div>
            )}

            {/* Recommendations */}
            {assessment.recommendations && assessment.recommendations.length > 0 && (
              <div className="space-y-2 pt-2">
                <p className="text-xs font-bold text-slate-700 flex items-center gap-1">
                  <span className="material-symbols-outlined text-sm">lightbulb</span>
                  Recommendations
                </p>
                <div className="space-y-1">
                  {assessment.recommendations.slice(0, 2).map((rec, idx) => (
                    <p key={idx} className="text-xs text-slate-700 flex items-start gap-2">
                      <span className="text-primary font-bold">✓</span>
                      {rec}
                    </p>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Loading State */}
      {isLoading && (
        <div className="rounded-2xl bg-gradient-to-r from-primary/5 to-blue-500/5 p-5 flex items-center justify-center gap-3 border-2 border-primary/20">
          <div className="animate-spin">
            <span className="material-symbols-outlined text-primary text-2xl">refresh</span>
          </div>
          <p className="text-sm font-semibold text-primary">Calculating risk assessment...</p>
        </div>
      )}
    </div>
  )
}
