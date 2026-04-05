import { useState } from 'react'

export default function Login({ onLogin }: { onLogin: (token: string, email: string) => void }) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [mode, setMode] = useState<'login'|'signup'>('login')

  const submit = async () => {
    setLoading(true); setError('')
    const endpoint = mode === 'login' ? '/api/auth/login' : '/api/auth/signup'
    const body = mode === 'login' ? { email, password } : { email, password, organization_name: 'My Store' }
    const r = await fetch(endpoint, { method: 'POST', headers: {'Content-Type':'application/json'}, body: JSON.stringify(body) })
    const d = await r.json()
    setLoading(false)
    if (r.status !== 200) { setError(d.detail || 'Something went wrong'); return }
    localStorage.setItem('token', d.token)
    localStorage.setItem('email', d.email)
    onLogin(d.token, d.email)
  }

  return (
    <div style={{minHeight:'100vh',background:'#0f172a',display:'flex',alignItems:'center',justifyContent:'center'}}>
      <div style={{background:'#1e293b',borderRadius:16,padding:40,width:380,border:'1px solid #334155'}}>
        <div style={{fontSize:24,fontWeight:700,color:'#a78bfa',marginBottom:8}}>◈ Retail Insights</div>
        <div style={{color:'#64748b',marginBottom:32,fontSize:14}}>{mode === 'login' ? 'Sign in to your account' : 'Create your account'}</div>
        <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)}
          style={{width:'100%',padding:'10px 14px',background:'#0f172a',border:'1px solid #334155',borderRadius:8,color:'#f1f5f9',fontSize:14,marginBottom:12,boxSizing:'border-box' as any}}/>
        <input placeholder="Password" type="password" value={password} onChange={e=>setPassword(e.target.value)}
          style={{width:'100%',padding:'10px 14px',background:'#0f172a',border:'1px solid #334155',borderRadius:8,color:'#f1f5f9',fontSize:14,marginBottom:16,boxSizing:'border-box' as any}}/>
        {error && <div style={{color:'#f87171',fontSize:13,marginBottom:12}}>{error}</div>}
        <button onClick={submit} disabled={loading}
          style={{width:'100%',padding:'11px',background:'#6366f1',color:'#fff',border:'none',borderRadius:8,fontSize:15,fontWeight:600,cursor:'pointer',marginBottom:16}}>
          {loading ? 'Please wait...' : mode === 'login' ? 'Sign In' : 'Create Account'}
        </button>
        <div style={{textAlign:'center' as any,color:'#64748b',fontSize:13}}>
          {mode === 'login' ? "No account? " : 'Have an account? '}
          <span onClick={()=>setMode(mode==='login'?'signup':'login')} style={{color:'#a78bfa',cursor:'pointer'}}>
            {mode === 'login' ? 'Sign up' : 'Sign in'}
          </span>
        </div>
      </div>
    </div>
  )
}
