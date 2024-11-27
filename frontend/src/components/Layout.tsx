import React from 'react';
import { Link, Outlet } from 'react-router-dom';
import { Home, Settings, User, LayoutDashboard, Moon, Sun } from 'lucide-react';
import { useAuth } from '../AuthContext';
import { useTheme } from '../ThemeContext';

const Layout = () => {
  const { isAuthenticated, userRole, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 flex">
      {/* Sidebar */}
      <div className="w-64 bg-white dark:bg-gray-800 border-r border-gray-200 dark:border-gray-700 py-6 px-4 hidden md:flex flex-col">
        <div className="mb-8 md:flex flex-row items-center">
          <img src="/logo512.png" alt="Logo" className="h-12 w-auto" />
          {isAuthenticated ? (
            <h1 className="text-xl font-bold text-gray-800 dark:text-gray-100 ml-2">Dashboard</h1>
          ) : (
            <h1 className="text-xl font-bold text-gray-800 dark:text-gray-100 ml-2">Infina</h1>
          )}
        </div>
        <nav className="space-y-2 flex-1">
          {!isAuthenticated && (
            <Link
              to="/"
              className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
            >
              <Home size={20} />
              <span>Home</span>
            </Link>
          )}

          {isAuthenticated && userRole === 'Admin' && (
            <Link
              to="/admin"
              className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
            >
              <Settings size={20} />
              <span>Admin</span>
            </Link>
          )}
          {isAuthenticated && userRole === 'User' && (
            <Link
              to="/user"
              className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
            >
              <User size={20} />
              <span>User</span>
            </Link>
          )}
          {isAuthenticated && (
            <button
              onClick={logout}
              className="flex items-center space-x-3 px-3 py-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 text-gray-700 dark:text-gray-300 hover:text-gray-900 dark:hover:text-gray-100 transition-colors"
            >
              <LayoutDashboard size={20} />
              <span>Logout</span>
            </button>
          )}
        </nav>
      </div>

      {/* Main Content */}
      <div className="flex-1">
        {isAuthenticated && (
          <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700">
            <div className="px-6 py-4">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-800 dark:text-gray-100">Welcome Back</h2>
                <div className="flex items-center space-x-4">
                  <button
                    onClick={toggleTheme}
                    className="p-2 rounded-full hover:bg-gray-100 dark:hover:bg-gray-700"
                  >
                    {theme === 'light' ? (
                      <Moon size={20} className="text-gray-600 dark:text-gray-300" />
                    ) : (
                      <Sun size={20} className="text-gray-600 dark:text-gray-300" />
                    )}
                  </button>
                  <div className="h-8 w-8 rounded-full bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
                    <User size={16} className="text-gray-600 dark:text-gray-300" />
                  </div>
                </div>
              </div>
            </div>
          </header>
        )}
        <main className="p-6">
          <Outlet />
        </main>
      </div>
    </div>
  );
};

export default Layout;