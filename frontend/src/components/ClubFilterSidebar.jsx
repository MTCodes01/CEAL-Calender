export default function ClubFilterSidebar({ clubs, selectedClubs, onToggleClub, onSelectAll, onDeselectAll }) {
  return (
    <div className="w-64 bg-white dark:bg-gray-800 shadow-lg p-6 min-h-screen border-r border-gray-200 dark:border-gray-700 transition-colors duration-200">
      <h2 className="text-lg font-bold text-gray-900 dark:text-white mb-4">Filter by Club</h2>

      <div className="flex gap-2 mb-4">
        <button
          onClick={onSelectAll}
          className="flex-1 text-xs px-2 py-1 bg-primary-100 dark:bg-primary-900/30 text-primary-700 dark:text-primary-300 rounded hover:bg-primary-200 dark:hover:bg-primary-900/50 transition"
        >
          All
        </button>
        <button
          onClick={onDeselectAll}
          className="flex-1 text-xs px-2 py-1 bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 rounded hover:bg-gray-200 dark:hover:bg-gray-600 transition"
        >
          None
        </button>
      </div>

      <div className="space-y-2 max-h-[calc(100vh-200px)] overflow-y-auto">
        {clubs.map((club) => (
          <label
            key={club.id}
            className="flex items-center space-x-3 p-2 rounded hover:bg-gray-50 dark:hover:bg-gray-700 cursor-pointer transition"
          >
            <input
              type="checkbox"
              checked={selectedClubs.includes(club.id)}
              onChange={() => onToggleClub(club.id)}
              className="w-4 h-4 text-primary-600 rounded focus:ring-primary-500 dark:bg-gray-700 dark:border-gray-600"
            />
            <span
              className="w-4 h-4 rounded-full flex-shrink-0"
              style={{ backgroundColor: club.color }}
            />
            <span className="text-sm text-gray-700 dark:text-gray-300 flex-1">{club.name}</span>
          </label>
        ))}
      </div>
    </div>
  );
}
