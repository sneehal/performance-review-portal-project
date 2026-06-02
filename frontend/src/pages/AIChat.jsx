import { useState } from 'react';
import { Bot, Send, Sparkles } from 'lucide-react';
import { chatbot } from '../services/portalService';
import { useAuth } from '../context/AuthContext';
import { Card } from '../components/UI';
const prompts=['Help me write a self-assessment for my React dashboard project','Suggest constructive manager feedback for missed deadlines','What does a rating of 5 mean?','How are goals weighted?'];
export default function AIChat(){
 const [q,setQ]=useState(''),[answer,setAnswer]=useState(''),[loading,setLoading]=useState(false); const {user}=useAuth();
 const ask=async(text=q)=>{if(!text.trim())return; setQ(text); setLoading(true); try{const res=await chatbot.ask(text,user?.user_id); setAnswer(res.answer)}catch(e){setAnswer('Could not reach AI service. Start Flask service on http://localhost:5000')}finally{setLoading(false)}};
 return <div><div className="page-title"><div><h2>AI Review Coach</h2><p>Generate polished feedback and get HR policy answers instantly.</p></div></div>
 <div className="row g-4"><div className="col-lg-5"><Card><div className="ai-hero"><Bot size={52}/><h3>Ask ReviewPro AI</h3><p>Use it for self-assessment, manager feedback, rating policies and writing improvement.</p></div>{prompts.map(p=><button key={p} className="prompt-chip" onClick={()=>ask(p)}><Sparkles size={16}/>{p}</button>)}</Card></div><div className="col-lg-7"><Card><label>Your Question</label><textarea className="form-control soft-input" rows="5" value={q} onChange={e=>setQ(e.target.value)} placeholder="Ask anything about review writing or HR policy..."/><button className="primary-btn mt-3" onClick={()=>ask()} disabled={loading}><Send size={18}/>{loading?'Generating...':'Ask AI'}</button>{answer&&<div className="ai-answer"><h5>AI Answer</h5><pre>{answer}</pre></div>}</Card></div></div></div>
}
