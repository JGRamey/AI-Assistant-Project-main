import React from 'react';
import { BarChart3, Contact as FileContract, CreditCard, TrendingUp, Settings } from 'lucide-react';

type Page = 'dashboard' | 'contracts' | 'subscriptions' | 'analytics' | 'settings';

interface NavigationProps {
  currentPage: Page;
  setCurrentPage: (page: Page) => void;
  mobile?: boolean;
  onNavigate?: () => void;
}

const Navigation: React.FC<NavigationProps> = ({ currentPage, setCurrentPage, mobile = false, onNavigate }) => {
  const navigationItems = [
    { id: 'dashboard' as Page, label: 'Dashboard', icon: BarChart3 },
    { id: 'contracts' as Page, label: 'Smart Contracts', icon: FileContract },
    { id: 'subscriptions' as Page, label: 'Subscriptions', icon: CreditCard },
    { id: 'analytics' as Page, label: 'Analytics', icon: TrendingUp },
    { id: 'settings' as Page, label: 'Settings', icon: Settings },
  ];

  const handleNavigation = (page: Page) => {
    setCurrentPage(page);
    if (onNavigate) onNavigate();
  };

  if (mobile) {
    return (
      <div className="space-y-1">
        {navigationItems.map((item) => {
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => handleNavigation(item.id)}
              className={`w-full flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
                currentPage === item.id
                  ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300'
                  : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-gray-100 dark:hover:bg-gray-700'
              }`}
            >
              <Icon className="h-5 w-5 mr-3" />
              {item.label}
            </button>
          );
        })}
      </div>
    );
  }

  return (
    <nav className="flex space-x-8">
      {navigationItems.map((item) => {
        const Icon = item.icon;
        return (
          <button
            key={item.id}
            onClick={() => handleNavigation(item.id)}
            className={`flex items-center px-3 py-2 text-sm font-medium rounded-md transition-colors ${
              currentPage === item.id
                ? 'bg-primary-100 text-primary-700 dark:bg-primary-900 dark:text-primary-300'
                : 'text-gray-600 hover:text-gray-900 hover:bg-gray-50 dark:text-gray-400 dark:hover:text-gray-100 dark:hover:bg-gray-700'
            }`}
          >
            <Icon className="h-5 w-5 mr-2" />
            {item.label}
          </button>
        );
      })}
    </nav>
  );
};

export default Navigation;