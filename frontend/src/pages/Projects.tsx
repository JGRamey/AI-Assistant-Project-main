import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Plus, 
  FolderOpen, 
  Users, 
  Calendar, 
  Target,
  TrendingUp,
  Clock,
  CheckCircle,
  AlertTriangle
} from 'lucide-react';

interface Project {
  id: number;
  name: string;
  description: string;
  status: 'planning' | 'active' | 'on-hold' | 'completed';
  progress: number;
  team: string[];
  startDate: string;
  endDate: string;
  budget: number;
  spent: number;
  priority: 'low' | 'medium' | 'high';
  tasks: {
    total: number;
    completed: number;
    inProgress: number;
    pending: number;
  };
}

const Projects: React.FC = () => {
  const [projects, setProjects] = useState<Project[]>([
    {
      id: 1,
      name: 'Website Redesign',
      description: 'Complete overhaul of company website with modern design and improved UX',
      status: 'active',
      progress: 75,
      team: ['Design Agent', 'Development Agent', 'Content Agent'],
      startDate: '2024-01-01',
      endDate: '2024-02-15',
      budget: 50000,
      spent: 37500,
      priority: 'high',
      tasks: { total: 24, completed: 18, inProgress: 4, pending: 2 }
    },
    {
      id: 2,
      name: 'Mobile App Development',
      description: 'Native mobile application for iOS and Android platforms',
      status: 'active',
      progress: 45,
      team: ['Mobile Agent', 'UI/UX Agent', 'Testing Agent'],
      startDate: '2024-01-15',
      endDate: '2024-03-01',
      budget: 80000,
      spent: 36000,
      priority: 'high',
      tasks: { total: 32, completed: 14, inProgress: 8, pending: 10 }
    },
    {
      id: 3,
      name: 'Marketing Campaign',
      description: 'Q1 digital marketing campaign across multiple channels',
      status: 'completed',
      progress: 100,
      team: ['Marketing Agent', 'Content Agent', 'Analytics Agent'],
      startDate: '2023-12-01',
      endDate: '2024-01-30',
      budget: 25000,
      spent: 24500,
      priority: 'medium',
      tasks: { total: 16, completed: 16, inProgress: 0, pending: 0 }
    },
    {
      id: 4,
      name: 'Data Analytics Platform',
      description: 'Internal analytics platform for business intelligence',
      status: 'planning',
      progress: 15,
      team: ['Data Agent', 'Backend Agent'],
      startDate: '2024-02-01',
      endDate: '2024-04-30',
      budget: 120000,
      spent: 18000,
      priority: 'medium',
      tasks: { total: 8, completed: 1, inProgress: 2, pending: 5 }
    }
  ]);

  const [selectedProject, setSelectedProject] = useState<Project | null>(null);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'active':
        return <TrendingUp className="h-5 w-5 text-blue-500" />;
      case 'on-hold':
        return <AlertTriangle className="h-5 w-5 text-yellow-500" />;
      default:
        return <Clock className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'active':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'on-hold':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'high':
        return 'text-red-600 dark:text-red-400';
      case 'medium':
        return 'text-yellow-600 dark:text-yellow-400';
      default:
        return 'text-green-600 dark:text-green-400';
    }
  };

  const formatCurrency = (amount: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0
    }).format(amount);
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">Project Management</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Oversee and coordinate your projects with AI assistance
          </p>
        </div>
        
        <motion.button
          className="flex items-center px-6 py-3 bg-gradient-to-r from-primary-600 to-secondary-600 text-white rounded-lg hover:from-primary-700 hover:to-secondary-700 transition-all duration-300 shadow-lg"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Plus className="h-5 w-5 mr-2" />
          New Project
        </motion.button>
      </div>

      {/* Project Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Projects', count: projects.length, color: 'from-gray-500 to-gray-600' },
          { label: 'Active', count: projects.filter(p => p.status === 'active').length, color: 'from-blue-500 to-blue-600' },
          { label: 'Completed', count: projects.filter(p => p.status === 'completed').length, color: 'from-green-500 to-green-600' },
          { label: 'Planning', count: projects.filter(p => p.status === 'planning').length, color: 'from-purple-500 to-purple-600' }
        ].map((stat, index) => (
          <motion.div
            key={stat.label}
            className="bg-white dark:bg-gray-800 rounded-xl p-4 shadow-sm border border-gray-200 dark:border-gray-700"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
          >
            <div className="flex items-center justify-between">
              <div>
                <p className="text-sm font-medium text-gray-600 dark:text-gray-400">{stat.label}</p>
                <p className="text-2xl font-bold text-gray-900 dark:text-white">{stat.count}</p>
              </div>
              <div className={`p-2 bg-gradient-to-r ${stat.color} rounded-lg`}>
                <FolderOpen className="h-4 w-4 text-white" />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Project Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {projects.map((project, index) => (
          <motion.div
            key={project.id}
            className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all duration-300 cursor-pointer"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -2 }}
            onClick={() => setSelectedProject(project)}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                {getStatusIcon(project.status)}
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {project.name}
                  </h3>
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(project.status)}`}>
                    {project.status}
                  </span>
                </div>
              </div>
              <span className={`text-sm font-medium ${getPriorityColor(project.priority)}`}>
                {project.priority} priority
              </span>
            </div>

            <p className="text-gray-600 dark:text-gray-400 mb-4 line-clamp-2">
              {project.description}
            </p>

            {/* Progress Bar */}
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600 dark:text-gray-400">Progress</span>
                <span className="font-medium text-gray-900 dark:text-white">{project.progress}%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <motion.div
                  className="bg-gradient-to-r from-primary-500 to-secondary-500 h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${project.progress}%` }}
                  transition={{ duration: 1, delay: index * 0.2 }}
                />
              </div>
            </div>

            {/* Project Details */}
            <div className="grid grid-cols-2 gap-4 mb-4">
              <div>
                <div className="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-500 mb-1">
                  <Calendar className="h-4 w-4" />
                  <span>Timeline</span>
                </div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  {project.startDate} - {project.endDate}
                </p>
              </div>
              <div>
                <div className="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-500 mb-1">
                  <Target className="h-4 w-4" />
                  <span>Budget</span>
                </div>
                <p className="text-sm font-medium text-gray-900 dark:text-white">
                  {formatCurrency(project.spent)} / {formatCurrency(project.budget)}
                </p>
              </div>
            </div>

            {/* Team */}
            <div className="mb-4">
              <div className="flex items-center space-x-1 text-sm text-gray-500 dark:text-gray-500 mb-2">
                <Users className="h-4 w-4" />
                <span>Team ({project.team.length})</span>
              </div>
              <div className="flex flex-wrap gap-1">
                {project.team.map((member, memberIndex) => (
                  <span
                    key={memberIndex}
                    className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300"
                  >
                    {member}
                  </span>
                ))}
              </div>
            </div>

            {/* Task Summary */}
            <div className="grid grid-cols-4 gap-2 text-center">
              <div>
                <p className="text-lg font-bold text-green-600">{project.tasks.completed}</p>
                <p className="text-xs text-gray-500">Done</p>
              </div>
              <div>
                <p className="text-lg font-bold text-blue-600">{project.tasks.inProgress}</p>
                <p className="text-xs text-gray-500">Active</p>
              </div>
              <div>
                <p className="text-lg font-bold text-yellow-600">{project.tasks.pending}</p>
                <p className="text-xs text-gray-500">Pending</p>
              </div>
              <div>
                <p className="text-lg font-bold text-gray-600">{project.tasks.total}</p>
                <p className="text-xs text-gray-500">Total</p>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Project Detail Modal */}
      <AnimatePresence>
        {selectedProject && (
          <motion.div
            className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedProject(null)}
          >
            <motion.div
              className="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-start justify-between mb-6">
                <div>
                  <h2 className="text-2xl font-bold text-gray-900 dark:text-white mb-2">
                    {selectedProject.name}
                  </h2>
                  <p className="text-gray-600 dark:text-gray-400">
                    {selectedProject.description}
                  </p>
                </div>
                <button
                  onClick={() => setSelectedProject(null)}
                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  ✕
                </button>
              </div>

              {/* Detailed project information would go here */}
              <div className="space-y-6">
                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Project Status</h3>
                    <div className="flex items-center space-x-2">
                      {getStatusIcon(selectedProject.status)}
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(selectedProject.status)}`}>
                        {selectedProject.status}
                      </span>
                    </div>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Priority</h3>
                    <span className={`font-medium ${getPriorityColor(selectedProject.priority)}`}>
                      {selectedProject.priority} priority
                    </span>
                  </div>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Progress</h3>
                  <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3">
                    <div
                      className="bg-gradient-to-r from-primary-500 to-secondary-500 h-3 rounded-full"
                      style={{ width: `${selectedProject.progress}%` }}
                    />
                  </div>
                  <p className="text-sm text-gray-600 dark:text-gray-400 mt-1">
                    {selectedProject.progress}% complete
                  </p>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Team Members</h3>
                  <div className="flex flex-wrap gap-2">
                    {selectedProject.team.map((member, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200"
                      >
                        {member}
                      </span>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};

export default Projects;