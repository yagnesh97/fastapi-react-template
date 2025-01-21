import React from "react";
import { useNavigate } from "react-router-dom";
import useAuth from "../../context/useAuth";

const Dashboard = () => {
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const handleLogout = async (e: React.FormEvent) => {
    e.preventDefault();
    logout();
    navigate("/");
  };

  if (!user) {
    return <p>Loading...</p>;
  }

  return (
    <div className="container dashboard">
      <h1>Welcome, {user.first_name}!</h1>
      <p>Email: {user.email}</p>
      <p>Username: {user.username}</p>
      <button onClick={handleLogout}>Logout</button>
    </div>
  );
};

export default Dashboard;
