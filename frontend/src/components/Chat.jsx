import React, { useState, useRef } from 'react'


export default function Chat(){
const [input, setInput] = useState('')
const [messages, setMessages] = useState([])
const evtSourceRef = useRef(null)


const sendMessage = async () => {
if (!input.trim()) return
const userMsg = input
setMessages(prev => [...prev, {role: 'user', text: userMsg}])
setInput('')


// Close previous source if open
if (evtSourceRef.current) {
try { evtSourceRef.current.close() } catch(e){/* ignore */}
}


// Start SSE via fetch and ReadableStream
try {
const resp = await fetch('/api/chat/stream', {
method: 'POST',
headers: { 'Content-Type': 'application/json' },
body: JSON.stringify({ message: userMsg })
})


if (!resp.ok) {
setMessages(prev => [...prev, {role: 'astra', text: 'Server error: ' + resp.statusText}])
return
}


const reader = resp.body.getReader()
const decoder = new TextDecoder('utf-8')
let astraText = ''


while (true) {
const { done, value } = await reader.read()
if (done) break
const chunk = decoder.decode(value)
// chunk may contain multiple SSE events; split by double newline
const parts = chunk.split('\n\n')
for (const part of parts) }