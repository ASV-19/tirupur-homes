import { ReactNode, useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import LoginSignupModal from './LoginSignupModal';

interface LayoutProps {
  children: ReactNode;
}

const Layout = ({ children }: LayoutProps) => {
  const [isModalOpen, setIsModalOpen] = useState(false);
  const location = useLocation();
  const { isAuthenticated, user, logout } = useAuth();

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
            <nav className="flex items-center space-x-8">
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
                <div className="flex items-center space-x-4">
                  <span className="text-gray-700">
                    Welcome, {user?.name}
                  </span>
                  {user?.role === 'ADMIN' && (
                    <Link
                      to="/admin"
                      className={`${
                        location.pathname.startsWith('/admin') ? 'text-blue-600' : 'text-gray-700'
                      } hover:text-gray-900 transition-colors`}
                    >
                      Admin Panel
                    </Link>
                  )}
                  <button
                    onClick={() => {
                      logout();
                      window.location.reload();
                    }}
                    className="text-gray-700 hover:text-gray-900 transition-colors"
                  >
                    Logout
                  </button>
                </div>
              ) : (
                <button
                  onClick={() => setIsModalOpen(true)}
                  className="text-gray-700 hover:text-gray-900 transition-colors"
                >
                  Sign In / Sign Up
                </button>
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

      <LoginSignupModal
        isOpen={isModalOpen}
        onClose={() => setIsModalOpen(false)}
      />
    </div>
  );
};

export default Layout;
