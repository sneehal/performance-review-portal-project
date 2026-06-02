import { useEffect, useState } from 'react';
import { cycles, goals, reviews } from '../services/portalService';
import { Card, Loader } from '../components/UI';
import { errMsg } from '../services/api';

export default function SelfAssessment(){
 const [loading,setLoading]=useState(true),[cycle,setCycle]=useState(null),[goalList,setGoals]=useState([]),[ratings,setRatings]=useState({}),[overall,setOverall]=useState(''),[reviewId,setReviewId]=useState(null),[msg,setMsg]=useState('');
 useEffect(()=>{(async()=>{const c=await cycles.list(); const active=(c||[]).find(x=>x.status==='Active')||c?.[0]; setCycle(active); const g=await goals.mine(active?.cycle_id); setGoals(g||[]);
      try{
        const existing = await reviews.mine(active?.cycle_id);
        setReviewId(existing.review_id);
        setOverall(existing.overall_comment || '');
        const loadedRatings = {};
        (existing.ratings||[]).forEach(r=>{loadedRatings[r.goal_id] = {score:r.score, comment:r.self_comment || r.comment || ''}});
        setRatings(loadedRatings);
      }catch(_){/* no draft yet */}
      setLoading(false)})()},[]);
 const setRate=(id,key,val)=>setRatings(r=>({...r,[id]:{...r[id],[key]:val}}));
 const save=async()=>{setMsg(''); try{const payload={cycle_id:cycle.cycle_id, overall_comment:overall, ratings:goalList.map(g=>({goal_id:g.goal_id,score:+(ratings[g.goal_id]?.score||3),comment:ratings[g.goal_id]?.comment||''}))}; const res=await reviews.selfAssessment(payload); setReviewId(res.review_id); setMsg('Draft saved. Now submit it to manager.')}catch(e){setMsg(errMsg(e))}};
 const submit=async()=>{try{await reviews.submit(reviewId); setMsg('Review submitted successfully')}catch(e){setMsg(errMsg(e))}};
 if(loading)return <Loader/>;
 return <div><div className="page-title"><div><h2>Self Assessment</h2><p>Rate your goals and write professional self-reflection.</p></div></div>{msg&&<div className="alert alert-info">{msg}</div>}
  <Card><h5>{cycle?.name}</h5>{goalList.map(g=><div className="rating-row" key={g.goal_id}><div><b>{g.title}</b><p>{g.description}</p><small>Weight: {g.weight}% • Target: {g.target}</small></div><div><label>Score</label><select value={ratings[g.goal_id]?.score||3} onChange={e=>setRate(g.goal_id,'score',e.target.value)}>{[1,2,3,4,5].map(n=><option key={n}>{n}</option>)}</select></div><textarea placeholder="Your comment" value={ratings[g.goal_id]?.comment||''} onChange={e=>setRate(g.goal_id,'comment',e.target.value)} /></div>)}
  <label className="mt-3">Overall Reflection</label><textarea className="form-control soft-input" rows="5" value={overall} onChange={e=>setOverall(e.target.value)} placeholder="Describe your achievements, challenges and learnings..." />
  <div className="d-flex gap-2 mt-3"><button className="primary-btn" onClick={save}>Save Draft</button><button className="btn btn-success rounded-pill px-4" disabled={!reviewId} onClick={submit}>Submit to Manager</button></div></Card>
 </div>
}
