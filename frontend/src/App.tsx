import React, { useEffect, useState } from 'react';
import { api } from './api';
import ModelSelector from './components/ModelSelector';
import RunForm from './components/RunForm';
import RunStatus from './components/RunStatus';
import ResultsTable from './components/ResultsTable';
// Optional MSAL gate
// import LoginGate from './components/LoginGate';


type Model = { id: string; name: string; params: Record<string, any> }


export default function App(){
const [models, setModels] = useState<Model[]>([])
const [selected, setSelected] = useState('')
const [error, setError] = useState('')
const [runId, setRunId] = useState('')
const [ready, setReady] = useState(false)


useEffect(()=>{ (async()=>{
try{
const r = await api.get('/api/models')
setModels(r.data.models || [])
}catch(e:any){ setError(e.message || 'Failed to load models') }
})() },[])


const shell = (
<>
<div className="topbar">
<div className="topbar-inner">
<div className="brand"><span className="dot"/> Model Runner Dashboard</div>
<div className="sub">Plan • Run • Inspect</div>
</div>
</div>


<div className="container">
{error && <div className="error-banner" style={{marginBottom:14}}>{error}</div>}


<div className="grid">
<div className="col-4">
<div className="card">
<div className="card-header">
<div className="card-title">Model & Parameters</div>
</div>
<div className="card-body">
<ModelSelector models={models} value={selected} onChange={setSelected}/>
<RunForm disabled={!selected} onSubmit={async (inputs)=>{
setError('');setReady(false);
try{
const r = await api.post('/api/runs', { model_id: selected, inputs })
setRunId(r.data.run_id)
}catch(e:any){ setError(e.message || 'Run failed to start') }
}}/>
</div>
</div>
</div>


<div className="col-8">
<div className="card">
<div className="card-header">
<div className="card-title">Execution & Results</div>
{runId && <button className="btn ghost" onClick={()=>{setRunId('');setReady(false)}}>Reset</button>}
</div>
<div className="card-body">
{runId ? (
<>
<RunStatus runId={runId} onDone={(ok)=>setReady(ok)}/>
<ResultsTable key={runId} runId={runId} active={ready}/>
</>
) : (
<div style={{color:'var(--muted)'}}>Start a run to see live status and results.</div>
)}
</div>
</div>
</div>
</div>
</div>
</>
)


// If user want to enforce login later:
// return <LoginGate>{shell}</LoginGate>
return shell
}