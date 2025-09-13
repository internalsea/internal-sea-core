import React from 'react';
import { BrowserRouter as Router, Routes, Route, useLocation } from 'react-router-dom';
import './App.css';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Items from './pages/Items';
import Settings from './pages/Settings';
import { AuthProvider } from './contexts/AuthContext';

// Component to conditionally render navbar
const AppContent: React.FC = () => {
  const location = useLocation();
  const isLoginPage = location.pathname === '/' || location.pathname === '/login';
  
  return (
    <div className="App">
      {!isLoginPage && <Navbar />}
      <main className={`main-content ${isLoginPage ? 'login-page-main' : ''}`}>
        <Routes>
          <Route path="/" element={<Login />} />
          <Route path="/home" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/items" element={<Items />} />
          <Route path="/settings" element={<Settings />} />
        </Routes>
      </main>
    </div>
  );
};

function App() {
  return (
    <AuthProvider>
      <Router>
        <AppContent />
      </Router>
    </AuthProvider>
  );
}

export default App; 