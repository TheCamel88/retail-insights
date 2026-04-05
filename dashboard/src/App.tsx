import { useState } from 'react'
import Login from './Login'
import Dashboard from './Dashboard'

export default function App() {
  const [token, setToken] = useState(localStorage.getItem('token'))
  const [email, setEmail] = useState(localStorage.getItem('email') || '')
  const handleLogin = (t, e) => { setToken(t); setEmail(e) }
  const handleLogout = () => { localStorage.removeItem('token'); localStorage.removeItem('email'); setToken(null) }
  if (!token) return <Login onLogin={handleLogin} />
  return <Dashboard email={email} onLogout={handleLogout} />
}