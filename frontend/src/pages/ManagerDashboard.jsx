import { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie } from 'recharts';
import { Users, Clock, Award } from 'lucide-react';
import { manager } from '../services/portalService';
import { Card, StatCard, Loader, Badge } from '../components/UI';
export default function ManagerDashboard(){
 const [loading,setLoading]=useState(true),[pending,setPending]=useState([]),[summary,setSummary]=useState([]);
 useEffect(()=>{(async()=>{setPending(await manager.pending()||[]); setSummary(await manager.summary()||[]); setLoading(false)})()},[]);
 if(loading)return <Loader/>;
 const avg=(summary.reduce((s,x)=>s+(+x.overall_rating||0),0)/(summary.filter(x=>x.overall_rating).length||1)).toFixed(1);
 return <div><div className="page-title"><div><h2>Manager Dashboard</h2><p>Review your team performance and complete pending evaluations.</p></div></div>
 <div className="stats-grid"><StatCard title="Team Members" value={summary.length} sub="Direct reports" icon={<Users/>}/><StatCard title="Pending Reviews" value={pending.length} sub="Awaiting your action" icon={<Clock/>}/><StatCard title="Average Rating" value={avg} sub="Team average" icon={<Award/>}/></div>
 <div className="row g-4 mt-1"><div className="col-lg-7"><Card><h5>Team Ratings</h5><ResponsiveContainer height={280}><BarChart data={summary}><XAxis dataKey="name" hide/><YAxis/><Tooltip/><Bar dataKey="overall_rating" radius={[10,10,0,0]}/></BarChart></ResponsiveContainer></Card></div><div className="col-lg-5"><Card><h5>Recommendation Split</h5><ResponsiveContainer height={280}><PieChart><Pie data={Object.values(summary.reduce((a,x)=>{const k=x.recommendation||'Pending'; a[k]=a[k]||{name:k,value:0}; a[k].value++; return a},{}))} dataKey="value" nameKey="name" outerRadius={95} label /></PieChart></ResponsiveContainer></Card></div></div>
 <Card className="mt-4"><h5>Pending Reviews</h5><div className="table-responsive"><table className="table align-middle"><thead><tr><th>Employee</th><th>Department</th><th>Cycle</th><th>Status</th><th></th></tr></thead><tbody>{pending.map(p=><tr key={p.review_id}><td><b>{p.employee_name}</b></td><td>{p.department}</td><td>{p.cycle_name}</td><td><Badge status={p.status}/></td><td><Link className="btn btn-sm btn-primary" to={`/app/manager/review/${p.review_id}`}>Review</Link></td></tr>)}</tbody></table></div></Card></div>
}
