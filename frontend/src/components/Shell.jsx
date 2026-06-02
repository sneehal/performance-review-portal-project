import { Outlet, NavLink } from 'react-router-dom';
import { BarChart3, Bot, ClipboardList, Gauge, Goal, LogOut, Menu, ShieldCheck, Star, Users } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import ChatWidget from './ChatWidget';

const item = (to, icon, label) => <NavLink to={to} className={({isActive})=>`side-link ${isActive?'active':''}`}>{icon}<span>{label}</span></NavLink>;
export default function Shell(){
  const { user, signOut } = useAuth();
  return <div className="app-shell">
    <aside className="sidebar">
      <div className="brand"><div className="brand-icon"><Gauge size={24}/></div><div><b>ReviewPro AI</b><small>Performance Portal</small></div></div>
      <nav>
        {item('/app', <BarChart3 size={18}/>, 'Dashboard')}
        {item('/app/profile', <Users size={18}/>, 'Profile')}
        {user?.role==='employee' && item('/app/goals', <Goal size={18}/>, 'My Goals')}
        {user?.role==='employee' && item('/app/self-assessment', <ClipboardList size={18}/>, 'Self Assessment')}
        {(user?.role==='employee'||user?.role==='manager') && item('/app/competencies', <Star size={18}/>, 'Competencies')}
        {(user?.role==='manager'||user?.role==='hr_admin') && item('/app/manager', <Users size={18}/>, 'Manager')}
        {user?.role==='hr_admin' && item('/app/hr', <ShieldCheck size={18}/>, 'HR Analytics')}
        {user?.role==='hr_admin' && item('/app/hr/cycles', <ClipboardList size={18}/>, 'Review Cycles')}
        {item('/app/chat', <Bot size={18}/>, 'AI Coach')}
      </nav>
      <button className="logout" onClick={signOut}><LogOut size={18}/> Logout</button>
    </aside>
    <main className="main">
      <header className="topbar">
        <div><h5 className="m-0">Welcome, {user?.name || 'User'}</h5><small>{user?.role} • {user?.department || 'Performance Team'}</small></div>
        <div className="avatar">{(user?.name||'U').charAt(0)}</div>
      </header>
      <section className="content"><Outlet/></section>
      <ChatWidget />
    </main>
  </div>
}
