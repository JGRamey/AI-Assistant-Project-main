import React from 'react';
import { motion } from 'framer-motion';
import { 
  CheckSquare, 
  FolderOpen, 
  Users, 
  Clock, 
  TrendingUp, 
  Brain,
  Zap,
  Target
} from 'lucide-react';

const Dashboard: React.FC = () => {
  const stats = [
    { label: 'Active Tasks', value: '12', change: '+3 today', icon: CheckSquare, color: 'from-green-500 to-green-600' },
    { label: 'Projects', value: '4', change: '2 in progress', icon: FolderOpen, color: 'from-purple-500 to-purple-600' },
    { label: 'AI Agents', value: '8', change: '6 active', icon: Users, color: 'from-orange-500 to-orange-600' },
    { label: 'Productivity', value: '87%', change: '+5% this week', icon: TrendingUp, color: 'from-blue-500 to-blue-600' },
  ];

  const recentTasks = [
    { id: 1, title: 'Review project proposal', status: 'In Progress', assignedTo: 'Research Agent', priority: 'High', time: '2 hours ago' },
    { id: 2, title: 'Schedule team meeting', status: 'Completed', assignedTo: 'Calendar Agent', priority: 'Medium', time: '4 hours ago' },
    { id: 3, title: 'Analyze market trends', status: 'Pending', assignedTo: 'Analytics Agent', priority: 'High', time: '6 hours ago' },
    { id: 4, title: 'Draft email response', status: 'In Progress', assignedTo: 'Communication Agent', priority: 'Low', time: '8 hours ago' },
  ];

  const activeProjects = [
    { id: 1, name: 'Website Redesign', progress: 75, team: 'Design Team', deadline: '2024-02-15', status: 'On Track' },
    { id: 2, name: 'Mobile App Development', progress: 45, team: 'Dev Team', deadline: '2024-03-01', status: 'At Risk' },
    { id: 3, name: 'Marketing Campaign', progress: 90, team: 'Marketing Team', deadline: '2024-01-30', status: 'Ahead' },
  ];

  const aiAgentActivity = [
    { agent: 'Research Agent', task: 'Analyzing competitor strategies', status: 'Active', efficiency: 94 },
    { agent: 'Calendar Agent', task: 'Optimizing schedule conflicts', status: 'Active', efficiency: 98 },
    { agent: 'Analytics Agent', task: 'Processing performance data', status: 'Active', efficiency: 87 },
    { agent: 'Communication Agent', task: 'Drafting client responses', status: 'Idle', efficiency: 92 },
  ];

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Completed':
      case 'On Track':
      case 'Ahead':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'In Progress':
      case 'Active':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'Pending':
      case 'At Risk':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      case 'Idle':
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
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
        {stats.map((stat, index) => {
          const Icon = stat.icon;
          return (
            <motion.div
              key={index}
              className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all duration-300"
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ y: -2 }}
            >
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-1">
                    {stat.label}
                  </p>
                  <p className="text-2xl font-bold text-gray-900 dark:text-white">
                    {stat.value}
                  </p>
                  <p className="text-sm text-gray-500 dark:text-gray-500">
                    {stat.change}
                  </p>
                </div>
                <div className={`p-3 bg-gradient-to-r ${stat.color} rounded-lg`}>
                  <Icon className="h-6 w-6 text-white" />
                </div>
              </div>
            </motion.div>
          );
        })}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Recent Tasks */}
        <motion.div
          className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
          initial={{ opacity: 0, x: -20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.2 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Recent Tasks</h2>
            <Zap className="h-5 w-5 text-primary-600" />
          </div>
          <div className="space-y-4">
            {recentTasks.map((task, index) => (
              <motion.div
                key={task.id}
                className="p-4 rounded-lg bg-gray-50 dark:bg-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 transition-colors"
                initial={{ opacity: 0, x: -10 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="flex items-start justify-between">
                  <div className="flex-1">
                    <h3 className="font-semibold text-gray-900 dark:text-white">{task.title}</h3>
                    <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                      Assigned to: {task.assignedTo}
                    </p>
                  </div>
                  <div className="flex flex-col items-end space-y-1">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(task.status)}`}>
                      {task.status}
                    </span>
                    <span className={`text-xs font-medium ${getPriorityColor(task.priority)}`}>
                      {task.priority}
                    </span>
                  </div>
                </div>
                <p className="text-xs text-gray-500 dark:text-gray-500 mt-2">{task.time}</p>
              </motion.div>
            ))}
          </div>
        </motion.div>

        {/* Active Projects */}
        <motion.div
          className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
          initial={{ opacity: 0, x: 20 }}
          animate={{ opacity: 1, x: 0 }}
          transition={{ duration: 0.6, delay: 0.3 }}
        >
          <div className="flex items-center justify-between mb-6">
            <h2 className="text-xl font-bold text-gray-900 dark:text-white">Active Projects</h2>
            <Target className="h-5 w-5 text-secondary-600" />
          </div>
          <div className="space-y-4">
            {activeProjects.map((project, index) => (
              <motion.div
                key={project.id}
                className="p-4 rounded-lg bg-gray-50 dark:bg-gray-700"
                initial={{ opacity: 0, y: 10 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: index * 0.1 }}
              >
                <div className="flex items-center justify-between mb-3">
                  <h3 className="font-semibold text-gray-900 dark:text-white">{project.name}</h3>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                    {project.status}
                  </span>
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm">
                    <span className="text-gray-600 dark:text-gray-400">Progress</span>
                    <span className="font-medium text-gray-900 dark:text-white">{project.progress}%</span>
                  </div>
                  <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-2">
                    <motion.div
                      className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full"
                      initial={{ width: 0 }}
                      animate={{ width: `${project.progress}%` }}
                      transition={{ duration: 1, delay: index * 0.2 }}
                    />
                  </div>
                  <div className="flex justify-between text-xs text-gray-500 dark:text-gray-500">
                    <span>{project.team}</span>
                    <span>Due: {project.deadline}</span>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        </motion.div>
      </div>

      {/* AI Agent Activity */}
      <motion.div
        className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700"
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6, delay: 0.4 }}
      >
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-xl font-bold text-gray-900 dark:text-white">AI Agent Activity</h2>
          <Users className="h-5 w-5 text-accent-600" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          {aiAgentActivity.map((agent, index) => (
            <motion.div
              key={index}
              className="p-4 rounded-lg bg-gradient-to-r from-gray-50 to-gray-100 dark:from-gray-700 dark:to-gray-600"
              initial={{ opacity: 0, scale: 0.9 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ delay: index * 0.1 }}
            >
              <div className="flex items-center justify-between mb-2">
                <h3 className="font-semibold text-gray-900 dark:text-white">{agent.agent}</h3>
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(agent.status)}`}>
                  {agent.status}
                </span>
              </div>
              <p className="text-sm text-gray-600 dark:text-gray-400 mb-3">{agent.task}</p>
              <div className="flex items-center justify-between">
                <span className="text-xs text-gray-500 dark:text-gray-500">Efficiency</span>
                <span className="text-sm font-medium text-gray-900 dark:text-white">{agent.efficiency}%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-600 rounded-full h-1.5 mt-1">
                <motion.div
                  className="bg-gradient-to-r from-accent-500 to-accent-600 h-1.5 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${agent.efficiency}%` }}
                  transition={{ duration: 1, delay: index * 0.2 }}
                />
              </div>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
};

export default Dashboard;