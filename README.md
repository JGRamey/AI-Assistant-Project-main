My AI Assistant
A modular AI assistant built on AWS Lambda, using Python, xAI Grok API, and agents for coding, trading, journaling, and more. Features include voice interaction (Mimic 3), blockchain storage (Polygon/Filecoin/Arweave), and a web dashboard.
Setup
Prerequisites

Python 3.8+: Compatible with AWS Lambda runtime.
AWS Account: Free tier covers Lambda, S3, DynamoDB, SNS, SSM, Cognito.
API Keys:
xAI Grok API: Obtain from https://x.ai/api (~$0.15/month for ~2,500 tokens/day).
Coinbase API: Create at https://www.coinbase.com (free for trading).
TradingView: No direct API; uses ta library for technical analysis.
GitHub API: Personal access token from https://github.com/settings/tokens (free).
Google APIs: OAuth2 credentials for Gmail/Calendar from https://console.cloud.google.com (free tier).
Twitter API: Keys from https://developer.twitter.com (free tier).
Coingecko API: Free at https://www.coingecko.com/en/api (news agent).
FRED API: Free at https://fred.stlouisfed.org (M2 data for news agent).


Blockchain:
Polygon RPC: Free public node (e.g., https://polygon-rpc.com).
Filecoin/Arweave: Storage accounts (~$0.01/GB/month).


Voice Feature (Mimic 3):
Open-source TTS/STT server: https://github.com/MycroftAI/mimic3.
Requires a local/remote server (min: 4GB RAM, 2GB disk, Linux recommended).
Install: pip install mycroft-mimic3-tts, run server on port 59125.
Configure in config/config.json (mimic3 endpoint).



Installation

Clone the repository: git clone <your-repo-url>
Install Python dependencies: pip install -r requirements.txt
Configure config/config.json with API keys and endpoints.
Set up AWS IAM roles with permissions for Lambda, S3, DynamoDB, SNS, SSM, Cognito.
Deploy to Lambda: bash deploy.sh

AWS Services

Lambda: Hosts the main function and agents (free tier: 1M requests/month).
S3: Stores notes, journal audio (free tier: 5GB).
DynamoDB: Dashboard data, CRM contacts (free tier: 25GB).
SNS: Trade alerts (free tier: 1M publishes).
SSM: API key storage (free tier: 10K parameters).
Cognito: User authentication (free tier: 50K MAUs).

Features

Coding Agent: Generates Rust code, manages GitHub repos.
Trading Agent: Fetches Coinbase data, analyzes patterns with ta (emulates TradingView).
Journal Agent: Voice-to-text journaling with Mimic 3, audio storage in S3.
Update Agent: Logs system updates with Grok API summaries, stored in SQLite.
Dashboard: Flask-based UI for projects, chats, updates.
Blockchain: Stores encrypted data on Polygon/Filecoin/Arweave.
Voice: Mimic 3 for TTS (text-to-speech) and STT (speech-to-text).

Voice Feature Details

Mimic 3: Open-source TTS/STT for the voice_agent.
TTS: Converts text to audio (e.g., for reading journal entries).
STT: Transcribes audio to text (e.g., for journaling).
Setup:
Run Mimic 3 server: mimic3-server --port 59125.
Update config/config.json with server URL (default: http://localhost:59125).
Requires ~2GB disk for voice models, 4GB RAM for smooth operation.


Cost: Free (self-hosted), or minimal if hosted on AWS EC2 (~$10/month for t2.micro).

Costs

AWS Free Tier: Covers Lambda, S3, DynamoDB, SNS, SSM, Cognito.
Grok API: $1-3/month (2,500 tokens/day).
Blockchain Storage: ~$0.01/GB/month (Filecoin/Arweave).
Mimic 3: Free (self-hosted) or ~$10/month (EC2).
Total: ~$5-15/month, depending on voice hosting.

Testing

Run unit tests: pytest tests/
Mock APIs with requests_mock for offline testing.

Deployment

Package and deploy: bash deploy.sh
Monitor logs in AWS CloudWatch.

My AI Assistant
A modular AI assistant built on AWS Lambda, using Python, xAI Grok API, Supabase, and agents for tasks like coding, trading, financial planning, CRM, and managing the Blockgnosis platform.
Overview
The AI Assistant acts as a hub, interpreting user requests (text/voice), delegating tasks to specialized agents, and providing a ReactJS dashboard for accessing agent functions (Financial Planning, Trading, Coding, CRM, etc.). The Blockgnosis platform educates users on money history via YouTube, token rewards, and analytics, with separate tabs in the UI.
Setup
Requirements

Python 3.8+: For AWS Lambda
Node.js 18+: For ReactJS frontend
AWS Account: Free tier covers Lambda, S3, SQS, API Gateway, DynamoDB.
Supabase Account: Free tier for auth and database (https://supabase.co).

.env setup
## Environment Setup
1. Create a `.env` file in the root directory.
2. Copy the template from `.env.example` or use the provided template.
3. Install dependencies: `pip install -r requirements.txt`.
4. Load environment variables: `python-dotenv` is used automatically.