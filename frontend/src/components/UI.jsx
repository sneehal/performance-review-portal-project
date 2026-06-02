export function Card({children, className=''}){return <div className={`glass-card ${className}`}>{children}</div>}
export function StatCard({title,value,icon,sub}){return <div className="stat-card"><div><p>{title}</p><h3>{value}</h3><small>{sub}</small></div><div className="stat-icon">{icon}</div></div>}
export function Loader(){return <div className="p-4 text-center"><div className="spinner-border text-primary"/></div>}
export function Empty({text='No data found'}){return <div className="empty-state">{text}</div>}
export function Badge({status}){const s=(status||'').toLowerCase(); return <span className={`status-badge ${s}`}>{status || 'N/A'}</span>}
