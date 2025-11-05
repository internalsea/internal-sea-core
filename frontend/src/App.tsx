import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import Session from './pages/Session';
import './App.css';

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Session />} />
        <Route path="/session" element={<Session />} />
      </Routes>
    </Router>
  );
}

export default App;

