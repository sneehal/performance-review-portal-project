import { useEffect, useState } from 'react';
import { cycles } from '../services/portalService';
import { Card, Loader, Badge } from '../components/UI';
import { errMsg } from '../services/api';
export default function ReviewCycles(){
 const [loading,setLoading]=useState(true),[list,setList]=useState([]),[msg,setMsg]=useState(''),[form,setForm]=useState({name:'',start_date:'',end_date:'',self_due_date:'',manager_due_date:''});
 const load=async()=>{setLoading(true); setList(await cycles.list()||[]); setLoading(false)}; useEffect(()=>{load()},[]);
 const submit=async(e)=>{e.preventDefault(); try{await cycles.create(form); setMsg('Review cycle created'); setForm({name:'',start_date:'',end_date:'',self_due_date:'',manager_due_date:''}); load()}catch(e){setMsg(errMsg(e))}};
 const activate=async(id,status)=>{await cycles.update(id,{status}); load()};
 if(loading)return <Loader/>;
 return <div><div className="page-title"><div><h2>Review Cycle Manager</h2><p>Create and manage appraisal cycles.</p></div></div>{msg&&<div className="alert alert-info">{msg}</div>}
 <div className="row g-4"><div className="col-lg-5"><Card><h5>Create Cycle</h5><form onSubmit={submit} className="pretty-form"><label>Name</label><input value={form.name} onChange={e=>setForm({...form,name:e.target.value})} placeholder="Q2 2025 Appraisal" required/><label>Start Date</label><input type="date" value={form.start_date} onChange={e=>setForm({...form,start_date:e.target.value})} required/><label>End Date</label><input type="date" value={form.end_date} onChange={e=>setForm({...form,end_date:e.target.value})} required/><label>Self Due Date</label><input type="date" value={form.self_due_date} onChange={e=>setForm({...form,self_due_date:e.target.value})} required/><label>Manager Due Date</label><input type="date" value={form.manager_due_date} onChange={e=>setForm({...form,manager_due_date:e.target.value})} required/><button className="primary-btn mt-3">Create Cycle</button></form></Card></div>
 <div className="col-lg-7"><Card><h5>All Cycles</h5><table className="table align-middle"><thead><tr><th>Cycle</th><th>Dates</th><th>Status</th><th>Action</th></tr></thead><tbody>{list.map(c=><tr key={c.cycle_id}><td><b>{c.name}</b></td><td><small>{c.start_date} → {c.end_date}</small></td><td><Badge status={c.status}/></td><td><button className="btn btn-sm btn-outline-success me-2" onClick={()=>activate(c.cycle_id,'Active')}>Active</button><button className="btn btn-sm btn-outline-secondary" onClick={()=>activate(c.cycle_id,'Closed')}>Close</button></td></tr>)}</tbody></table></Card></div></div></div>
}
