import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import Layout from './components/Layout';
import AdminDashboard from './components/Admin/AdminDashboard';
import PromptTemplates from './components/Admin/PromptTemplates';
import UserDashboard from './components/User/UserDashboard';
import HomePage from "./components/HomePage";
import UnauthorizedPage from "./UnauthorizedPage";
import withAuth from './withAuth';

const AdminDashboardWithAuth = withAuth(AdminDashboard, ['Admin']);
const UserDashboardWithAuth = withAuth(UserDashboard, ['User']);
const PromptTemplatesWithAuth = withAuth(PromptTemplates, ['Admin']);

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Layout />}>
            <Route path="/" element={<HomePage />} />
            <Route path="admin" element={<AdminDashboardWithAuth />} />
            <Route path="admin/prompt-templates" element={<PromptTemplatesWithAuth />} />
            <Route path="user" element={<UserDashboardWithAuth />} />
            <Route path="login" element={<HomePage />} />
            <Route path="unauthorized" element={<UnauthorizedPage />} />
          </Route>
        </Routes>
      </Router>
    </AuthProvider>
  );
};

export default App;