import { useEffect, useState } from 'react';
import { cycles, goals } from '../services/portalService';
import { Card, Loader } from '../components/UI';
import { errMsg } from '../services/api';

export default function Goals(){
 const [loading,setLoading]=useState(true),[cycleList,setCycles]=useState([]),[goalList,setGoals]=useState([]),[msg,setMsg]=useState(''),[form,setForm]=useState({cycle_id:'',title:'',description:'',weight:'',target:''});
 const load=async()=>{setLoading(true); const c=await cycles.list(); setCycles(c||[]); const active=(c||[]).find(x=>x.status==='Active')||c?.[0]; setForm(f=>({...f,cycle_id:active?.cycle_id||''})); setGoals(await goals.mine(active?.cycle_id)||[]); setLoading(false)};
 useEffect(()=>{load()},[]);
 const submit=async(e)=>{e.preventDefault(); setMsg(''); try{await goals.create({...form, weight:+form.weight}); setForm({...form,title:'',description:'',weight:'',target:''}); await load(); setMsg('Goal created successfully')}catch(err){setMsg(errMsg(err))}};
 const addAchievement=async(id)=>{const achievement=prompt('Enter achievement'); if(!achievement)return; await goals.achievement(id,achievement); await load();};
 if(loading) return <Loader/>;
 return <div><div className="page-title"><div><h2>My Goals</h2><p>Create measurable goals and record achievements.</p></div></div>
  {msg && <div className="alert alert-info">{msg}</div>}
  <div className="row g-4"><div className="col-lg-5"><Card><h5>Add New Goal</h5><form onSubmit={submit} className="pretty-form">
    <label>Cycle</label><select value={form.cycle_id} onChange={e=>setForm({...form,cycle_id:e.target.value})} required>{cycleList.map(c=><option key={c.cycle_id} value={c.cycle_id}>{c.name} ({c.status})</option>)}</select>
    <label>Goal Title</label><input value={form.title} onChange={e=>setForm({...form,title:e.target.value})} required placeholder="Complete React dashboard" />
    <label>Description</label><textarea value={form.description} onChange={e=>setForm({...form,description:e.target.value})} placeholder="Detailed goal description" />
    <div className="row"><div className="col"><label>Weight %</label><input type="number" value={form.weight} onChange={e=>setForm({...form,weight:e.target.value})} required /></div></div>
    <label>Target</label><input value={form.target} onChange={e=>setForm({...form,target:e.target.value})} placeholder="Deliver by March 31" />
    <button className="primary-btn mt-3">Save Goal</button>
  </form></Card></div><div className="col-lg-7"><Card><h5>Goal List</h5><div className="table-responsive"><table className="table align-middle"><thead><tr><th>Goal</th><th>Weight</th><th>Target</th><th></th></tr></thead><tbody>{goalList.map(g=><tr key={g.goal_id}><td><b>{g.title}</b><br/><small>{g.achievement||g.description}</small></td><td>{g.weight}%</td><td>{g.target}</td><td><button className="btn btn-sm btn-outline-primary" onClick={()=>addAchievement(g.goal_id)}>Achievement</button></td></tr>)}</tbody></table></div></Card></div></div>
 </div>
}
