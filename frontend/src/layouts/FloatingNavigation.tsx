import React from 'react';
import { motion } from 'framer-motion';
import { 
  LayoutDashboard, 
  CheckSquare, 
  FolderOpen, 
  Users, 
  BarChart3, 
  Settings 
} from 'lucide-react';

type Page = 'dashboard' | 'tasks' | 'projects' | 'agents' | 'analytics' | 'settings';

interface FloatingNavigationProps {
  currentPage: Page;
  setCurrentPage: (page: Page) => void;
  onNavigate: () => void;
}

const FloatingNavigation: React.FC<FloatingNavigationProps> = ({
  currentPage,
  setCurrentPage,
  onNavigate
}) => {
  const navigationItems = [
    { id: 'dashboard' as Page, label: 'Dashboard', icon: LayoutDashboard, color: 'from-blue-500 to-blue-600' },
    { id: 'tasks' as Page, label: 'Tasks', icon: CheckSquare, color: 'from-green-500 to-green-600' },
    { id: 'projects' as Page, label: 'Projects', icon: FolderOpen, color: 'from-purple-500 to-purple-600' },
    { id: 'agents' as Page, label: 'AI Agents', icon: Users, color: 'from-orange-500 to-orange-600' },
    { id: 'analytics' as Page, label: 'Analytics', icon: BarChart3, color: 'from-pink-500 to-pink-600' },
    { id: 'settings' as Page, label: 'Settings', icon: Settings, color: 'from-gray-500 to-gray-600' },
  ];

  const handleNavigation = (page: Page) => {
    setCurrentPage(page);
    onNavigate();
  };

  return (
    <div className="fixed top-16 left-0 right-0 z-30 pointer-events-none">
      {/* Navigation Circles - Below nav bar */}
      <motion.div
        className="w-full px-8 py-8 pointer-events-auto"
        initial={{ opacity: 0, y: -30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8, ease: "easeOut" }}
      >
        <div className="max-w-5xl mx-auto">
          <div className="flex justify-center items-center space-x-12">
            {navigationItems.map((item, index) => {
              const Icon = item.icon;
              
              return (
                <motion.div
                  key={item.id}
                  className="flex flex-col items-center group"
                  initial={{ opacity: 0, scale: 0, y: -20 }}
                  animate={{ 
                    opacity: 1, 
                    scale: 1,
                    y: 0
                  }}
                  transition={{ 
                    delay: index * 0.15,
                    duration: 0.6,
                    ease: "easeOut"
                  }}
                >
                  <motion.button
                    onClick={() => handleNavigation(item.id)}
                    className={`relative w-16 h-16 rounded-full bg-gradient-to-r ${item.color} shadow-lg hover:shadow-xl transition-all duration-300 flex items-center justify-center mb-3`}
                    whileHover={{ 
                      scale: 1.1,
                      y: -4,
                      transition: { duration: 0.2 }
                    }}
                    whileTap={{ scale: 0.95 }}
                  >
                    <Icon className="h-6 w-6 text-white" />
                    
                    {/* Active indicator */}
                    {currentPage === item.id && (
                      <>
                        <motion.div
                          className="absolute inset-0 rounded-full border-3 border-white"
                          initial={{ scale: 0.8, opacity: 0 }}
                          animate={{ scale: 1, opacity: 1 }}
                          transition={{ duration: 0.3 }}
                        />
                        {/* Pulse effect for active item */}
                        <motion.div
                          className="absolute inset-0 rounded-full border-2 border-white"
                          animate={{
                            scale: [1, 1.4, 1],
                            opacity: [0.6, 0, 0.6]
                          }}
                          transition={{
                            duration: 2.5,
                            repeat: Infinity,
                            ease: "easeInOut"
                          }}
                        />
                      </>
                    )}

                    {/* Hover glow effect */}
                    <motion.div
                      className={`absolute inset-0 rounded-full bg-gradient-to-r ${item.color} opacity-0 group-hover:opacity-30 transition-opacity duration-300 blur-md`}
                      style={{ transform: 'scale(1.2)' }}
                    />
                  </motion.button>

                  {/* Label */}
                  <motion.span
                    className={`text-sm font-medium transition-all duration-300 ${
                      currentPage === item.id
                        ? 'text-gray-900 dark:text-white'
                        : 'text-gray-600 dark:text-gray-400 group-hover:text-gray-900 dark:group-hover:text-white'
                    }`}
                    initial={{ opacity: 0 }}
                    animate={{ opacity: 1 }}
                    transition={{ delay: index * 0.15 + 0.3 }}
                  >
                    {item.label}
                  </motion.span>

                  {/* Active underline */}
                  {currentPage === item.id && (
                    <motion.div
                      className="mt-1 h-0.5 w-8 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-full"
                      initial={{ scaleX: 0 }}
                      animate={{ scaleX: 1 }}
                      transition={{ duration: 0.3 }}
                    />
                  )}
                </motion.div>
              );
            })}
          </div>
        </div>
      </motion.div>
    </div>
  );
};

export default FloatingNavigation;