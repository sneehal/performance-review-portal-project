import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom';
import { useAuth } from './context/AuthContext';
import Shell from './components/Shell';
import Login from './pages/Login';
import Register from './pages/Register';
import Profile from './pages/Profile';
import EmployeeDashboard from './pages/EmployeeDashboard';
import Goals from './pages/Goals';
import SelfAssessment from './pages/SelfAssessment';
import CompetencyForm from './pages/CompetencyForm';
import ManagerDashboard from './pages/ManagerDashboard';
import ManagerReview from './pages/ManagerReview';
import HRDashboard from './pages/HRDashboard';
import ReviewCycles from './pages/ReviewCycles';
import AIChat from './pages/AIChat';

function Protected({ roles, children }) {
  const { user, isAuth } = useAuth();
  if (!isAuth) return <Navigate to="/" replace />;
  if (roles && !roles.includes(user?.role)) return <Navigate to="/app" replace />;
  return children;
}
function Landing() {
  const { user, isAuth } = useAuth();
  if (!isAuth) return <Login />;
  return <Navigate to="/app" replace />;
}
export default function App(){
  return <BrowserRouter>
    <Routes>
      <Route path="/" element={<Landing/>}/>
      <Route path="/register" element={<Register/>}/>
      <Route path="/app" element={<Protected><Shell/></Protected>}>
        <Route index element={<RoleHome/>}/>
        <Route path="profile" element={<Protected><Profile/></Protected>}/>
        <Route path="goals" element={<Protected roles={['employee']}><Goals/></Protected>}/>
        <Route path="self-assessment" element={<Protected roles={['employee']}><SelfAssessment/></Protected>}/>
        <Route path="competencies" element={<CompetencyForm/>}/>
        <Route path="manager" element={<Protected roles={['manager','hr_admin']}><ManagerDashboard/></Protected>}/>
        <Route path="manager/review/:reviewId" element={<Protected roles={['manager','hr_admin']}><ManagerReview/></Protected>}/>
        <Route path="hr" element={<Protected roles={['hr_admin']}><HRDashboard/></Protected>}/>
        <Route path="hr/cycles" element={<Protected roles={['hr_admin']}><ReviewCycles/></Protected>}/>
        <Route path="chat" element={<AIChat/>}/>
      </Route>
    </Routes>
  </BrowserRouter>
}
function RoleHome(){
  const { user } = useAuth();
  if(user?.role === 'hr_admin') return <HRDashboard/>;
  if(user?.role === 'manager') return <ManagerDashboard/>;
  return <EmployeeDashboard/>;
}
