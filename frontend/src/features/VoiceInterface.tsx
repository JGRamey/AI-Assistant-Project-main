import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Mic, MicOff, Volume2, MessageSquare } from 'lucide-react';

interface VoiceInterfaceProps {
  isListening: boolean;
  onToggleListening: () => void;
  onNavigate: (page: string) => void;
  onShowInterface: () => void;
}

const VoiceInterface: React.FC<VoiceInterfaceProps> = ({
  isListening,
  onToggleListening,
  onNavigate,
  onShowInterface
}) => {
  const [transcript, setTranscript] = useState('');
  const [response, setResponse] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);

  const recentCommands = [
    "Create a new project for website redesign",
    "Schedule meeting with development team",
    "Analyze last week's productivity metrics"
  ];

  const handleVoiceCommand = (command: string) => {
    setIsProcessing(true);
    
    // Simulate AI processing
    setTimeout(() => {
      setResponse(`Processing: "${command}". I'll handle this task and coordinate with the appropriate AI agents.`);
      setIsProcessing(false);
    }, 2000);
  };

  const pulseVariants = {
    listening: {
      scale: [1, 1.2, 1],
      opacity: [0.7, 1, 0.7],
      transition: {
        duration: 2,
        repeat: Infinity,
        ease: "easeInOut"
      }
    },
    idle: {
      scale: 1,
      opacity: 1
    }
  };

  const waveVariants = {
    listening: {
      scale: [1, 1.5, 1],
      opacity: [0.3, 0.1, 0.3],
      transition: {
        duration: 3,
        repeat: Infinity,
        ease: "easeInOut"
      }
    },
    idle: {
      scale: 1,
      opacity: 0.1
    }
  };

  return (
    <div className="fixed inset-0 flex flex-col overflow-hidden">
      {/* Background Waves - Subtle and professional */}
      <motion.div
        className="absolute inset-0 flex items-center justify-center pointer-events-none"
        variants={waveVariants}
        animate={isListening ? "listening" : "idle"}
      >
        <div className="w-[400px] h-[400px] rounded-full bg-gradient-to-r from-primary-500/8 to-secondary-500/8 blur-3xl" />
      </motion.div>

      <motion.div
        className="absolute inset-0 flex items-center justify-center pointer-events-none"
        variants={waveVariants}
        animate={isListening ? "listening" : "idle"}
        transition={{ delay: 0.5 }}
      >
        <div className="w-[300px] h-[300px] rounded-full bg-gradient-to-r from-secondary-500/8 to-accent-500/8 blur-2xl" />
      </motion.div>

      {/* Main Content Container - Positioned below navigation */}
      <div className="relative z-10 flex flex-col items-center pt-56 px-8 h-full">
        
        {/* Central Voice Interface */}
        <motion.div
          className="flex flex-col items-center space-y-6"
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          {/* Main Voice Button - Smaller and properly sized */}
          <motion.button
            onClick={onToggleListening}
            className={`relative w-24 h-24 rounded-full flex items-center justify-center transition-all duration-500 ${
              isListening
                ? 'bg-gradient-to-r from-red-500 to-red-600 shadow-xl shadow-red-500/25'
                : 'bg-gradient-to-r from-primary-600 to-secondary-600 shadow-xl shadow-primary-500/25 hover:shadow-primary-500/40'
            }`}
            variants={pulseVariants}
            animate={isListening ? "listening" : "idle"}
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
          >
            {isListening ? (
              <MicOff className="h-8 w-8 text-white" />
            ) : (
              <Mic className="h-8 w-8 text-white" />
            )}
            
            {/* Pulse rings */}
            {isListening && (
              <>
                <motion.div
                  className="absolute inset-0 rounded-full border-2 border-white/30"
                  animate={{
                    scale: [1, 1.5, 2],
                    opacity: [0.5, 0.2, 0]
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeOut"
                  }}
                />
                <motion.div
                  className="absolute inset-0 rounded-full border-2 border-white/30"
                  animate={{
                    scale: [1, 1.5, 2],
                    opacity: [0.5, 0.2, 0]
                  }}
                  transition={{
                    duration: 2,
                    repeat: Infinity,
                    ease: "easeOut",
                    delay: 0.5
                  }}
                />
              </>
            )}
          </motion.button>

          {/* Status Text */}
          <motion.div
            className="text-center space-y-2"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
          >
            <h2 className="text-2xl font-bold text-gray-900 dark:text-white">
              {isListening ? 'Listening...' : 'Ready to Assist'}
            </h2>
            <p className="text-gray-600 dark:text-gray-400 max-w-md">
              {isListening 
                ? 'Speak your command and I\'ll coordinate with AI agents'
                : 'Click the microphone to get started'
              }
            </p>
          </motion.div>

          {/* Processing Indicator */}
          {isProcessing && (
            <motion.div
              className="flex items-center space-x-2 text-primary-600"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              <motion.div
                className="w-2 h-2 bg-primary-600 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.8, repeat: Infinity }}
              />
              <motion.div
                className="w-2 h-2 bg-primary-600 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.8, repeat: Infinity, delay: 0.2 }}
              />
              <motion.div
                className="w-2 h-2 bg-primary-600 rounded-full"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 0.8, repeat: Infinity, delay: 0.4 }}
              />
              <span className="text-sm font-medium ml-2">Processing...</span>
            </motion.div>
          )}
        </motion.div>

        {/* Recent Commands - Positioned at bottom with proper spacing */}
        {/* Recent Commands - Completely centered approach */}
        <div className="absolute bottom-0 left-0 right-0 flex justify-center pb-8">
          <motion.div
            className="bg-white/70 dark:bg-gray-800/70 backdrop-blur-lg rounded-2xl p-6 w-full max-w-2xl mx-8"
            initial={{ opacity: 0, y: 30 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.6 }}
          >
            <h3 className="text-lg font-semibold text-gray-700 dark:text-gray-300 mb-4 text-center">
              Recent Commands
            </h3>
            <div className="grid grid-cols-1 gap-3">
              {recentCommands.map((command, index) => (
                <motion.button
                  key={index}
                  onClick={() => handleVoiceCommand(command)}
                  className="w-full text-center text-sm text-gray-600 dark:text-gray-400 hover:text-primary-600 dark:hover:text-primary-400 transition-all duration-300 p-3 rounded-xl hover:bg-white/60 dark:hover:bg-gray-700/60 hover:shadow-md"
                  whileHover={{ scale: 1.02 }}
                  whileTap={{ scale: 0.98 }}
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.8 + index * 0.1 }}
                >
                  <div className="flex items-center justify-center space-x-3">
                    <div className="w-1.5 h-1.5 bg-primary-500 rounded-full opacity-60" />
                    <span>"{command}"</span>
                    <div className="w-1.5 h-1.5 bg-primary-500 rounded-full opacity-60" />
                  </div>
                </motion.button>
              ))}
            </div>
          </motion.div>
        </div>
      </div>

      {/* Transcript Display - Bottom left corner */}
      {transcript && (
        <motion.div
          className="absolute bottom-8 left-8 bg-white/95 dark:bg-gray-800/95 backdrop-blur-lg rounded-xl p-4 max-w-sm shadow-lg"
          initial={{ opacity: 0, scale: 0.9, x: -20 }}
          animate={{ opacity: 1, scale: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <div className="flex items-center space-x-2 mb-2">
            <MessageSquare className="h-4 w-4 text-primary-600" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">You said:</span>
          </div>
          <p className="text-sm text-gray-900 dark:text-white leading-relaxed">{transcript}</p>
        </motion.div>
      )}

      {/* Response Display - Bottom right corner */}
      {response && (
        <motion.div
          className="absolute bottom-8 right-8 bg-gradient-to-r from-primary-50 to-secondary-50 dark:from-primary-900/60 dark:to-secondary-900/60 backdrop-blur-lg rounded-xl p-4 max-w-sm shadow-lg"
          initial={{ opacity: 0, scale: 0.9, x: 20 }}
          animate={{ opacity: 1, scale: 1, x: 0 }}
          transition={{ duration: 0.3 }}
        >
          <div className="flex items-center space-x-2 mb-2">
            <Volume2 className="h-4 w-4 text-primary-600" />
            <span className="text-sm font-medium text-gray-700 dark:text-gray-300">Assistant:</span>
          </div>
          <p className="text-sm text-gray-900 dark:text-white leading-relaxed">{response}</p>
        </motion.div>
      )}
    </div>
  );
};

export default VoiceInterface;