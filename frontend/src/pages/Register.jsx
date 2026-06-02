import { useState } from 'react';
import { Link, useNavigate, Navigate } from 'react-router-dom';
import { User, Mail, Lock, ShieldCheck, Briefcase, Users } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { errMsg } from '../services/api';

export default function Register() {
  const { isAuth, register } = useAuth();
  const navigate = useNavigate();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [role, setRole] = useState('employee');
  const [department, setDepartment] = useState('Engineering');
  const [managerId, setManagerId] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');

  if (isAuth) return <Navigate to="/app" replace />;

  const submit = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    try {
      const payload = {
        name,
        email,
        password,
        role,
        department,
        manager_id: managerId ? Number(managerId) : null
      };
      await register(payload);
      setSuccess('Registration complete. Redirecting to login...');
      setTimeout(() => navigate('/'), 900);
    } catch (err) {
      setError(errMsg(err));
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="login-page">
      <div className="login-art">
        <div className="hero-card">
          <h1>Join ReviewPro AI</h1>
          <p>Register your employee, manager or HR account and start using the performance review portal.</p>
        </div>
      </div>
      <form className="login-card" onSubmit={submit}>
        <h2>Create Account</h2>
        <p className="text-muted">Fill in your details to register and then login.</p>
        {error && <div className="alert alert-danger py-2">{error}</div>}
        {success && <div className="alert alert-success py-2">{success}</div>}

        <div className="input-icon"><User size={18} /><input value={name} onChange={(e) => setName(e.target.value)} placeholder="Full name" required /></div>
        <div className="input-icon"><Mail size={18} /><input type="email" value={email} onChange={(e) => setEmail(e.target.value)} placeholder="john.emp@company.com" required /></div>
        <div className="input-icon"><Lock size={18} /><input type="password" value={password} onChange={(e) => setPassword(e.target.value)} placeholder="Strong password" required /></div>
        <div className="input-icon"><ShieldCheck size={18} /><select value={role} onChange={(e) => setRole(e.target.value)}>
          <option value="employee">Employee</option>
          <option value="manager">Manager</option>
          <option value="hr_admin">HR Admin</option>
        </select></div>
        <div className="input-icon"><Briefcase size={18} /><input value={department} onChange={(e) => setDepartment(e.target.value)} placeholder="Engineering" required /></div>
        <div className="input-icon"><Users size={18} /><input type="number" value={managerId} onChange={(e) => setManagerId(e.target.value)} placeholder="Manager ID" required /></div>

        <button className="primary-btn" style={{ width: '100%' }} disabled={loading}>{loading ? 'Registering...' : 'Register'}</button>
        <div style={{ marginTop: '18px', textAlign: 'center' }}>
          <span className="text-muted" style={{ marginRight: '8px' }}>Already have an account?</span>
          <Link to="/" style={{ color: 'var(--primary)', fontWeight: 700, textDecoration: 'none' }}>Login here</Link>
        </div>
      </form>
    </div>
  );
}
