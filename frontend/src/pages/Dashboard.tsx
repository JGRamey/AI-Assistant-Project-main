import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { 
  CheckSquare, 
  FolderOpen, 
  TrendingUp, 
  Brain,
  DollarSign
} from 'lucide-react';

const Dashboard: React.FC = () => {
  const [dashboardData, setDashboardData] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await fetch('/api/dashboard', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ task: 'view', user_id: 'test-user' }), // Hardcoded user_id for now
        });
        const data = await response.json();
        setDashboardData(data);
      } catch (error) {
        console.error('Error fetching dashboard data:', error);
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completed':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'In Progress':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'Pending':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'High':
        return 'text-red-600 dark:text-red-400';
      case 'Medium':
        return 'text-yellow-600 dark:text-yellow-400';
      case 'Low':
        return 'text-green-600 dark:text-green-400';
      default:
        return 'text-gray-600 dark:text-gray-400';
    }
  };

  if (loading) {
    return <div className="flex justify-center items-center h-full">Loading...</div>;
  }

  if (!dashboardData || dashboardData.error) {
    return <div className="flex justify-center items-center h-full">Error loading data. Please try again later.</div>;
  }

  const stats = [
    { label: 'Active Tasks', value: dashboardData.tasks?.length || 0, icon: CheckSquare, color: 'from-green-500 to-green-600' },
    { label: 'Portfolio Items', value: dashboardData.portfolio?.length || 0, icon: FolderOpen, color: 'from-purple-500 to-purple-600' },
    { label: 'Total Expenses', value: `$${(dashboardData.expenses?.reduce((acc: any, exp: any) => acc + exp.amount, 0) || 0).toFixed(2)}`, icon: DollarSign, color: 'from-orange-500 to-orange-600' },
    { label: 'Budgets Set', value: dashboardData.budgets?.length || 0, icon: TrendingUp, color: 'from-blue-500 to-blue-600' },
  ];

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <motion.div
        className="bg-gradient-to-r from-primary-600 via-secondary-600 to-accent-600 rounded-2xl p-8 text-white"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold mb-2">Welcome back!</h1>
            <p className="text-white/90 text-lg">
              Your AI assistants are ready to help you tackle today's challenges
            </p>
          </div>
          <motion.div
            className="p-4 bg-white/20 rounded-full"
            animate={{ rotate: 360 }}
            transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
          >
            <Brain className="h-12 w-12 text-white" />
          </motion.div>
        </div>
      </motion.div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {stats.map((stat, index) => (
          <motion.div
            key={index}
            className={`bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg transform hover:-translate-y-1 transition-all duration-300`}
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
          >
            <div className="flex items-center justify-between">
              <div className={`p-3 rounded-full bg-gradient-to-br ${stat.color}`}>
                <stat.icon className="h-6 w-6 text-white" />
              </div>
              <div className="text-right">
                <p className="text-gray-500 dark:text-gray-400">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-800 dark:text-white">{stat.value}</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        {/* Recent Tasks */}
        <div className="lg:col-span-2 bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg">
          <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Recent Tasks</h2>
          <div className="space-y-4">
            {(dashboardData.tasks && dashboardData.tasks.length > 0) ? dashboardData.tasks.map((task: any) => (
              <motion.div
                key={task.id}
                className="flex items-center justify-between p-4 bg-gray-50 dark:bg-gray-700/50 rounded-lg"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.5 }}
              >
                <div>
                  <p className="font-semibold text-gray-800 dark:text-white">{task.title}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">Assigned to: {task.assigned_to}</p>
                </div>
                <div className="text-right">
                  <span className={`px-2 py-1 text-xs font-semibold rounded-full ${getStatusColor(task.status)}`}>
                    {task.status}
                  </span>
                  <p className={`text-sm mt-1 ${getPriorityColor(task.priority)}`}>{task.priority} Priority</p>
                </div>
              </motion.div>
            )) : <p className="text-gray-500 dark:text-gray-400">No tasks found.</p>}
          </div>
        </div>

        {/* Portfolio */}
        <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg">
          <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Portfolio</h2>
          <ul className="space-y-4">
            {(dashboardData.portfolio && dashboardData.portfolio.length > 0) ? dashboardData.portfolio.map((item: any) => (
              <li key={item.id} className="flex items-center space-x-4">
                <div className={`p-2 rounded-full`}>
                  <TrendingUp className="h-5 w-5" />
                </div>
                <div>
                  <p className="font-semibold text-gray-800 dark:text-white">{item.symbol}</p>
                  <p className="text-sm text-gray-500 dark:text-gray-400">{item.quantity} @ ${item.average_cost}</p>
                </div>
              </li>
            )) : <p className="text-gray-500 dark:text-gray-400">No portfolio items found.</p>}
          </ul>
        </div>
      </div>

      {/* Recent Expenses */}
      <div className="bg-white dark:bg-gray-800 rounded-2xl p-6 shadow-lg">
        <h2 className="text-xl font-bold mb-4 text-gray-800 dark:text-white">Recent Expenses</h2>
        <div className="overflow-x-auto">
          <table className="w-full text-left">
            <thead>
              <tr className="text-gray-500 dark:text-gray-400">
                <th className="p-2">Date</th>
                <th className="p-2">Category</th>
                <th className="p-2">Description</th>
                <th className="p-2 text-right">Amount</th>
              </tr>
            </thead>
            <tbody>
              {(dashboardData.expenses && dashboardData.expenses.length > 0) ? dashboardData.expenses.map((expense: any) => (
                <tr key={expense.id} className="border-b border-gray-200 dark:border-gray-700">
                  <td className="p-2 text-gray-600 dark:text-gray-300">{new Date(expense.date).toLocaleDateString()}</td>
                  <td className="p-2 text-gray-600 dark:text-gray-300">{expense.category}</td>
                  <td className="p-2 font-semibold text-gray-800 dark:text-white">{expense.description}</td>
                  <td className="p-2 text-right font-semibold text-red-500">-${expense.amount.toFixed(2)}</td>
                </tr>
              )) : <tr><td colSpan={4} className="text-center p-4 text-gray-500 dark:text-gray-400">No expenses found.</td></tr>}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;