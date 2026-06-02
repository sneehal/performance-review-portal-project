import { useState } from 'react';
import { Bot, Send, X } from 'lucide-react';
import { chatbot } from '../services/portalService';
import { useAuth } from '../context/AuthContext';

export default function ChatWidget(){
  const [open,setOpen]=useState(false), [q,setQ]=useState(''), [msgs,setMsgs]=useState([{from:'ai',text:'Hi! I can help you write self-assessments, manager feedback, and explain review policies.'}]);
  const { user } = useAuth();
  const ask=async()=>{ if(!q.trim()) return; const question=q; setQ(''); setMsgs(m=>[...m,{from:'me',text:question}]); try{ const res=await chatbot.ask(question,user?.user_id); setMsgs(m=>[...m,{from:'ai',text:res.answer}]); }catch(e){setMsgs(m=>[...m,{from:'ai',text:'AI service is not reachable. Please check Flask service on port 5000.'}]);}};
  return <>
    <button className="chat-fab" onClick={()=>setOpen(true)}><Bot size={24}/></button>
    {open && <div className="chat-panel">
      <div className="chat-head"><b>AI Review Coach</b><button onClick={()=>setOpen(false)}><X size={18}/></button></div>
      <div className="chat-body">{msgs.map((m,i)=><div key={i} className={`msg ${m.from}`}>{m.text}</div>)}</div>
      <div className="chat-input"><input value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>e.key==='Enter'&&ask()} placeholder="Ask AI..."/><button onClick={ask}><Send size={18}/></button></div>
    </div>}
  </>
}
