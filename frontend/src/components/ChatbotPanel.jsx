import { useMemo, useState } from 'react'

const canned = {
  upload: 'Use the upload card to submit JPG, PNG, or DICOM scans for analysis.',
  report:
    'After prediction, click Export Report (PDF) to generate a downloadable summary.',
  risk: 'High risk predictions should be reviewed by a clinician immediately.',
  default:
    'I can help with upload steps, prediction details, risk levels, and report export.',
}

function getReply(message) {
  const text = message.toLowerCase()
  if (text.includes('upload')) return canned.upload
  if (text.includes('report')) return canned.report
  if (text.includes('risk')) return canned.risk
  return canned.default
}

export default function ChatbotPanel() {
  const [messages, setMessages] = useState([
    {
      id: 1,
      role: 'bot',
      text: 'Hello, I am MedVision Assistant. Ask me anything about this analysis page.',
    },
  ])
  const [input, setInput] = useState('')

  const canSend = useMemo(() => input.trim().length > 0, [input])

  const sendMessage = (event) => {
    event.preventDefault()
    if (!canSend) return

    const userText = input.trim()
    const user = { id: Date.now(), role: 'user', text: userText }
    const bot = { id: Date.now() + 1, role: 'bot', text: getReply(userText) }

    setMessages((prev) => [...prev, user, bot])
    setInput('')
  }

  return (
    <div className="rounded-2xl border border-slate-200 bg-white shadow-sm">
      <div className="border-b border-slate-200 px-4 py-3">
        <h3 className="text-sm font-bold text-slate-800">Live Chatbot</h3>
      </div>

      <div className="max-h-72 space-y-3 overflow-y-auto px-4 py-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`max-w-[90%] rounded-xl px-3 py-2 text-sm ${
              message.role === 'user'
                ? 'ml-auto bg-primary text-white'
                : 'bg-slate-100 text-slate-700'
            }`}
          >
            {message.text}
          </div>
        ))}
      </div>

      <form onSubmit={sendMessage} className="flex gap-2 border-t border-slate-200 p-3">
        <input
          value={input}
          onChange={(event) => setInput(event.target.value)}
          placeholder="Ask MedVision Assistant..."
          className="flex-1 rounded-lg border border-slate-300 px-3 py-2 text-sm outline-none focus:border-primary"
        />
        <button
          type="submit"
          disabled={!canSend}
          className="rounded-lg bg-primary px-4 py-2 text-sm font-semibold text-white disabled:cursor-not-allowed disabled:opacity-50"
        >
          Send
        </button>
      </form>
    </div>
  )
}
