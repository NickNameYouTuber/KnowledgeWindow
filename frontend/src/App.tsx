import React, { Suspense, lazy } from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import { AuthProvider } from './AuthContext';
import Layout from './components/Layout';
import HomePage from "./components/HomePage";
import UnauthorizedPage from "./UnauthorizedPage";
import withAuth from "./withAuth";

const AdminDashboard = lazy(() => import('./components/Admin/AdminDashboard'));
const PromptTemplates = lazy(() => import('./components/Admin/PromptTemplates'));
const UserDashboard = lazy(() => import('./components/User/UserDashboard'));

const AdminDashboardWithAuth = withAuth(AdminDashboard, ['Admin']);
const UserDashboardWithAuth = withAuth(UserDashboard, ['User']);
const PromptTemplatesWithAuth = withAuth(PromptTemplates, ['Admin']);

const App: React.FC = () => {
  return (
    <AuthProvider>
      <Router>
        <Suspense fallback={<div>Loading...</div>}>
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
        </Suspense>
      </Router>
    </AuthProvider>
  );
};

export default App;