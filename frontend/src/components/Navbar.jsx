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
        <div className="flex justify-between items-center h-16">
          <div className="flex-shrink-0 flex items-center">
            <Link to="/calendar" className="text-xl md:text-2xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-primary-500 to-primary-700 dark:from-primary-400 dark:to-primary-600 tracking-tight hover:opacity-80 transition-opacity">
              CEAL Calendar
            </Link>
          </div>

          <div className="flex items-center space-x-3 md:space-x-6">
            <ThemeToggle />
            
            {user && (
              <div className="flex items-center space-x-3 md:space-x-4">
                <div className="hidden md:flex flex-col items-end">
                  <span className="text-sm font-semibold text-gray-900 dark:text-white leading-tight">
                    {user.first_name} {user.last_name}
                  </span>
                  <div className="flex gap-1 mt-0.5">
                    {user.club && (
                      <span 
                        className="text-[10px] font-bold px-1.5 py-0.5 rounded-sm uppercase tracking-wider text-white shadow-sm"
                        style={{ backgroundColor: user.club.color }}
                      >
                        {user.club.name}
                      </span>
                    )}
                    {user.sub_club && (
                      <span 
                        className="text-[10px] font-bold px-1.5 py-0.5 rounded-sm uppercase tracking-wider text-white shadow-sm"
                        style={{ backgroundColor: user.sub_club.color }}
                      >
                        {user.sub_club.name}
                      </span>
                    )}
                  </div>
                </div>

                <div className="h-6 w-px bg-gray-300 dark:bg-gray-600 hidden md:block" />

                <nav className="hidden sm:flex items-center space-x-1">
                  {user.is_superuser && (
                    <Link
                      to="/admin"
                      className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
                    >
                      Admin
                    </Link>
                  )}
                  <Link
                    to="/profile"
                    className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
                  >
                    Profile
                  </Link>
                  <Link
                    to="/settings"
                    className="px-3 py-2 rounded-md text-sm font-medium text-gray-600 dark:text-gray-300 hover:text-primary-600 dark:hover:text-primary-400 hover:bg-gray-100 dark:hover:bg-gray-700 transition"
                  >
                    Settings
                  </Link>
                </nav>

                <button
                  onClick={handleLogout}
                  className="ml-2 inline-flex items-center justify-center px-4 py-2 border border-transparent text-sm font-medium rounded-md text-white bg-red-600 hover:bg-red-700 shadow-sm transition-colors focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500 dark:focus:ring-offset-gray-800"
                >
                  Logout
                </button>
              </div>
            )}
          </div>
        </div>
      </div>
    </nav>
  );
}
