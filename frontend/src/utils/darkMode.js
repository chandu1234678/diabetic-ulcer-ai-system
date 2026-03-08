// Dark mode is disabled globally
export const applyDarkMode = () => {
  // Force light mode always
  localStorage.setItem('darkMode', 'false')
  document.documentElement.classList.remove('dark')
  return false
}

export const toggleDarkMode = (enabled) => {
  // Ignore requests to toggle - always light mode
  localStorage.setItem('darkMode', 'false')
  document.documentElement.classList.remove('dark')
}

