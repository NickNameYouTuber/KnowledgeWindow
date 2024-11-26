import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Layout from './components/Layout';
import AdminDashboard from './components/Admin/AdminDashboard';
import PromptTemplates from './components/Admin/PromptTemplates';
import UserDashboard from './components/User/UserDashboard';
import HomePage from "./components/HomePage";

const App: React.FC = () => {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Layout />}>
            <Route path="/" element={<HomePage />} />
          <Route path="admin" element={<AdminDashboard />} />
          <Route path="admin/prompt-templates" element={<PromptTemplates />} />
          <Route path="user" element={<UserDashboard />} />
        </Route>
      </Routes>
    </Router>
  );
};

export default App;