import { useState, useEffect } from 'react'
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const STORE_ID = 'store_001'
const API = '/api'
const COLORS = ['#6366f1', '#8b5cf6', '#a78bfa', '#c4b5fd']

const RANGES = [
  { label: 'Today', days: 1 },
  { label: '7 Days', days: 7 },
  { label: '30 Days', days: 30 },
]

function getRange(days: number) {
  const end = new Date()
  const start = new Date()
  start.setDate(start.getDate() - days)
  return {
    start: start.toISOString().slice(0, 19),
    end: end.toISOString().slice(0, 19),
  }
}

export default function Dashboard({ email, onLogout }: { email: string, onLogout: () => void }) {
  const [dwell, setDwell] = useState<any[]>([])
  const [traffic, setTraffic] = useState<any[]>([])
  const [insight, setInsight] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)
  const [generating, setGenerating] = useState(false)
  const [selectedRange, setSelectedRange] = useState(0)

  useEffect(() => {
    setLoading(true)
    const { start, end } = getRange(RANGES[selectedRange].days)
    Promise.all([
      fetch(`${API}/analytics/${STORE_ID}/dwell?start=${start}&end=${end}`).then(r=>r.json()),
      fetch(`${API}/analytics/${STORE_ID}/traffic?start=${start}&end=${end}`).then(r=>r.json()),
      fetch(`${API}/recommendations/${STORE_ID}/latest`).then(r=>r.json()),
    ]).then(([dwellData, trafficData, insightData]) => {
      setDwell(dwellData.dwell || [])
      setTraffic((trafficData.traffic || []).map((t: any) => ({
        hour: new Date(t.hour).toLocaleDateString('en-US', {month:'short', day:'numeric', hour:'numeric'}),
        visitors: t.count
      })))
      setInsight(insightData.summary || null)
      setLoading(false)
    })
  }, [selectedRange])

  const generate = async () => {
    setGenerating(true)
    const r = await fetch(`${API}/recommendations/${STORE_ID}/generate`, {method:'POST'})
    const d = await r.json()
    setInsight(d.summary)
    setGenerating(false)
  }

  return (
    <div style={{minHeight:'100vh',background:'#0f172a',color:'#f1f5f9',fontFamily:'system-ui'}}>
      <div style={{borderBottom:'1px solid #1e293b',padding:'0 32px'}}>
        <div style={{maxWidth:1100,margin:'0 auto',height:60,display:'flex',alignItems:'center',justifyContent:'space-between'}}>
          <div style={{fontSize:20,fontWeight:700,color:'#a78bfa'}}>◈ Retail Insights</div>
          <div style={{display:'flex',alignItems:'center',gap:16}}>
            <div style={{color:'#64748b',fontSize:13}}>{email}</div>
            <button onClick={onLogout} style={{background:'transparent',color:'#64748b',border:'1px solid #334155',borderRadius:8,padding:'4px 12px',fontSize:13,cursor:'pointer'}}>Logout</button>
          </div>
        </div>
      </div>
      <div style={{maxWidth:1100,margin:'0 auto',padding:'40px 32px'}}>

        <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:32}}>
          <div>
            <h1 style={{fontSize:32,fontWeight:700,margin:0}}>Store Overview</h1>
            <p style={{color:'#64748b',margin:'6px 0 0'}}>Store 001</p>
          </div>
          <div style={{display:'flex',gap:8}}>
            {RANGES.map((r, i) => (
              <button
                key={r.label}
                onClick={() => setSelectedRange(i)}
                style={{
                  padding:'8px 16px',
                  borderRadius:8,
                  border:'1px solid #334155',
                  fontSize:13,
                  fontWeight:600,
                  cursor:'pointer',
                  background: selectedRange === i ? '#6366f1' : 'transparent',
                  color: selectedRange === i ? '#fff' : '#94a3b8',
                }}
              >
                {r.label}
              </button>
            ))}
          </div>
        </div>

        <div style={{background:'#1e293b',borderRadius:12,padding:28,border:'1px solid #334155',marginBottom:24}}>
          <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:16}}>
            <div>
              <h2 style={{fontSize:17,fontWeight:600,margin:'0 0 4px'}}>Live Camera Feed</h2>
              <p style={{color:'#64748b',fontSize:13,margin:0}}>Real-time view from store camera</p>
            </div>
            <div style={{display:'flex',alignItems:'center',gap:8}}>
              <div style={{width:8,height:8,borderRadius:'50%',background:'#22c55e'}}/>
              <span style={{color:'#22c55e',fontSize:13,fontWeight:600}}>LIVE</span>
            </div>
          </div>
          <img
            src="http://localhost:8000/stream/feed"
            style={{width:'100%',borderRadius:8,maxHeight:400,objectFit:'cover',background:'#0f172a'}}
            alt="Live camera feed"
          />
        </div>

        <div style={{display:'grid',gridTemplateColumns:'repeat(3,1fr)',gap:16,marginBottom:24}}>
          <div style={{background:'#1e293b',borderRadius:12,padding:'24px 28px',border:'1px solid #334155'}}>
            <div style={{color:'#64748b',fontSize:13,marginBottom:8}}>TOTAL VISITS</div>
            <div style={{fontSize:36,fontWeight:700,color:'#a78bfa'}}>{loading ? '...' : dwell.reduce((a,z)=>a+z.visits,0)}</div>
          </div>
          <div style={{background:'#1e293b',borderRadius:12,padding:'24px 28px',border:'1px solid #334155'}}>
            <div style={{color:'#64748b',fontSize:13,marginBottom:8}}>AVG DWELL</div>
            <div style={{fontSize:36,fontWeight:700,color:'#a78bfa'}}>{loading ? '...' : Math.round(dwell.reduce((a,z)=>a+z.avg_seconds,0)/(dwell.length||1))}s</div>
          </div>
          <div style={{background:'#1e293b',borderRadius:12,padding:'24px 28px',border:'1px solid #334155'}}>
            <div style={{color:'#64748b',fontSize:13,marginBottom:8}}>PEAK HOUR</div>
            <div style={{fontSize:36,fontWeight:700,color:'#a78bfa'}}>{loading ? '...' : traffic.length ? traffic.reduce((a,b)=>a.visitors>b.visitors?a:b).hour : '-'}</div>
          </div>
        </div>

        <div style={{background:'#1e293b',borderRadius:12,padding:28,border:'1px solid #334155',marginBottom:24}}>
          <h2 style={{fontSize:17,fontWeight:600,margin:'0 0 4px'}}>Foot Traffic</h2>
          <p style={{color:'#64748b',fontSize:13,margin:'0 0 24px'}}>Visitors detected — {RANGES[selectedRange].label}</p>
          {loading ? <div style={{color:'#64748b',textAlign:'center',padding:40}}>Loading...</div> :
          <ResponsiveContainer width='100%' height={220}>
            <BarChart data={traffic} margin={{left:0,right:20}}>
              <XAxis dataKey='hour' stroke='#94a3b8' tick={{fontSize:11}}/>
              <YAxis stroke='#94a3b8' tick={{fontSize:12}} allowDecimals={false}/>
              <Tooltip formatter={(v:any)=>[v,'Visitors']} contentStyle={{background:'#1e293b',border:'none',color:'#f1f5f9'}}/>
              <Bar dataKey='visitors' radius={[6,6,0,0]} fill='#6366f1'/>
            </BarChart>
          </ResponsiveContainer>}
        </div>

        <div style={{display:'grid',gridTemplateColumns:'1fr 1fr',gap:16,marginBottom:24}}>
          <div style={{background:'#1e293b',borderRadius:12,padding:28,border:'1px solid #334155'}}>
            <h2 style={{fontSize:17,fontWeight:600,margin:'0 0 20px'}}>Dwell Time by Zone</h2>
            {loading ? <div style={{color:'#64748b',textAlign:'center',padding:40}}>Loading...</div> :
            <ResponsiveContainer width='100%' height={220}>
              <BarChart data={dwell} layout='vertical' margin={{left:20,right:30}}>
                <XAxis type='number' stroke='#94a3b8' tick={{fontSize:12}}/>
                <YAxis dataKey='zone' type='category' stroke='#94a3b8' tick={{fontSize:13}} width={90}/>
                <Tooltip formatter={(v:any)=>[v+'s','Dwell']} contentStyle={{background:'#1e293b',border:'none',color:'#f1f5f9'}}/>
                <Bar dataKey='avg_seconds' radius={[0,6,6,0]}>{dwell.map((_,i)=><Cell key={i} fill={COLORS[i%4]}/>)}</Bar>
              </BarChart>
            </ResponsiveContainer>}
          </div>
          <div style={{background:'#1e293b',borderRadius:12,padding:28,border:'1px solid #334155'}}>
            <h2 style={{fontSize:17,fontWeight:600,margin:'0 0 20px'}}>Zone Performance</h2>
            {loading ? <div style={{color:'#64748b',textAlign:'center',padding:40}}>Loading...</div> :
            dwell.map((z,i)=>(
              <div key={z.zone} style={{display:'flex',alignItems:'center',gap:12,marginBottom:16}}>
                <div style={{width:10,height:10,borderRadius:'50%',background:COLORS[i%4]}}/>
                <div>
                  <div style={{fontSize:14,fontWeight:600}}>{z.zone}</div>
                  <div style={{fontSize:12,color:'#64748b'}}>{z.visits} visit · {z.avg_seconds}s avg</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div style={{background:'#1e293b',borderRadius:12,padding:28,border:'1px solid #334155'}}>
          <div style={{display:'flex',justifyContent:'space-between',alignItems:'center',marginBottom:20}}>
            <div>
              <h2 style={{fontSize:17,fontWeight:600,margin:'0 0 4px'}}>AI Recommendations</h2>
              <p style={{color:'#64748b',fontSize:13,margin:0}}>Generated by Claude</p>
            </div>
            <button onClick={generate} disabled={generating} style={{background:'#6366f1',color:'#fff',border:'none',borderRadius:8,padding:'8px 18px',fontSize:14,cursor:'pointer'}}>
              {generating?'Generating...':'Refresh'}
            </button>
          </div>
          {insight
            ? <div style={{color:'#cbd5e1',fontSize:15,lineHeight:1.8,whiteSpace:'pre-wrap'}}>{insight}</div>
            : <div style={{textAlign:'center',padding:32}}>
                <button onClick={generate} disabled={generating} style={{background:'#6366f1',color:'#fff',border:'none',borderRadius:8,padding:'10px 24px',fontSize:15,cursor:'pointer'}}>
                  {generating?'Generating...':'Generate Recommendations'}
                </button>
              </div>
          }
        </div>
      </div>
    </div>
  )
}