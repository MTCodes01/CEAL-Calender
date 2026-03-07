export default function Footer() {
  return (
    <footer className="bg-white/80 dark:bg-gray-900/80 backdrop-blur-md border-t border-gray-200 dark:border-gray-800 transition-colors duration-200">
      <div className="w-full px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-center h-10">
          <p className="text-sm text-gray-500 dark:text-gray-400 flex items-center gap-1.5">
            Made with
            <span className="text-red-500 animate-pulse">❤️</span>
            by
            <a href="https://sreedevss.in/" target="_blank" rel="noopener noreferrer"><span className="font-semibold text-gray-700 dark:text-gray-300">MT</span></a>
            <span className="text-gray-400 dark:text-gray-600">|</span>
            <a href="https://foss.ceal.in/chamber/303/train.html" target="_blank" rel="noopener noreferrer"><span className="font-semibold text-gray-700 dark:text-gray-300 tracking-wide">TRAIN303</span></a>
          </p>
        </div>
      </div>
    </footer>
  );
}
