import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, LineChart, Line } from 'recharts';
import { Download, ShieldCheck, TrendingUp, Users } from 'lucide-react';
import { admin } from '../services/portalService';
import { Card, StatCard, Loader, Badge } from '../components/UI';
export default function HRDashboard(){
 const [loading,setLoading]=useState(true),[ratings,setRatings]=useState([]),[completion,setCompletion]=useState([]);
 useEffect(()=>{(async()=>{setRatings(await admin.ratingsSummary()||[]); setCompletion(await admin.completion()||[]); setLoading(false)})()},[]);
 if(loading)return <Loader/>;
 const total=ratings.reduce((s,x)=>s+x.total_employees,0), promote=ratings.reduce((s,x)=>s+x.promote_count,0), pip=ratings.reduce((s,x)=>s+x.pip_count,0);
 const download=()=>{const token=localStorage.getItem('token'); fetch(admin.exportCsvUrl(),{headers:{Authorization:`Bearer ${token}`}}).then(r=>r.blob()).then(b=>{const a=document.createElement('a'); a.href=URL.createObjectURL(b); a.download='review_export.csv'; a.click();});}
 return <div><div className="page-title"><div><h2>HR Analytics Dashboard</h2><p>Beautiful insight center for review cycles, ratings and completion.</p></div><button className="primary-btn" onClick={download}><Download size={18}/> Export CSV</button></div>
 <div className="stats-grid"><StatCard title="Employees" value={total} sub="Active employees" icon={<Users/>}/><StatCard title="Promote" value={promote} sub="Promotion recommendations" icon={<TrendingUp/>}/><StatCard title="PIP" value={pip} sub="Needs improvement" icon={<ShieldCheck/>}/></div>
 <div className="row g-4 mt-1"><div className="col-lg-7"><Card><h5>Department Average Ratings</h5><ResponsiveContainer height={300}><BarChart data={ratings}><XAxis dataKey="department"/><YAxis/><Tooltip/><Bar dataKey="avg_rating" radius={[10,10,0,0]}/></BarChart></ResponsiveContainer></Card></div><div className="col-lg-5"><Card><h5>Promote vs PIP</h5><ResponsiveContainer height={300}><PieChart><Pie data={[{name:'Promote',value:promote},{name:'PIP',value:pip},{name:'Others',value:Math.max(0,total-promote-pip)}]} dataKey="value" nameKey="name" outerRadius={100} label /></PieChart></ResponsiveContainer></Card></div></div>
 <div className="row g-4 mt-1"><div className="col-lg-6"><Card><h5>Cycle Completion Trend</h5><ResponsiveContainer height={260}><LineChart data={completion}><XAxis dataKey="cycle_name" hide/><YAxis/><Tooltip/><Line type="monotone" dataKey="completion_pct" strokeWidth={3}/></LineChart></ResponsiveContainer></Card></div><div className="col-lg-6"><Card><h5>Completion Table</h5><table className="table align-middle"><thead><tr><th>Cycle</th><th>Status</th><th>Submitted</th><th>%</th></tr></thead><tbody>{completion.map(c=><tr key={c.cycle_id}><td>{c.cycle_name}</td><td><Badge status={c.status}/></td><td>{c.submitted_count}/{c.total_employees}</td><td>{c.completion_pct}%</td></tr>)}</tbody></table></Card></div></div></div>
}
