import React, { useState, useEffect } from 'react';
import api from '../api/client';
import { useAuth } from '../context/AuthContext';
import ClubManagement from '../components/ClubManagement';

const AdminDashboard = () => {
  const { user } = useAuth();
  const [activeTab, setActiveTab] = useState('users'); // 'users' or 'clubs'
  const [users, setUsers] = useState([]);
  const [clubs, setClubs] = useState([]);
  const [loading, setLoading] = useState(true);
  const [editingUser, setEditingUser] = useState(null);
  const [selectedClub, setSelectedClub] = useState('');
  const [selectedSubClub, setSelectedSubClub] = useState('');
  const [error, setError] = useState('');

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [usersRes, clubsRes] = await Promise.all([
        api.get('/api/auth/users/'),
        api.get('/api/clubs/')
      ]);
      setUsers(usersRes.data.results || usersRes.data);
      setClubs(clubsRes.data.results || clubsRes.data);
    } catch (err) {
      setError('Failed to load data. Ensure you are an admin.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleEditClick = (user) => {
    setEditingUser(user);
    setSelectedClub(user.club ? user.club.id : '');
    setSelectedSubClub(user.sub_club ? user.sub_club.id : '');
  };

  const handleSave = async () => {
    try {
      await api.patch(`/api/auth/users/${editingUser.id}/`, {
        club: selectedClub || null,
        sub_club: selectedSubClub || null
      });
      setEditingUser(null);
      fetchData(); // Refresh list
    } catch (err) {
      console.error('Failed to update user', err);
      alert('Failed to update user');
    }
  };

  const handleDelete = async (userId) => {
    if (window.confirm('Are you sure you want to delete this user? This action cannot be undone.')) {
      try {
        await api.delete(`/api/auth/users/${userId}/`);
        fetchData(); // Refresh list
      } catch (err) {
        console.error('Failed to delete user', err);
        alert('Failed to delete user');
      }
    }
  };

  // Filter sub-clubs based on selected parent club using the nested structure
  const selectedMainClub = clubs.find(c => c.id === parseInt(selectedClub));
  const subClubOptions = selectedMainClub?.sub_clubs || [];
  
  // Main clubs are those returned at the top level (they have no parent in the new API)
  const mainClubOptions = clubs;

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (error) return <div className="p-8 text-center text-red-500">{error}</div>;

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
      <div className="flex flex-col md:flex-row md:items-center justify-between mb-8 space-y-4 md:space-y-0">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Admin Dashboard</h1>
        
        <div className="flex bg-gray-100 dark:bg-gray-700 p-1 rounded-lg">
          <button
            onClick={() => setActiveTab('users')}
            className={`px-4 py-2 text-sm font-medium rounded-md transition ${activeTab === 'users' ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'}`}
          >
            Manage Users
          </button>
          <button
            onClick={() => setActiveTab('clubs')}
            className={`px-4 py-2 text-sm font-medium rounded-md transition ${activeTab === 'clubs' ? 'bg-white dark:bg-gray-600 text-gray-900 dark:text-white shadow' : 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200'}`}
          >
            Manage Clubs
          </button>
        </div>
      </div>
      
      {activeTab === 'users' ? (
        <div className="bg-white dark:bg-gray-800 shadow overflow-x-auto sm:rounded-lg border border-gray-200 dark:border-gray-700">
          <table className="min-w-full divide-y divide-gray-200 dark:divide-gray-700">
            <thead className="bg-gray-50 dark:bg-gray-700">
              <tr>
                <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase tracking-wider">User</th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Email</th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Club</th>
                <th className="px-6 py-3 text-left text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Sub Club</th>
                <th className="px-6 py-3 text-right text-xs font-semibold text-gray-500 dark:text-gray-300 uppercase tracking-wider">Actions</th>
              </tr>
            </thead>
            <tbody className="bg-white dark:bg-gray-800 divide-y divide-gray-200 dark:divide-gray-700">
              {users.map((u) => (
                <tr key={u.id} className="hover:bg-gray-50 dark:hover:bg-gray-700/50 transition">
                  <td className="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900 dark:text-white">
                    {u.first_name} {u.last_name} <span className="text-gray-400 ml-1">({u.username})</span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {u.email}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {u.club ? (
                      <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full border" style={{ borderColor: u.club.color, color: u.club.color, backgroundColor: u.club.color + '10' }}>
                        {u.club.name}
                      </span>
                    ) : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500 dark:text-gray-400">
                    {u.sub_club ? (
                      <span className="px-2 py-1 inline-flex text-xs leading-5 font-semibold rounded-full border" style={{ borderColor: u.sub_club.color, color: u.sub_club.color, backgroundColor: u.sub_club.color + '10' }}>
                        {u.sub_club.name}
                      </span>
                    ) : '-'}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium space-x-2">
                    <button onClick={() => handleEditClick(u)} className="text-primary-600 hover:text-primary-900 dark:text-primary-400 dark:hover:text-primary-300 font-semibold transition">Edit</button>
                    <button onClick={() => handleDelete(u.id)} className="text-red-600 hover:text-red-900 dark:text-red-400 dark:hover:text-red-300 font-semibold transition">Delete</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      ) : (
        <ClubManagement />
      )}

      {activeTab === 'users' && editingUser && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 transition-opacity" aria-hidden="true">
              <div className="absolute inset-0 bg-gray-500 opacity-75"></div>
            </div>
            <span className="hidden sm:inline-block sm:align-middle sm:h-screen" aria-hidden="true">&#8203;</span>
            <div className="inline-block align-bottom bg-white dark:bg-gray-800 rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full border border-gray-200 dark:border-gray-700">
              <div className="bg-white dark:bg-gray-800 px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                <h3 className="text-lg leading-6 font-bold text-gray-900 dark:text-white" id="modal-title">
                  Assign Roles: {editingUser.email}
                </h3>
                <div className="mt-4 space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Main Club Responsibility</label>
                    <select
                      value={selectedClub}
                      onChange={(e) => {
                        setSelectedClub(e.target.value);
                        setSelectedSubClub(''); // Reset sub-club when main club changes
                      }}
                      className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md dark:bg-gray-700 dark:text-white"
                    >
                      <option value="">None (Viewer Only)</option>
                      {mainClubOptions.map(c => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                      ))}
                    </select>
                  </div>
                  <div>
                    <label className="block text-sm font-medium text-gray-700 dark:text-gray-300">Sub Club Responsibility</label>
                    <select
                      value={selectedSubClub}
                      onChange={(e) => setSelectedSubClub(e.target.value)}
                      disabled={!selectedClub}
                      className="mt-1 block w-full pl-3 pr-10 py-2 text-base border border-gray-300 dark:border-gray-600 focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm rounded-md dark:bg-gray-700 dark:text-white disabled:opacity-50"
                    >
                      <option value="">None</option>
                      {subClubOptions.map(c => (
                        <option key={c.id} value={c.id}>{c.name}</option>
                      ))}
                    </select>
                    {!selectedClub && <p className="text-xs text-gray-500 mt-2">Assign a main club first to see sub-club options.</p>}
                  </div>
                </div>
              </div>
              <div className="bg-gray-50 dark:bg-gray-700 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse space-y-2 sm:space-y-0">
                <button
                  type="button"
                  onClick={handleSave}
                  className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-primary-600 text-base font-medium text-white hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:ml-3 sm:w-auto sm:text-sm"
                >
                  Save Changes
                </button>
                <button
                  type="button"
                  onClick={() => setEditingUser(null)}
                  className="w-full inline-flex justify-center rounded-md border border-gray-300 dark:border-gray-600 shadow-sm px-4 py-2 bg-white dark:bg-gray-800 text-base font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 sm:w-auto sm:text-sm"
                >
                  Cancel
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminDashboard;
