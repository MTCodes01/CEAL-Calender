import { createContext, useContext, useState, useCallback } from 'react';

const ToastContext = createContext(null);

/**
 * Toast notification types with their corresponding styles.
 */
const TOAST_STYLES = {
  success: {
    bg: 'bg-green-50 dark:bg-green-900/40 border-green-300 dark:border-green-700',
    text: 'text-green-800 dark:text-green-200',
    icon: '✓',
  },
  error: {
    bg: 'bg-red-50 dark:bg-red-900/40 border-red-300 dark:border-red-700',
    text: 'text-red-800 dark:text-red-200',
    icon: '✕',
  },
  info: {
    bg: 'bg-blue-50 dark:bg-blue-900/40 border-blue-300 dark:border-blue-700',
    text: 'text-blue-800 dark:text-blue-200',
    icon: 'ℹ',
  },
  warning: {
    bg: 'bg-yellow-50 dark:bg-yellow-900/40 border-yellow-300 dark:border-yellow-700',
    text: 'text-yellow-800 dark:text-yellow-200',
    icon: '⚠',
  },
};

let toastId = 0;

export function ToastProvider({ children }) {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = 'info', duration = 4000) => {
    const id = ++toastId;
    setToasts((prev) => [...prev, { id, message, type }]);

    if (duration > 0) {
      setTimeout(() => {
        setToasts((prev) => prev.filter((t) => t.id !== id));
      }, duration);
    }

    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts((prev) => prev.filter((t) => t.id !== id));
  }, []);

  const toast = {
    success: (msg, duration) => addToast(msg, 'success', duration),
    error: (msg, duration) => addToast(msg, 'error', duration),
    info: (msg, duration) => addToast(msg, 'info', duration),
    warning: (msg, duration) => addToast(msg, 'warning', duration),
  };

  return (
    <ToastContext.Provider value={toast}>
      {children}

      {/* Toast container — fixed to top-right */}
      <div className="fixed top-4 right-4 z-[9999] flex flex-col gap-2 max-w-sm w-full pointer-events-none">
        {toasts.map((t) => {
          const style = TOAST_STYLES[t.type] || TOAST_STYLES.info;
          return (
            <div
              key={t.id}
              className={`pointer-events-auto flex items-start gap-3 px-4 py-3 rounded-lg border shadow-lg backdrop-blur-sm animate-slide-in ${style.bg}`}
              role="alert"
            >
              <span className={`text-lg font-bold ${style.text} flex-shrink-0`}>{style.icon}</span>
              <p className={`text-sm font-medium ${style.text} flex-1`}>{t.message}</p>
              <button
                onClick={() => removeToast(t.id)}
                className={`text-sm font-bold ${style.text} opacity-60 hover:opacity-100 flex-shrink-0`}
              >
                ×
              </button>
            </div>
          );
        })}
      </div>
    </ToastContext.Provider>
  );
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}
