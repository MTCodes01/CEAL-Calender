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

      <div className="space-y-6 max-h-[calc(100vh-200px)] overflow-y-auto pr-2">
        {['IEEE', 'FOSS', 'IEDC', 'ISTE', 'NSS', 'TinkerHub', 'Cultural', 'Sports', 'Other'].map((category) => {
          const categoryClubs = clubs.filter(club => {
            const s = club.slug;
            if (category === 'Cultural') return s === 'yavanika';
            if (category === 'FOSS') return s.startsWith('foss-');
            if (category === 'IEDC') return s.startsWith('iedc-');
            if (category === 'IEEE') return s.startsWith('ieee-');
            if (category === 'ISTE') return s === 'iste';
            if (category === 'NSS') return s === 'nss';
            if (category === 'Sports') return s === 'sports';
            if (category === 'TinkerHub') return s === 'tinkerhub';
            
            // Other: anything not matched above
            return !s.startsWith('ieee-') && !s.startsWith('foss-') && !s.startsWith('iedc-') && 
                   !['iste', 'nss', 'tinkerhub', 'yavanika', 'sports'].includes(s);
          });

          if (categoryClubs.length === 0) return null;

          return (
            <div key={category}>
              <h3 className="text-xs font-semibold text-gray-500 dark:text-gray-400 uppercase tracking-wider mb-2 px-2">
                {category}
              </h3>
              <div className="space-y-1">
                {categoryClubs.map((club) => (
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
              <div className="mt-4 border-b border-gray-100 dark:border-gray-700 last:border-0" />
            </div>
          );
        })}
      </div>
    </div>
  );
}
