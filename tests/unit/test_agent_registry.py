import unittest
from unittest.mock import patch, MagicMock
import sys
import os
import importlib

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

# Mock potentially missing modules before importing the registry
# This allows testing the registry even if some agents are not yet created.
mock_modules = [
    'agents.notes_agent',
    'agents.voice_agent',
    'dashboard.dashboard',
    'workflows'
]
for module_name in mock_modules:
    if module_name not in sys.modules:
        sys.modules[module_name] = MagicMock()

from src.agents import agent_registry

class TestAgentRegistry(unittest.TestCase):

    def test_handler_registry_structure(self):
        """Test that the HANDLER_REGISTRY is a dictionary and contains essential handlers."""
        self.assertIsInstance(agent_registry.HANDLER_REGISTRY, dict)

        essential_handlers = [
            'code',
            'email',
            'trade',
            'priority',
            'news',
            'alert'
        ]

        for handler_name in essential_handlers:
            self.assertIn(handler_name, agent_registry.HANDLER_REGISTRY)
            self.assertTrue(callable(agent_registry.HANDLER_REGISTRY[handler_name]))



if __name__ == '__main__':
    unittest.main()
