import React, { useState } from "react";
import { createRoot } from "react-dom/client";
import "./styles.css";

const API = "http://localhost:8000";

const demo = `We want to build a mobile banking application.
Customers should be able to log in securely, view account balances,
add beneficiaries, transfer money, download transaction history and
receive transaction notifications. High-value transactions should
require additional authentication. The application should be secure,
highly available and fast. Requirements may evolve based on feedback.`;

function App() {
  const [description, setDescription] = useState(demo);
  const [name, setName] = useState("Digital Banking Application");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [tab, setTab] = useState("overview");
  const [error, setError] = useState("");

  async function analyze() {
    setLoading(true); setError("");
    try {
      const res = await fetch(`${API}/api/projects/analyze`, {
        method: "POST",
        headers: {"Content-Type":"application/json"},
        body: JSON.stringify({name, domain:"Digital Banking", description, stakeholder:"Product Owner"})
      });
      if (!res.ok) throw new Error(await res.text());
      setResult(await res.json());
      setTab("overview");
    } catch (e) {
      setError("Backend connection failed. Start FastAPI on port 8000.");
    } finally { setLoading(false); }
  }

  async function approve(req, decision) {
    if (!result) return;
    await fetch(`${API}/api/projects/${result.project_id}/approve`, {
      method:"POST",
      headers:{"Content-Type":"application/json"},
      body:JSON.stringify({requirement_id:req.id, decision, comment:"Reviewed in prototype UI"})
    });
    setResult({...result, requirements: result.requirements.map(x =>
      x.id === req.id ? {...x, approval_status: decision} : x
    )});
  }

  const tabs = ["overview","requirements","quality","compliance","security","risk","sdlc","artifacts"];

  return (
    <div className="app">
      <aside>
        <div className="brand"><span>FR</span> FinReqAI</div>
        <p className="muted">Financial Requirements Engineering</p>
        {tabs.map(t => <button key={t} className={tab===t?"nav active":"nav"} onClick={()=>setTab(t)}>
          {t.replace("_"," ").replace(/\b\w/g,c=>c.toUpperCase())}
        </button>)}
        <div className="side-note">
          <b>Prototype mode</b>
          <p>AI outputs are advisory. Regulatory interpretation and SDLC adoption require human approval.</p>
        </div>
      </aside>

      <main>
        <header>
          <div>
            <div className="eyebrow">AGENTIC REQUIREMENTS PLATFORM</div>
            <h1>Turn financial project ideas into traceable requirements.</h1>
            <p className="subtitle">Extraction → quality → compliance → security → risk → SDLC → documentation</p>
          </div>
          <div className="status">● {result ? "Analysis ready" : "Ready"}</div>
        </header>

        <section className="input-card">
          <div className="row">
            <input value={name} onChange={e=>setName(e.target.value)} placeholder="Project name"/>
            <button className="primary" onClick={analyze} disabled={loading}>{loading ? "Analyzing..." : "Analyze Project"}</button>
          </div>
          <textarea value={description} onChange={e=>setDescription(e.target.value)} rows="7"/>
          {error && <div className="error">{error}</div>}
        </section>

        {!result ? (
          <section className="empty">
            <div className="orb">AI</div>
            <h2>Start with a financial project description</h2>
            <p>The demo text above is already loaded. Click Analyze Project to run the complete pipeline.</p>
          </section>
        ) : (
          <section className="content">
            {tab==="overview" && <Overview result={result}/>}
            {tab==="requirements" && <Requirements result={result} approve={approve}/>}
            {tab==="quality" && <Quality result={result}/>}
            {tab==="compliance" && <Compliance result={result}/>}
            {tab==="security" && <Security result={result}/>}
            {tab==="risk" && <Risk result={result}/>}
            {tab==="sdlc" && <SDLC result={result}/>}
            {tab==="artifacts" && <Artifacts result={result}/>}
          </section>
        )}
      </main>
    </div>
  )
}

function Metric({label,value}) {
  return <div className="metric"><span>{label}</span><strong>{value}</strong></div>
}

function Overview({result}) {
  const high = result.risks.filter(x=>["High","Critical"].includes(x.level)).length;
  return <>
    <div className="grid metrics">
      <Metric label="Requirements" value={result.requirements.length}/>
      <Metric label="Quality findings" value={result.quality_findings.length}/>
      <Metric label="Conflicts" value={result.conflicts.length}/>
      <Metric label="High/Critical risk" value={high}/>
    </div>
    <div className="grid two">
      <Card title="SDLC recommendation">
        <div className="big">{result.sdlc.recommendation}</div>
        <p>{result.sdlc.explanation}</p>
        <div className="score-list">{Object.entries(result.sdlc.scores).map(([k,v])=>
          <div className="score" key={k}><span>{k}</span><div><i style={{width:`${v}%`}}></i></div><b>{v}</b></div>
        )}</div>
      </Card>
      <Card title="Clarification queue">
        {result.next_questions.length ? result.next_questions.map((x,i)=><div className="item" key={i}>? {x}</div>) :
          <p className="muted">No clarification questions generated.</p>}
      </Card>
    </div>
  </>
}

