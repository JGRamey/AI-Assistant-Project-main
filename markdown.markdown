AI Assistant Project
A modular AI system with agent-based task delegation, blockchain integration, and platform services.
Setup
python3.13 -m venv venv
source venv/bin/activate
export PYTHONPATH=$PWD/src
pip install -r requirements.txt
pytest tests/unit/
cd frontend && npm install && npm test

Structure

src/agents/: Agent implementations.
src/blockchain/: Smart contract management.
src/lambda/: Lambda handler.
src/platform/: Platform services.
tests/unit/: Unit tests.

