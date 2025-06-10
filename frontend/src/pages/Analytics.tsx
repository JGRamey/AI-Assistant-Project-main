import React, { useState } from 'react';
import { motion } from 'framer-motion';
import { 
  TrendingUp, 
  Calendar, 
  Filter, 
  BarChart3, 
  PieChart, 
  Activity,
  Clock,
  Target,
  Zap
} from 'lucide-react';

const Analytics: React.FC = () => {
  const [timeRange, setTimeRange] = useState('30d');
  const [selectedMetric, setSelectedMetric] = useState('productivity');

  const analyticsData = [
    { label: 'Tasks Completed', value: '127', change: '+12%', positive: true, icon: Target },
    { label: 'Productivity Score', value: '87%', change: '+5%', positive: true, icon: TrendingUp },
    { label: 'AI Agent Efficiency', value: '94%', change: '+3%', positive: true, icon: Zap },
    { label: 'Average Response Time', value: '2.3s', change: '-15%', positive: true, icon: Clock },
  ];

  const productivityData = [
    { day: 'Mon', tasks: 18, efficiency: 92 },
    { day: 'Tue', tasks: 22, efficiency: 88 },
    { day: 'Wed', tasks: 15, efficiency: 95 },
    { day: 'Thu', tasks: 28, efficiency: 91 },
    { day: 'Fri', tasks: 24, efficiency: 89 },
    { day: 'Sat', tasks: 12, efficiency: 94 },
    { day: 'Sun', tasks: 8, efficiency: 96 },
  ];

  const agentPerformance = [
    { name: 'Research Agent', tasks: 45, efficiency: 94, color: 'bg-blue-500' },
    { name: 'Calendar Agent', tasks: 32, efficiency: 98, color: 'bg-green-500' },
    { name: 'Content Agent', tasks: 38, efficiency: 87, color: 'bg-purple-500' },
    { name: 'Analytics Agent', tasks: 28, efficiency: 91, color: 'bg-orange-500' },
    { name: 'Communication Agent', tasks: 41, efficiency: 92, color: 'bg-pink-500' },
  ];

  const taskCategories = [
    { category: 'Research', count: 45, percentage: 35, color: 'bg-blue-500' },
    { category: 'Communication', count: 32, percentage: 25, color: 'bg-green-500' },
    { category: 'Content Creation', count: 28, percentage: 22, color: 'bg-purple-500' },
    { category: 'Analysis', count: 23, percentage: 18, color: 'bg-orange-500' },
  ];

  const recentInsights = [
    {
      title: 'Peak Productivity Hours',
      description: 'Your highest productivity occurs between 9-11 AM with 95% efficiency',
      type: 'time',
      impact: 'high'
    },
    {
      title: 'Agent Optimization',
      description: 'Research Agent shows 15% improvement in task completion speed',
      type: 'performance',
      impact: 'medium'
    },
    {
      title: 'Task Distribution',
      description: 'Consider delegating more analysis tasks to optimize workload',
      type: 'recommendation',
      impact: 'medium'
    },
    {
      title: 'Weekly Goal Achievement',
      description: 'Exceeded weekly task completion goal by 23%',
      type: 'achievement',
      impact: 'high'
    }
  ];

  const getImpactColor = (impact: string) => {
    switch (impact) {
      case 'high':
        return 'border-l-green-500 bg-green-50 dark:bg-green-900/20';
      case 'medium':
        return 'border-l-yellow-500 bg-yellow-50 dark:bg-yellow-900/20';
      default:
        return 'border-l-blue-500 bg-blue-50 dark:bg-blue-900/20';
    }
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Analytics Dashboard</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Insights into your productivity and AI agent performance
          </p>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <Calendar className="h-4 w-4 text-gray-500" />
            <select
              value={timeRange}
              onChange={(e) => setTimeRange(e.target.value)}
              className="border border-gray-300 dark:border-gray-600 rounded-lg px-3 py-2 text-sm bg-white dark:bg-gray-700 text-gray-900 dark:text-white focus:ring-2 focus:ring-primary-500 focus:border-transparent"
            >
              <option value="7d">Last 7 days</option>
              <option value="30d">Last 30 days</option>
              <option value="90d">Last 90 days</option>
              <option value="1y">Last year</option>
            </select>
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 border border-gray-300 dark:border-gray-600 rounded-lg text-sm font-medium text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors">
            <Filter className="h-4 w-4" />
            <span>Filter</span>
          </button>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {analyticsData.map((metric, index) => {
          const Icon = metric.icon;
          return (
            <motion.div
              key={index}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-md transition-shadow"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                    {metric.label}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {metric.value}
                  </p>
                  <p className={`text-sm font-medium ${
                    metric.positive ? 'text-green-600' : 'text-red-600'
                  }`}>
                    {metric.change}
                  </p>
                </div>
                <div className="p-3 bg-primary-100 dark:bg-primary-900 rounded-lg">
                  <Icon className="h-6 w-6 text-primary-600 dark:text-primary-400" />
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Productivity Chart */}
        <motion.div
          className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Weekly Productivity</h2>
            <BarChart3 className="h-5 w-5 text-primary-600" />
          </div>
          <div className="space-y-4">
            {productivityData.map((day, index) => (
              <div key={day.day} className="flex items-center space-x-4">
                <div className="w-12 text-sm font-medium text-gray-600 dark:text-gray-400">
                  {day.day}
                </div>
                <div className="flex-1">
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-sm text-gray-600 dark:text-gray-400">Tasks: {day.tasks}</span>
                    <span className="text-sm font-medium text-gray-900 dark:text-white">{day.efficiency}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                    <motion.div
                      className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: `${day.efficiency}%` }}
                      transition={{ duration: 1, delay: index * 0.1 }}
                    />
                  </div>
                </div>
              </div>
            ))}
          </div>
        </motion.div>

        {/* Agent Performance */}
        <motion.div
          className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ delay: 0.3 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Agent Performance</h2>
            <Activity className="h-5 w-5 text-secondary-600" />
          </div>
          <div className="space-y-4">
            {agentPerformance.map((agent, index) => (
              <motion.div
                key={agent.name}
                className="p-4 rounded-lg bg-gray-50 dark:bg-gray-700"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="flex items-center justify-between mb-2">
                  <h3 className="font-semibold text-gray-900 dark:text-white">{agent.name}</h3>
                  <span className="text-sm font-medium text-gray-600 dark:text-gray-400">
                    {agent.efficiency}%
                  </span>
                </div>
                <div className="flex items-center space-x-3">
                  <div className="flex-1">
                    <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                      <motion.div
                        className={`${agent.color} h-2 rounded-full`}
                        initial={{ width: 0 }}
                        animate={{ width: `${agent.efficiency}%` }}
                        transition={{ duration: 1, delay: index * 0.2 }}
                      />
                    </div>
                  </div>
                  <span className="text-sm text-gray-600 dark:text-gray-400">
                    {agent.tasks} tasks
                  </span>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* Task Categories */}
      <motion.div
        className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.4 }}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">Task Distribution</h2>
          <PieChart className="h-5 w-5 text-accent-600" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {taskCategories.map((category, index) => (
            <motion.div
              key={category.category}
              className="text-center"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="relative w-24 h-24 mx-auto mb-4">
                <svg className="w-24 h-24 transform -rotate-90" viewBox="0 0 36 36">
                  <path
                    className="text-gray-200 dark:text-gray-700"
                    stroke="currentColor"
                    strokeWidth="3"
                    fill="none"
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                  />
                  <motion.path
                    className={category.color.replace('bg-', 'text-')}
                    stroke="currentColor"
                    strokeWidth="3"
                    strokeLinecap="round"
                    fill="none"
                    strokeDasharray={`${category.percentage}, 100`}
                    d="M18 2.0845 a 15.9155 15.9155 0 0 1 0 31.831 a 15.9155 15.9155 0 0 1 0 -31.831"
                    initial={{ strokeDasharray: "0, 100" }}
                    animate={{ strokeDasharray: `${category.percentage}, 100` }}
                    transition={{ duration: 1, delay: index * 0.2 }}
                  />
                </svg>
                <div className="absolute inset-0 flex items-center justify-center">
                  <span className="text-lg font-bold text-gray-900 dark:text-white">
                    {category.percentage}%
                  </span>
                </div>
              </div>
              <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                {category.category}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {category.count} tasks
              </p>
            </motion.div>
          ))}
        </div>
      </motion.div>

      {/* Insights */}
      <motion.div
        className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <h2 className="text-xl font-bold text-gray-900 dark:text-white mb-6">AI Insights & Recommendations</h2>
        <div className="space-y-4">
          {recentInsights.map((insight, index) => (
            <motion.div
              key={index}
              className={`p-4 rounded-lg border-l-4 ${getImpactColor(insight.impact)}`}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <h3 className="font-semibold text-gray-900 dark:text-white mb-1">
                {insight.title}
              </h3>
              <p className="text-gray-600 dark:text-gray-400 text-sm">
                {insight.description}
              </p>
              <div className="flex items-center justify-between mt-2">
                <span className="text-xs text-gray-500 dark:text-gray-500 capitalize">
                  {insight.type}
                </span>
                <span className={`text-xs font-medium px-2 py-1 rounded-full ${
                  insight.impact === 'high' 
                    ? 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200'
                    : insight.impact === 'medium'
                    ? 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200'
                    : 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200'
                }`}>
                  {insight.impact} impact
                </span>
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Analytics;