import { createContext, useState, ReactNode } from 'react';
import { fetchUserDetails } from '../services/authService';

interface User {
  username: string;
  email: string;
  first_name: string;
  last_name: string;
  admin: boolean;
}

interface AuthContextType {
  user: User | null;
  login: (token: string) => void;
  logout: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export const AuthProvider = ({ children }: { children: ReactNode }) => {
  const [user, setUser] = useState<User | null>(null);

  const login = async (token: string) => {
    localStorage.setItem('access_token', token);
    try {
      const userDetails = await fetchUserDetails();
      setUser(userDetails);
    } catch (err) {
      console.error('Failed to fetch user details:', err);
      logout();
    }
  };

  const logout = () => {
    localStorage.removeItem('access_token');
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};

export default AuthContext;
