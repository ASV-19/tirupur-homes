import { ReactNode } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../hooks/useAuth';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const location = useLocation();
  const { isAuthenticated, user } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-4">
            <div className="flex items-center">
              <Link to="/" className="text-2xl font-bold text-gray-900 hover:text-gray-700">
                Tirupur Homes
              </Link>
            </div>
            <nav className="flex space-x-8">
              <Link
                to="/"
                className={`${
                  location.pathname === '/' ? 'text-blue-600' : 'text-gray-700'
                } hover:text-gray-900 transition-colors`}
              >
                Home
              </Link>
              <Link
                to="/properties"
                className={`${
                  location.pathname.startsWith('/properties') ? 'text-blue-600' : 'text-gray-700'
                } hover:text-gray-900 transition-colors`}
              >
                Properties
              </Link>
              <a
                href="#contact"
                className="text-gray-700 hover:text-gray-900 transition-colors"
              >
                Contact
              </a>
              {isAuthenticated ? (
                <Link
                  to="/admin"
                  className={`${
                    location.pathname.startsWith('/admin') ? 'text-blue-600' : 'text-gray-700'
                  } hover:text-gray-900 transition-colors`}
                >
                  Admin
                </Link>
              ) : (
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-gray-900 transition-colors"
                >
                  Admin Login
                </Link>
              )}
            </nav>
          </div>
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {children}
      </main>

      <footer className="bg-white border-t">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <p className="text-center text-gray-500">
            © 2025 Tirupur Homes. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
