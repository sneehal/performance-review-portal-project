import { useEffect, useState } from 'react';
import { useAuth } from '../context/AuthContext';
import { errMsg } from '../services/api';

export default function Profile() {
  const { user, refreshProfile } = useAuth();
  const [profile, setProfile] = useState(user);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    let mounted = true;
    (async () => {
      setLoading(true);
      setError('');
      try {
        const data = await refreshProfile();
        if (mounted) setProfile(data);
      } catch (err) {
        if (mounted) setError(errMsg(err));
      } finally {
        if (mounted) setLoading(false);
      }
    })();
    return () => {
      mounted = false;
    };
  }, []);

  return (
    <div>
      <div className="page-title">
        <div>
          <h2>Profile</h2>
          <p>View your account details and assigned role.</p>
        </div>
      </div>
      {error && <div className="alert alert-danger">{error}</div>}
      <div className="card p-4">
        {loading ? (
          <div>Loading profile...</div>
        ) : (
          <div className="profile-grid">
            <div><strong>Name</strong><p>{profile?.name || '-'}</p></div>
            <div><strong>Email</strong><p>{profile?.email || '-'}</p></div>
            <div><strong>Role</strong><p>{profile?.role || '-'}</p></div>
            <div><strong>Department</strong><p>{profile?.department || '-'}</p></div>
            <div><strong>Manager ID</strong><p>{profile?.manager_id ?? '-'}</p></div>
            <div><strong>User ID</strong><p>{profile?.user_id ?? '-'}</p></div>
          </div>
        )}
      </div>
    </div>
  );
}
