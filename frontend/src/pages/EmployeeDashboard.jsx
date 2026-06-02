import { useEffect, useState } from 'react';
import { BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { ClipboardCheck, Goal, Star, TrendingUp } from 'lucide-react';
import { cycles, goals } from '../services/portalService';
import { Card, StatCard, Loader, Badge } from '../components/UI';

export default function EmployeeDashboard(){
 const [loading,setLoading]=useState(true), [cycleList,setCycles]=useState([]), [goalList,setGoals]=useState([]);
 useEffect(()=>{(async()=>{try{const c=await cycles.list(); setCycles(c||[]); const active=(c||[]).find(x=>x.status==='Active')||c?.[0]; const g=await goals.mine(active?.cycle_id); setGoals(g||[])}finally{setLoading(false)}})()},[]);
 if(loading) return <Loader/>;
 const active=cycleList.find(c=>c.status==='Active')||cycleList[0]; const totalWeight=goalList.reduce((s,g)=>s+(+g.weight||0),0);
 return <div>
  <div className="page-title"><div><h2>Employee Dashboard</h2><p>Track goals, assessments and review readiness.</p></div><Badge status={active?.status}/></div>
  <div className="stats-grid">
    <StatCard title="Active Cycle" value={active?.name||'No cycle'} sub="Current appraisal window" icon={<ClipboardCheck/>}/>
    <StatCard title="Goals" value={goalList.length} sub="Created by you" icon={<Goal/>}/>
    <StatCard title="Weight Assigned" value={`${totalWeight}%`} sub="Goal weight total" icon={<TrendingUp/>}/>
    <StatCard title="AI Coach" value="Ready" sub="Feedback assistant" icon={<Star/>}/>
  </div>
  <div className="row g-4 mt-1">
    <div className="col-lg-8"><Card><h5>Goal Weight Distribution</h5><ResponsiveContainer width="100%" height={280}><BarChart data={goalList}><XAxis dataKey="title" hide/><YAxis/><Tooltip/><Bar dataKey="weight" radius={[10,10,0,0]}/></BarChart></ResponsiveContainer></Card></div>
    <div className="col-lg-4"><Card><h5>Readiness</h5><ResponsiveContainer width="100%" height={280}><PieChart><Pie data={[{name:'Assigned',value:totalWeight},{name:'Remaining',value:Math.max(0,100-totalWeight)}]} dataKey="value" innerRadius={65} outerRadius={95}><Cell/><Cell/></Pie></PieChart></ResponsiveContainer><p className="text-center fw-bold">{totalWeight}% completed</p></Card></div>
  </div>
  <Card className="mt-4"><h5>My Goals</h5><div className="table-responsive"><table className="table align-middle"><thead><tr><th>Goal</th><th>Weight</th><th>Target</th><th>Achievement</th></tr></thead><tbody>{goalList.map(g=><tr key={g.goal_id}><td><b>{g.title}</b><br/><small>{g.description}</small></td><td>{g.weight}%</td><td>{g.target}</td><td>{g.achievement || 'Not added'}</td></tr>)}</tbody></table></div></Card>
 </div>
}
