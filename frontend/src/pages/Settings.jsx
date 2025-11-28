import { useState, useEffect } from 'react';
import { useAuth } from '../context/AuthContext';
import Navbar from '../components/Navbar';

const TIMEZONES = [
  'Asia/Kolkata', 'America/New_York', 'America/Los_Angeles', 'Europe/London',
  'Europe/Paris', 'Asia/Tokyo', 'Australia/Sydney', 'Asia/Dubai', 'UTC'
];

export default function Settings() {
  const { user, updateProfile } = useAuth();
  const [formData, setFormData] = useState({
    notification_enabled: true,
    notification_time: '',
    timezone: 'Asia/Kolkata',
  });
  const [message, setMessage] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (user) {
      setFormData({
        notification_enabled: user.notification_enabled ?? true,
        notification_time: user.notification_time || '',
        timezone: user.timezone || 'Asia/Kolkata',
      });
    }
  }, [user]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setMessage('');
    setError('');
    setLoading(true);

    const result = await updateProfile(formData);

    if (result.success) {
      setMessage('Settings saved successfully!');
    } else {
      setError('Failed to save settings');
    }
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 dark:bg-gray-900 transition-colors duration-200">
      <Navbar />
      
      <div className="max-w-3xl mx-auto p-8">
        <div className="bg-white dark:bg-gray-800 rounded-xl shadow-lg p-8 transition-colors duration-200">
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-6">Notification Settings</h1>

          {message && (
            <div className="bg-green-50 dark:bg-green-900/30 border border-green-200 dark:border-green-800 text-green-700 dark:text-green-300 px-4 py-3 rounded-lg mb-6">
              {message}
            </div>
          )}

          {error && (
            <div className="bg-red-50 dark:bg-red-900/30 border border-red-200 dark:border-red-800 text-red-700 dark:text-red-300 px-4 py-3 rounded-lg mb-6">
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} className="space-y-6">
            <div className="flex items-center space-x-3">
              <input
                type="checkbox"
                id="notification_enabled"
                checked={formData.notification_enabled}
                onChange={(e) => setFormData({ ...formData, notification_enabled: e.target.checked })}
                className="w-5 h-5 text-primary-600 rounded focus:ring-primary-500"
              />
              <label htmlFor="notification_enabled" className="text-lg font-medium text-gray-900 dark:text-white">
                Enable Email Notifications
              </label>
            </div>

            {formData.notification_enabled && (
              <>
                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Notification Time (HH:MM)
                  </label>
                  <input
                    type="time"
                    required={formData.notification_enabled}
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    value={formData.notification_time}
                    onChange={(e) => setFormData({ ...formData, notification_time: e.target.value })}
                  />
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-2">
                    You'll receive a daily email at this time if new events were added to your club.
                  </p>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
                    Timezone
                  </label>
                  <select
                    className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:ring-2 focus:ring-primary-500 bg-white dark:bg-gray-700 text-gray-900 dark:text-white"
                    value={formData.timezone}
                    onChange={(e) => setFormData({ ...formData, timezone: e.target.value })}
                  >
                    {TIMEZONES.map((tz) => (
                      <option key={tz} value={tz}>{tz}</option>
                    ))}
                  </select>
                </div>
              </>
            )}

            <button
              type="submit"
              disabled={loading}
              className="w-full bg-gradient-to-r from-primary-500 to-purple-600 text-white py-3 rounded-lg font-semibold hover:shadow-lg transition disabled:opacity-50"
            >
              {loading ? 'Saving...' : 'Save Settings'}
            </button>
          </form>

          <div className="mt-8 p-4 bg-blue-50 dark:bg-blue-900/30 border border-blue-200 dark:border-blue-800 rounded-lg">
            <h3 className="font-semibold text-blue-900 dark:text-blue-300 mb-2">ℹ️  How Notifications Work</h3>
            <ul className="text-sm text-blue-800 dark:text-blue-200 space-y-1">
              <li>• Emails are sent only if NEW events were created since your last notification</li>
              <li>• Only events from your club will be included</li>
              <li>• Other members will continue to receive notifications if they have them enabled</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
}
