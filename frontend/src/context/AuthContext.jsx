import { createContext, useContext, useMemo, useState } from 'react';
import * as authService from '../services/authService';

const AuthContext = createContext(null);
export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => JSON.parse(localStorage.getItem('user') || 'null'));
  const [token, setToken] = useState(() => localStorage.getItem('token'));

  const signIn = async (email, password) => {
    const data = await authService.login({ email, password });
    localStorage.setItem('token', data.access_token);
    setToken(data.access_token);

    const profile = await authService.me();
    localStorage.setItem('user', JSON.stringify(profile));
    setUser(profile);

    return profile;
  };

  const register = async (payload) => {
    return await authService.register(payload);
  };

  const refreshProfile = async () => {
    const profile = await authService.me();
    localStorage.setItem('user', JSON.stringify(profile));
    setUser(profile);
    return profile;
  };

  const signOut = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user');
    setToken(null);
    setUser(null);
  };

  const value = useMemo(
    () => ({ user, token, signIn, register, refreshProfile, signOut, isAuth: !!token }),
    [user, token]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
export const useAuth = () => useContext(AuthContext);
