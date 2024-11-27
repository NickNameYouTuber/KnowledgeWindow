import React from 'react';
import { useAuth } from './AuthContext';
import { Navigate, useLocation } from 'react-router-dom';

interface WithAuthProps {
  allowedRoles?: string[];
}

const withAuth = <P extends object>(
  WrappedComponent: React.ComponentType<P>,
  allowedRoles?: string[]
) => {
  const WithAuth: React.FC<P & WithAuthProps> = (props) => {
    const { isAuthenticated, userRole } = useAuth();
    const location = useLocation();

    if (!isAuthenticated) {
      return <Navigate to="/login" state={{ from: location }} replace />;
    }
    console.log("allowedRoles", allowedRoles, "role", userRole)
    if (allowedRoles && !allowedRoles.includes(userRole!)) {
      return <Navigate to="/unauthorized" replace />;
    }

    return <WrappedComponent {...props} />;
  };

  return WithAuth;
};

export default withAuth;