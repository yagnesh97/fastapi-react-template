import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { AuthProvider } from './context/AuthProvider';
import Dashboard from './components/Dashboard/Dashboard';
import Login from './components/Login/Login';

const App: React.FC = () => (
  <AuthProvider>
    <Router>
      <Routes>
        <Route path="" element={<Login />} />
        <Route path="dashboard" element={<Dashboard />} />
      </Routes>
    </Router>
  </AuthProvider>
);

export default App;
