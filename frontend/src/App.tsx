import React, { useState, useEffect } from 'react';
import { Sun, Moon, Mic, MicOff } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import Dashboard from './pages/Dashboard';
import Tasks from './pages/Tasks';
import Projects from './pages/Projects';
import Agents from './pages/Agents';
import Analytics from './pages/Analytics';
import Settings from './pages/Settings';
import VoiceInterface from './features/VoiceInterface';
import FloatingNavigation from './layouts/FloatingNavigation';

type Page = 'dashboard' | 'tasks' | 'projects' | 'agents' | 'analytics' | 'settings';

function App() {
  const [currentPage, setCurrentPage] = useState<Page>('dashboard');
  const [darkMode, setDarkMode] = useState(false);
  const [isListening, setIsListening] = useState(false);
  const [showMainInterface, setShowMainInterface] = useState(false);

  useEffect(() => {
    if (typeof window !== 'undefined') {
      const isDark = localStorage.getItem('darkMode') === 'true' || 
        (!localStorage.getItem('darkMode') && window.matchMedia('(prefers-color-scheme: dark)').matches);
      setDarkMode(isDark);
      document.documentElement.classList.toggle('dark', isDark);
    }
  }, []);

  const toggleDarkMode = () => {
    const newMode = !darkMode;
    setDarkMode(newMode);
    localStorage.setItem('darkMode', newMode.toString());
    document.documentElement.classList.toggle('dark', newMode);
  };

  const toggleVoice = () => {
    setIsListening(!isListening);
    // Here you would integrate with speech recognition API
  };

  const renderCurrentPage = () => {
    switch (currentPage) {
      case 'dashboard':
        return <Dashboard />;
      case 'tasks':
        return <Tasks />;
      case 'projects':
        return <Projects />;
      case 'agents':
        return <Agents />;
      case 'analytics':
        return <Analytics />;
      case 'settings':
        return <Settings />;
      default:
        return <Dashboard />;
    }
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-50 via-blue-50 to-purple-50 dark:from-gray-900 dark:via-blue-900 dark:to-purple-900 transition-all duration-500">
      {/* Header */}
      <header className="fixed top-0 left-0 right-0 z-50 bg-white/80 dark:bg-gray-900/80 backdrop-blur-lg border-b border-gray-200/50 dark:border-gray-700/50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-16">
            <motion.div 
              className="flex items-center"
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.5 }}
            >
              <h1 className="text-2xl font-bold bg-gradient-to-r from-primary-600 via-secondary-600 to-accent-600 bg-clip-text text-transparent">
                AI Assistant Hub
              </h1>
            </motion.div>

            <div className="flex items-center space-x-4">
              <motion.button
                onClick={toggleVoice}
                className={`p-3 rounded-full transition-all duration-300 ${
                  isListening 
                    ? 'bg-red-500 text-white shadow-lg shadow-red-500/25' 
                    : 'bg-primary-100 dark:bg-primary-900 text-primary-600 dark:text-primary-400 hover:bg-primary-200 dark:hover:bg-primary-800'
                }`}
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {isListening ? <MicOff className="h-5 w-5" /> : <Mic className="h-5 w-5" />}
              </motion.button>

              <motion.button
                onClick={toggleDarkMode}
                className="p-3 text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200 rounded-full hover:bg-gray-100 dark:hover:bg-gray-800 transition-all duration-300"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {darkMode ? <Sun className="h-5 w-5" /> : <Moon className="h-5 w-5" />}
              </motion.button>

              <motion.button
                onClick={() => setShowMainInterface(!showMainInterface)}
                className="px-4 py-2 bg-gradient-to-r from-primary-600 to-secondary-600 text-white rounded-lg hover:from-primary-700 hover:to-secondary-700 transition-all duration-300 shadow-lg"
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
              >
                {showMainInterface ? 'Hide Interface' : 'Show Interface'}
              </motion.button>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="h-screen overflow-hidden">
        <AnimatePresence mode="wait">
          {!showMainInterface ? (
            <motion.div
              key="voice-interface"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              transition={{ duration: 0.5 }}
              className="h-screen relative"
            >
              <VoiceInterface 
                isListening={isListening}
                onToggleListening={toggleVoice}
                onNavigate={setCurrentPage}
                onShowInterface={() => setShowMainInterface(true)}
              />
              <FloatingNavigation 
                currentPage={currentPage}
                setCurrentPage={setCurrentPage}
                onNavigate={() => setShowMainInterface(true)}
              />
            </motion.div>
          ) : (
            <motion.div
              key="main-interface"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              exit={{ opacity: 0, y: -20 }}
              transition={{ duration: 0.5 }}
              className="h-screen overflow-y-auto pt-16 max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8"
            >
              {renderCurrentPage()}
            </motion.div>
          )}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;