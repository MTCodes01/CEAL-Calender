import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { useTheme } from '../context/ThemeContext';
import ThemeToggle from './ThemeToggle';

export default function Navbar() {
  const { user, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <nav className="bg-white dark:bg-gray-800 shadow-md border-b border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/calendar" className="text-2xl font-bold text-primary-600 dark:text-primary-400">
              CEAL Calendar
            </Link>
          </div>

          <div className="flex items-center space-x-4">
            <ThemeToggle />
            {user && (
              <>
                <span className="text-sm text-gray-700 dark:text-gray-300">
                  <span className="font-semibold">{user.first_name} {user.last_name}</span>
                  {user.club && (
                    <span className="ml-2 px-2 py-1 text-xs rounded-full text-white"
                          style={{ backgroundColor: user.club.color }}>
                      {user.club.name}
                    </span>
                  )}
                </span>
                <Link
                  to="/settings"
                  className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition"
                >
                  Settings
                </Link>
                <Link
                  to="/profile"
                  className="text-gray-700 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 font-medium transition"
                >
                  Profile
                </Link>
                <button
                  onClick={handleLogout}
                  className="px-4 py-2 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded-lg hover:bg-gray-200 dark:hover:bg-gray-600 transition font-medium"
                >
                  Logout
                </button>
              </>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
