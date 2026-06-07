"use client"
import { useState } from "react"
import { sendMessage } from "./lib/api"

export default function Home() {
  const [messages, setMessages] = useState<{role: string, content: string}[]>([])
  const [input, setInput] = useState("")
  const [loading, setLoading] = useState(false)

  const handleSend = async () => {
    if (!input.trim()) return
    const userMessage = { role: "user", content: input }
    setMessages(prev => [...prev, userMessage])
    setInput("")
    setLoading(true)
    const response = await sendMessage("havish_001", input)
    setLoading(false)
    setMessages(prev => [...prev, { role: "assistant", content: response }])
  }

  const profile = {
    major: "Computer Science",
    catalogYear: "2023",
    targetGraduation: "Winter 2027",
    completedCourses: ["EECS 280", "MATH 214", "EECS 203"]
  }

  return (
    <main className="flex h-screen bg-gray-950 text-white">
      {/* Chat Panel */}
      <div className="flex flex-col w-1/2 border-r border-gray-800">
        <div className="p-4 border-b border-gray-800">
          <h1 className="text-xl font-bold">Pathfinder</h1>
        </div>
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((m, i) => (
            <div key={i} className={`p-3 rounded-lg ${m.role === "user" ? "bg-blue-900 ml-8" : "bg-gray-800 mr-8"}`}>
              {m.content.split("\n").map((line, j) => (
                <p key={j}>{line}</p>
              ))}
            </div>
          ))}
          {loading && (
            <div className="bg-gray-800 mr-8 p-3 rounded-lg animate-pulse">
              Thinking...
            </div>
          )}
        </div>
        <div className="p-4 border-t border-gray-800 flex gap-2">
          <input
            className="flex-1 bg-gray-800 rounded-lg px-4 py-2 outline-none"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
            placeholder="Ask about your courses..."
          />
          <button onClick={handleSend} className="bg-blue-600 px-4 py-2 rounded-lg">Send</button>
        </div>
      </div>

      {/* Semester Plan Panel */}
      <div className="w-1/4 border-r border-gray-800 p-4">
        <h2 className="font-bold mb-4">Semester Plan</h2>
      </div>

      {/* Profile Panel */}
      <div className="w-1/4 p-4">
        <h2 className="font-bold mb-4">Your Profile</h2>
        <div className="space-y-3 text-sm text-gray-300">
          <p><span className="text-gray-500">Major:</span> {profile.major}</p>
          <p><span className="text-gray-500">Catalog Year:</span> {profile.catalogYear}</p>
          <p><span className="text-gray-500">Graduation:</span> {profile.targetGraduation}</p>
          <div>
            <p className="text-gray-500 mb-2">Completed:</p>
            {profile.completedCourses.map((c, i) => (
              <p key={i} className="bg-gray-800 px-2 py-1 rounded mb-1">{c}</p>
            ))}
          </div>
        </div>
      </div>
    </main>
  )
}