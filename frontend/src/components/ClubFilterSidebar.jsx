export default function ClubFilterSidebar({ clubs, selectedClubs, onToggleClub, onSelectAll, onDeselectAll }) {
  // Main clubs are those with no parent (the API returns them this way by default in ClubListView)
  const mainClubs = clubs.filter(club => !club.parent);

  return (
    <div className="w-64 bg-white/80 dark:bg-gray-900/80 backdrop-blur-md shadow-lg p-6 flex flex-col h-full border-r border-gray-200/50 dark:border-gray-800/50 z-10 transition-colors duration-200">
      <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4 tracking-tight">Filter by Club</h2>

      <div className="flex gap-2 mb-4">
        <button
          onClick={onSelectAll}
          className={`flex-1 text-xs font-semibold px-2 py-1.5 rounded-md transition duration-200 ${
            selectedClubs.length > 0 && selectedClubs.length >= clubs.reduce((acc, club) => acc + 1 + (club.sub_clubs ? club.sub_clubs.length : 0), 0)
              ? 'bg-primary-600 text-white shadow-md hover:bg-primary-700'
              : 'bg-primary-50 dark:bg-primary-500/10 text-primary-600 dark:text-primary-400 hover:bg-primary-100 dark:hover:bg-primary-500/20 border border-primary-200 dark:border-primary-500/30'
          }`}
        >
          All
        </button>
        <button
          onClick={onDeselectAll}
          className={`flex-1 text-xs font-semibold px-2 py-1.5 rounded-md transition duration-200 ${
            selectedClubs.length === 0
              ? 'bg-gray-600 dark:bg-gray-700 text-white shadow-md hover:bg-gray-700 dark:hover:bg-gray-600'
              : 'bg-gray-50 dark:bg-gray-800/50 text-gray-600 dark:text-gray-400 hover:bg-gray-100 dark:hover:bg-gray-800 border border-gray-200 dark:border-gray-700'
          }`}
        >
          None
        </button>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 custom-scrollbar">
        {mainClubs.map((club) => (
          <div key={club.id} className="mb-4">
            <h3 className="text-xs font-bold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 px-2 flex items-center">
              <span className="w-2 h-2 rounded-full mr-2" style={{ backgroundColor: club.color }} />
              {club.name}
            </h3>
            
            <div className="space-y-1 ml-2 border-l-2 border-gray-100 dark:border-gray-700 pl-2">
              {/* Main club checkbox */}
              <label
                className="flex items-center space-x-3 p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition group"
              >
                <input
                  type="checkbox"
                  checked={selectedClubs.includes(club.id)}
                  onChange={() => onToggleClub(club.id)}
                  className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 dark:bg-gray-700 dark:border-gray-600"
                />
                <span className="text-sm font-medium text-gray-700 dark:text-gray-300 flex-1 group-hover:text-primary-600 dark:group-hover:text-primary-400">
                  {club.name}
                </span>
              </label>

              {/* Sub clubs */}
              {club.sub_clubs && club.sub_clubs.map((subClub) => (
                <label
                  key={subClub.id}
                  className="flex items-center space-x-3 p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition group"
                >
                  <input
                    type="checkbox"
                    checked={selectedClubs.includes(subClub.id)}
                    onChange={() => onToggleClub(subClub.id)}
                    className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 dark:bg-gray-700 dark:border-gray-600"
                  />
                  <div 
                    className="w-3 h-3 rounded-full flex-shrink-0" 
                    style={{ backgroundColor: subClub.color }}
                  />
                  <span className="text-xs text-gray-600 dark:text-gray-400 flex-1 group-hover:text-primary-600 dark:group-hover:text-primary-400">
                    {subClub.name}
                  </span>
                </label>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
