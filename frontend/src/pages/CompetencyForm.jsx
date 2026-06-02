import { useEffect, useState } from 'react';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer } from 'recharts';
import { competencies } from '../services/portalService';
import { Card, Loader } from '../components/UI';

export default function CompetencyForm(){
 const [loading,setLoading]=useState(true),[list,setList]=useState([]),[ratings,setRatings]=useState({}),[reviewId,setReviewId]=useState(''),[msg,setMsg]=useState('');
 useEffect(()=>{(async()=>{setList(await competencies.list()||[]); setLoading(false)})()},[]);
 if(loading)return <Loader/>;
 const chart=list.map(c=>({name:c.name, score:+(ratings[c.comp_id]?.score||3)}));
 const submit=async()=>{await competencies.submit({review_id:+reviewId, ratings:list.map(c=>({comp_id:c.comp_id,score:+(ratings[c.comp_id]?.score||3),feedback_comment:ratings[c.comp_id]?.feedback_comment||''}))}); setMsg('Competency ratings saved')};
 return <div><div className="page-title"><div><h2>Competency Assessment</h2><p>Rate communication, technical skills, teamwork and more.</p></div></div>{msg&&<div className="alert alert-success">{msg}</div>}
 <div className="row g-4"><div className="col-lg-7"><Card><label>Review ID</label><input className="form-control soft-input mb-3" value={reviewId} onChange={e=>setReviewId(e.target.value)} placeholder="Enter review_id"/>{list.map(c=><div className="competency-line" key={c.comp_id}><div><b>{c.name}</b><p>{c.description}</p></div><select value={ratings[c.comp_id]?.score||3} onChange={e=>setRatings(r=>({...r,[c.comp_id]:{...r[c.comp_id],score:e.target.value}}))}>{[1,2,3,4,5].map(n=><option key={n}>{n}</option>)}</select><input placeholder="Comment" onChange={e=>setRatings(r=>({...r,[c.comp_id]:{...r[c.comp_id],feedback_comment:e.target.value}}))}/></div>)}<button className="primary-btn mt-3" onClick={submit}>Submit Ratings</button></Card></div>
 <div className="col-lg-5"><Card><h5>Skill Radar</h5><ResponsiveContainer height={350}><RadarChart data={chart}><PolarGrid/><PolarAngleAxis dataKey="name"/><PolarRadiusAxis domain={[0,5]}/><Radar dataKey="score" fillOpacity={0.45}/></RadarChart></ResponsiveContainer></Card></div></div></div>
}
