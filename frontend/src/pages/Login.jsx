import { useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { Link, Navigate } from 'react-router-dom';
import { errMsg } from '../services/api';
import { Bot, LockKeyhole, Mail } from 'lucide-react';

export default function Login(){
  const { signIn, isAuth } = useAuth();
  const [email,setEmail]=useState(''), [password,setPassword]=useState(''), [error,setError]=useState(''), [loading,setLoading]=useState(false);
  if(isAuth) return <Navigate to="/app"/>;
  const submit=async(e)=>{e.preventDefault(); setLoading(true); setError(''); try{await signIn(email,password)}catch(err){setError(errMsg(err))}finally{setLoading(false)}};
  return <div className="login-page">
    <div className="login-art">
      <div className="hero-card"><Bot size={48}/><h1>AI-Powered Performance Review Portal</h1><p>Goals, reviews, competencies, HR analytics and smart feedback assistance in one modern platform.</p></div>
    </div>
    <form className="login-card" onSubmit={submit}>
      <h2>Welcome back</h2><p>Login with your employee, manager or HR account.</p>
      {error && <div className="alert alert-danger py-2">{error}</div>}
      <label>Email</label><div className="input-icon"><Mail size={18}/><input type="email" value={email} onChange={e=>setEmail(e.target.value)} placeholder="alice@company.com" required/></div>
      <label>Password</label><div className="input-icon"><LockKeyhole size={18}/><input type="password" value={password} onChange={e=>setPassword(e.target.value)} placeholder="Password" required/></div>
      <button className="primary-btn" disabled={loading}>{loading?'Signing in...':'Login to Dashboard'}</button>
      <div className="mt-3 text-center">
        <small>Don't have an account? <Link to="/register">Register here</Link></small>
      </div>
      {/* <small className="text-muted">Backend: localhost:8000 • AI: localhost:5000</small> */}
    </form>
  </div>
}