function Requirements({result, approve}) {
  return <Card title="Structured requirements">
    <div className="table-wrap"><table><thead><tr><th>ID</th><th>Requirement</th><th>Category</th><th>Risk</th><th>Confidence</th><th>Approval</th></tr></thead>
    <tbody>{result.requirements.map(r=><tr key={r.id}><td><b>{r.id}</b></td><td>{r.statement}<div className="flags">{r.quality_flags?.map(f=><span key={f}>{f}</span>)}</div></td>
    <td>{r.category.map(c=><span className="tag" key={c}>{c}</span>)}</td><td><span className={`risk ${r.risk_level.toLowerCase()}`}>{r.risk_level}</span></td>
    <td>{Math.round(r.confidence*100)}%</td><td>
      <button className="mini ok" onClick={()=>approve(r,"Approved")}>Approve</button>
      <button className="mini no" onClick={()=>approve(r,"Rejected")}>Reject</button>
    </td></tr>)}</tbody></table></div>
  </Card>
}

function Quality({result}) {
  return <Card title="Quality and conflict analysis">
    <h3>Quality findings</h3>
    {result.quality_findings.map((x,i)=><div className="finding" key={i}><b>{x.requirement_id}</b><p>{x.flags.join(" · ")}</p><small>{x.recommendation}</small></div>)}
    <h3>Conflicts</h3>
    {result.conflicts.length ? result.conflicts.map((x,i)=><div className="finding danger" key={i}><b>{x.requirements.join(" ↔ ")}</b><p>{x.reason}</p><small>{x.action}</small></div>) : <p>No conflicts detected.</p>}
  </Card>
}

function Compliance({result}) {
  return <Card title="Compliance evidence">
    {result.compliance.map(x=><div className="finding" key={x.requirement_id}><b>{x.requirement_id}</b><p>{x.status}</p><small>Sources: {x.sources.join(", ") || "None found"} · Confidence: {Math.round(x.confidence*100)}%</small><p>Gap: {x.gap}</p></div>)}
  </Card>
}

function Security({result}) {
  return <Card title="Security analysis">
    {result.security.map(x=><div className="finding" key={x.requirement_id}><b>{x.requirement_id}</b><p>{x.controls.map(c=><span className="tag" key={c}>{c}</span>)}</p><small>{x.status}</small></div>)}
  </Card>
}

function Risk({result}) {
  return <Card title="Risk register">
    <div className="table-wrap"><table><thead><tr><th>Requirement</th><th>Impact</th><th>Probability</th><th>Score</th><th>Level</th></tr></thead>
    <tbody>{result.risks.map(r=><tr key={r.requirement_id}><td>{r.requirement_id}</td><td>{r.impact}</td><td>{r.probability}</td><td>{r.score}</td><td><span className={`risk ${r.level.toLowerCase()}`}>{r.level}</span></td></tr>)}</tbody></table></div>
  </Card>
}

function SDLC({result}) {
  return <><Card title="SDLC decision factors"><div className="factor-grid">{Object.entries(result.sdlc.factors).map(([k,v])=><div className="factor" key={k}><span>{k.replaceAll("_"," ")}</span><b>{v}/5</b></div>)}</div></Card>
  <Card title={`Generated ${result.sdlc.recommendation} workflow`}><div className="workflow">{result.sdlc.workflow.map((p,i)=><div className="phase" key={i}><div className="num">{i+1}</div><div><b>{p.phase}</b><p>{p.activities.join(" · ")}</p><small>Gate: {p.gate}</small></div></div>)}</div></Card></>
}

function Artifacts({result}) {
  const [type,setType]=useState("srs");
  return <Card title="Generated project artifacts">
    <div className="artifact-tabs">{Object.keys(result.artifacts).map(k=><button className={type===k?"active":""} key={k} onClick={()=>setType(k)}>{k.replaceAll("_"," ")}</button>)}</div>
    <pre className="artifact">{result.artifacts[type]}</pre>
  </Card>
}

function Card({title,children}) { return <div className="card"><h2>{title}</h2>{children}</div> }

createRoot(document.getElementById("root")).render(<App/>);
