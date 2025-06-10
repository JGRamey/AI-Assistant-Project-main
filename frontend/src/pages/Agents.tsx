import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Bot, 
  Brain, 
  Zap, 
  Settings, 
  Play, 
  Pause, 
  RotateCcw,
  Activity,
  Clock,
  CheckCircle,
  AlertCircle,
  Plus
} from 'lucide-react';

interface Agent {
  id: number;
  name: string;
  type: string;
  description: string;
  status: 'active' | 'idle' | 'busy' | 'offline';
  efficiency: number;
  tasksCompleted: number;
  currentTask: string | null;
  capabilities: string[];
  lastActive: string;
  uptime: string;
}

const Agents: React.FC = () => {
  const [agents, setAgents] = useState<Agent[]>([
    {
      id: 1,
      name: 'Research Agent',
      type: 'Research & Analysis',
      description: 'Specialized in market research, competitor analysis, and data gathering',
      status: 'active',
      efficiency: 94,
      tasksCompleted: 127,
      currentTask: 'Analyzing competitor pricing strategies',
      capabilities: ['Web Scraping', 'Data Analysis', 'Report Generation', 'Market Research'],
      lastActive: '2 minutes ago',
      uptime: '99.2%'
    },
    {
      id: 2,
      name: 'Calendar Agent',
      type: 'Scheduling & Organization',
      description: 'Manages schedules, meetings, and time optimization',
      status: 'active',
      efficiency: 98,
      tasksCompleted: 89,
      currentTask: 'Optimizing weekly schedule conflicts',
      capabilities: ['Calendar Management', 'Meeting Scheduling', 'Time Optimization', 'Reminders'],
      lastActive: '1 minute ago',
      uptime: '99.8%'
    },
    {
      id: 3,
      name: 'Content Agent',
      type: 'Content Creation',
      description: 'Creates and manages content across various platforms',
      status: 'busy',
      efficiency: 87,
      tasksCompleted: 156,
      currentTask: 'Drafting blog post about AI trends',
      capabilities: ['Writing', 'Editing', 'SEO Optimization', 'Social Media'],
      lastActive: 'Active now',
      uptime: '97.5%'
    },
    {
      id: 4,
      name: 'Analytics Agent',
      type: 'Data Analytics',
      description: 'Processes data and generates insights and reports',
      status: 'idle',
      efficiency: 91,
      tasksCompleted: 203,
      currentTask: null,
      capabilities: ['Data Processing', 'Statistical Analysis', 'Visualization', 'Reporting'],
      lastActive: '15 minutes ago',
      uptime: '98.1%'
    },
    {
      id: 5,
      name: 'Communication Agent',
      type: 'Communication',
      description: 'Handles emails, messages, and client communications',
      status: 'active',
      efficiency: 92,
      tasksCompleted: 78,
      currentTask: 'Responding to client inquiries',
      capabilities: ['Email Management', 'Client Communication', 'Language Translation', 'Sentiment Analysis'],
      lastActive: '5 minutes ago',
      uptime: '99.5%'
    },
    {
      id: 6,
      name: 'Development Agent',
      type: 'Software Development',
      description: 'Assists with coding, debugging, and development tasks',
      status: 'offline',
      efficiency: 89,
      tasksCompleted: 45,
      currentTask: null,
      capabilities: ['Code Generation', 'Debugging', 'Testing', 'Documentation'],
      lastActive: '2 hours ago',
      uptime: '95.3%'
    }
  ]);

  const [selectedAgent, setSelectedAgent] = useState<Agent | null>(null);

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircle className="h-5 w-5 text-green-500" />;
      case 'busy':
        return <Activity className="h-5 w-5 text-blue-500" />;
      case 'idle':
        return <Clock className="h-5 w-5 text-yellow-500" />;
      default:
        return <AlertCircle className="h-5 w-5 text-gray-500" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200';
      case 'busy':
        return 'bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200';
      case 'idle':
        return 'bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200';
      default:
        return 'bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300';
    }
  };

  const toggleAgentStatus = (agentId: number) => {
    setAgents(agents.map(agent => {
      if (agent.id === agentId) {
        const newStatus = agent.status === 'active' ? 'idle' : 'active';
        return { ...agent, status: newStatus };
      }
      return agent;
    }));
  };

  const restartAgent = (agentId: number) => {
    setAgents(agents.map(agent => {
      if (agent.id === agentId) {
        return { ...agent, status: 'active', currentTask: null };
      }
      return agent;
    }));
  };

  return (
    <div className="space-y-8">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center space-y-4 sm:space-y-0">
        <div>
          <h1 className="text-3xl font-bold text-gray-900 dark:text-white">AI Agent Management</h1>
          <p className="text-gray-600 dark:text-gray-400 mt-2">
            Monitor and control your AI assistants and their tasks
          </p>
        </div>
        
        <motion.button
          className="flex items-center px-6 py-3 bg-gradient-to-r from-primary-600 to-secondary-600 text-white rounded-lg hover:from-primary-700 hover:to-secondary-700 transition-all duration-300 shadow-lg"
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
        >
          <Plus className="h-5 w-5 mr-2" />
          Add Agent
        </motion.button>
      </div>

      {/* Agent Stats */}
      <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
        {[
          { label: 'Total Agents', count: agents.length, color: 'from-gray-500 to-gray-600' },
          { label: 'Active', count: agents.filter(a => a.status === 'active').length, color: 'from-green-500 to-green-600' },
          { label: 'Busy', count: agents.filter(a => a.status === 'busy').length, color: 'from-blue-500 to-blue-600' },
          { label: 'Offline', count: agents.filter(a => a.status === 'offline').length, color: 'from-red-500 to-red-600' }
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
                <Bot className="h-4 w-4 text-white" />
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Agent Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
        {agents.map((agent, index) => (
          <motion.div
            key={agent.id}
            className="bg-white dark:bg-gray-800 rounded-xl p-6 shadow-sm border border-gray-200 dark:border-gray-700 hover:shadow-lg transition-all duration-300"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: index * 0.1 }}
            whileHover={{ y: -2 }}
          >
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className="p-2 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg">
                  <Brain className="h-6 w-6 text-white" />
                </div>
                <div>
                  <h3 className="text-lg font-semibold text-gray-900 dark:text-white">
                    {agent.name}
                  </h3>
                  <p className="text-sm text-gray-600 dark:text-gray-400">{agent.type}</p>
                </div>
              </div>
              <div className="flex items-center space-x-1">
                {getStatusIcon(agent.status)}
                <span className={`inline-flex items-center px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(agent.status)}`}>
                  {agent.status}
                </span>
              </div>
            </div>

            <p className="text-gray-600 dark:text-gray-400 mb-4 text-sm">
              {agent.description}
            </p>

            {/* Current Task */}
            {agent.currentTask && (
              <div className="mb-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg">
                <p className="text-sm font-medium text-blue-800 dark:text-blue-200 mb-1">
                  Current Task:
                </p>
                <p className="text-sm text-blue-700 dark:text-blue-300">
                  {agent.currentTask}
                </p>
              </div>
            )}

            {/* Efficiency */}
            <div className="mb-4">
              <div className="flex justify-between text-sm mb-2">
                <span className="text-gray-600 dark:text-gray-400">Efficiency</span>
                <span className="font-medium text-gray-900 dark:text-white">{agent.efficiency}%</span>
              </div>
              <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                <motion.div
                  className="bg-gradient-to-r from-accent-500 to-accent-600 h-2 rounded-full"
                  initial={{ width: 0 }}
                  animate={{ width: `${agent.efficiency}%` }}
                  transition={{ duration: 1, delay: index * 0.2 }}
                />
              </div>
            </div>

            {/* Stats */}
            <div className="grid grid-cols-2 gap-4 mb-4 text-sm">
              <div>
                <p className="text-gray-600 dark:text-gray-400">Tasks Completed</p>
                <p className="font-semibold text-gray-900 dark:text-white">{agent.tasksCompleted}</p>
              </div>
              <div>
                <p className="text-gray-600 dark:text-gray-400">Uptime</p>
                <p className="font-semibold text-gray-900 dark:text-white">{agent.uptime}</p>
              </div>
            </div>

            {/* Capabilities */}
            <div className="mb-4">
              <p className="text-sm font-medium text-gray-600 dark:text-gray-400 mb-2">Capabilities</p>
              <div className="flex flex-wrap gap-1">
                {agent.capabilities.slice(0, 3).map((capability, capIndex) => (
                  <span
                    key={capIndex}
                    className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300"
                  >
                    {capability}
                  </span>
                ))}
                {agent.capabilities.length > 3 && (
                  <span className="inline-flex items-center px-2 py-1 rounded-md text-xs font-medium bg-gray-100 text-gray-800 dark:bg-gray-700 dark:text-gray-300">
                    +{agent.capabilities.length - 3} more
                  </span>
                )}
              </div>
            </div>

            {/* Controls */}
            <div className="flex items-center justify-between pt-4 border-t border-gray-200 dark:border-gray-700">
              <p className="text-xs text-gray-500 dark:text-gray-500">
                Last active: {agent.lastActive}
              </p>
              <div className="flex space-x-2">
                <motion.button
                  onClick={() => toggleAgentStatus(agent.id)}
                  className={`p-2 rounded-lg transition-colors ${
                    agent.status === 'active' 
                      ? 'text-yellow-600 hover:bg-yellow-50 dark:hover:bg-yellow-900/20' 
                      : 'text-green-600 hover:bg-green-50 dark:hover:bg-green-900/20'
                  }`}
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  {agent.status === 'active' ? <Pause className="h-4 w-4" /> : <Play className="h-4 w-4" />}
                </motion.button>
                <motion.button
                  onClick={() => restartAgent(agent.id)}
                  className="p-2 text-blue-600 hover:bg-blue-50 dark:hover:bg-blue-900/20 rounded-lg transition-colors"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <RotateCcw className="h-4 w-4" />
                </motion.button>
                <motion.button
                  onClick={() => setSelectedAgent(agent)}
                  className="p-2 text-gray-600 hover:bg-gray-50 dark:hover:bg-gray-700 rounded-lg transition-colors"
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                >
                  <Settings className="h-4 w-4" />
                </motion.button>
              </div>
            </div>
          </motion.div>
        ))}
      </div>

      {/* Agent Detail Modal */}
      <AnimatePresence>
        {selectedAgent && (
          <motion.div
            className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            onClick={() => setSelectedAgent(null)}
          >
            <motion.div
              className="bg-white dark:bg-gray-800 rounded-xl p-6 max-w-2xl w-full max-h-[80vh] overflow-y-auto"
              initial={{ scale: 0.9, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.9, opacity: 0 }}
              onClick={(e) => e.stopPropagation()}
            >
              <div className="flex items-start justify-between mb-6">
                <div className="flex items-center space-x-3">
                  <div className="p-3 bg-gradient-to-r from-primary-500 to-secondary-500 rounded-lg">
                    <Brain className="h-8 w-8 text-white" />
                  </div>
                  <div>
                    <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
                      {selectedAgent.name}
                    </h2>
                    <p className="text-gray-600 dark:text-gray-400">{selectedAgent.type}</p>
                  </div>
                </div>
                <button
                  onClick={() => setSelectedAgent(null)}
                  className="text-gray-500 hover:text-gray-700 dark:text-gray-400 dark:hover:text-gray-200"
                >
                  ✕
                </button>
              </div>

              <div className="space-y-6">
                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Description</h3>
                  <p className="text-gray-600 dark:text-gray-400">{selectedAgent.description}</p>
                </div>

                <div>
                  <h3 className="font-semibold text-gray-900 dark:text-white mb-3">All Capabilities</h3>
                  <div className="grid grid-cols-2 gap-2">
                    {selectedAgent.capabilities.map((capability, index) => (
                      <span
                        key={index}
                        className="inline-flex items-center px-3 py-2 rounded-lg text-sm font-medium bg-primary-100 text-primary-800 dark:bg-primary-900 dark:text-primary-200"
                      >
                        <Zap className="h-4 w-4 mr-2" />
                        {capability}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="grid grid-cols-2 gap-6">
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Performance</h3>
                    <div className="space-y-3">
                      <div>
                        <div className="flex justify-between text-sm mb-1">
                          <span>Efficiency</span>
                          <span>{selectedAgent.efficiency}%</span>
                        </div>
                        <div className="w-full bg-gray-200 dark:bg-gray-700 rounded-full h-2">
                          <div
                            className="bg-gradient-to-r from-accent-500 to-accent-600 h-2 rounded-full"
                            style={{ width: `${selectedAgent.efficiency}%` }}
                          />
                        </div>
                      </div>
                      <div className="text-sm">
                        <span className="text-gray-600 dark:text-gray-400">Tasks Completed: </span>
                        <span className="font-medium">{selectedAgent.tasksCompleted}</span>
                      </div>
                      <div className="text-sm">
                        <span className="text-gray-600 dark:text-gray-400">Uptime: </span>
                        <span className="font-medium">{selectedAgent.uptime}</span>
                      </div>
                    </div>
                  </div>
                  <div>
                    <h3 className="font-semibold text-gray-900 dark:text-white mb-2">Status</h3>
                    <div className="space-y-3">
                      <div className="flex items-center space-x-2">
                        {getStatusIcon(selectedAgent.status)}
                        <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-sm font-medium ${getStatusColor(selectedAgent.status)}`}>
                          {selectedAgent.status}
                        </span>
                      </div>
                      {selectedAgent.currentTask && (
                        <div>
                          <p className="text-sm text-gray-600 dark:text-gray-400 mb-1">Current Task:</p>
                          <p className="text-sm font-medium">{selectedAgent.currentTask}</p>
                        </div>
                      )}
                      <div className="text-sm">
                        <span className="text-gray-600 dark:text-gray-400">Last Active: </span>
                        <span className="font-medium">{selectedAgent.lastActive}</span>
                      </div>
                    </div>
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

export default Agents;