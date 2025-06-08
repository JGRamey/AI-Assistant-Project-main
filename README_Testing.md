#Security Considerations
Never Commit .env: Ensure it’s in .gitignore to prevent accidental exposure.
Use Test Keys: For Stripe, Ethereum, and other APIs, use test keys during development (e.g., Stripe’s sk_test_..., Sepolia testnet for Ethereum).
Restrict AWS IAM Permissions: Limit AWS_ACCESS_KEY_ID to only necessary services (DynamoDB, SQS).
Rotate Keys Regularly: Update API keys and private keys periodically.
Store Production Keys Securely: In production, use AWS Secrets Manager or Parameter Store instead of .env.


Security for testing the Blockgnosis & AI Assistant Project
Overview
Blockgnosis is a platform integrating AI agents, blockchain smart contracts, and financial tools to manage YouTube content, revenue, trading, and more. Built with Python, Flask, Supabase, and React, it leverages AWS services (Lambda, SQS, DynamoDB) and Ethereum for decentralized operations.
Security Concerns for Testing
Testing the Blockgnosis project involves handling sensitive data (e.g., API keys, database URLs, Ethereum private keys). Below are key security concerns and mitigation strategies to ensure files and data are not compromised during testing or when pushing to GitHub.
1. Exposure of Sensitive Files
Concern: Committing files like .env containing API keys, private keys, or credentials to GitHub can expose them publicly.Mitigation:

Use .gitignore: Ensure .env and other sensitive files are excluded from version control.
Scan Commits: Use tools like truffleHog to detect secrets before pushing.

2. Hardcoded Credentials
Concern: Embedding API keys or secrets in source code (e.g., revenue.py, SmartContractManager.py) risks exposure if code is shared.Mitigation:

Environment Variables: Store credentials in .env and access via os.environ.get().
Code Review: Check for hardcoded keys before committing.

3. Untracked Sensitive Data
Concern: Accidentally committing files with sensitive data due to missing .gitignore entries.Mitigation:

Comprehensive .gitignore: Include common sensitive file patterns.
Pre-Commit Hooks: Use hooks to block commits with sensitive data.

4. Real API Keys in Tests
Concern: Tests making unintended API calls or failing due to missing real keys (e.g., Stripe, Web3).Mitigation:

Mocking: Use requests_mock and unittest.mock in tests (e.g., test_agents.py) to simulate APIs.
Mock Environment Variables: Set mock keys in test fixtures.

5. AWS Credentials Exposure
Concern: Misconfigured AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY with excessive permissions can be exploited.Mitigation:

Least Privilege: Limit AWS IAM roles to necessary services (DynamoDB, SQS).
Secure Storage: Store AWS credentials in GitHub Secrets for CI.

6. Ethereum Private Key Exposure
Concern: Committing ETH_PRIVATE_KEY used in SmartContractManager.py can lead to fund loss.Mitigation:

Testnet Keys: Use Sepolia testnet keys for development.
Secret Management: Store keys in .env locally and GitHub Secrets in CI.

7. Lack of Key Rotation
Concern: Unrotated API keys or private keys increase risk if exposed.Mitigation:

Regular Rotation: Update keys every 3-6 months or after suspected exposure.
Automation: Use scripts to rotate keys in CI/CD pipelines.

8. Production Secrets in Development
Concern: Using production keys in .env for local testing risks unintended actions (e.g., real Stripe charges).Mitigation:

Test Keys: Use test keys (e.g., Stripe’s sk_test_..., Sepolia ETH).
Environment Separation: Maintain separate .env files for development and production.

9. GitHub Actions Secrets
Concern: Unsecured secrets in GitHub Actions workflows (e.g., ci.yml) can be accessed by unauthorized users.Mitigation:

GitHub Secrets: Store credentials in repository secrets.
Access Control: Restrict workflow permissions to trusted users.

Security Setup Instructions
Follow these steps to maintain security during testing and when pushing to GitHub.
1. Create and Secure .env

Purpose: Store sensitive credentials (e.g., API keys, private keys) securely.
Steps:
Create .env in the project root (my-ai-assistant/):SUPABASE_URL=https://your-supabase-project-id.supabase.co
SUPABASE_KEY=your-supabase-anon-key
STRIPE_API_KEY=sk_test_your-stripe-key
ETH_RPC_URL=https://sepolia.infura.io/v3/your-infura-project-id
ETH_PRIVATE_KEY=your-ethereum-private-key
CHAIN_ID=11155111
AWS_ACCESS_KEY_ID=your-aws-access-key
AWS_SECRET_ACCESS_KEY=your-aws-secret-key
SQS_QUEUE_URL=https://sqs.us-east-1.amazonaws.com/your-account-id/agent-comms-queue
YOUTUBE_API_KEY=your-google-api-key
GROK_API_KEY=your-grok-key
COINBASE_API_KEY=your-coinbase-key
GITHUB_TOKEN=your-github-key
TWITTER_API_KEY=your-twitter-key
MAILCHIMP_API_KEY=your-mailchimp-key
FRED_API_KEY=your-fred-api-key


Use test keys (e.g., Stripe test key, Sepolia ETH private key funded via a faucet).
Install python-dotenv:pip install python-dotenv
echo "python-dotenv==1.0.1" >> requirements.txt


Load .env in code (already implemented in src/utils.py):from dotenv import load_dotenv
load_dotenv()





2. Configure .gitignore

Purpose: Prevent sensitive files from being committed.
Steps:
Create or update .gitignore in the project root:.env
*.pyc
__pycache__/
venv/
node_modules/
*.log
*.key
*.pem


Verify .env is not tracked:git status


If .env is tracked, remove it:git rm --cached .env
git commit -m "Remove .env from version control"





3. Scan for Secrets

Purpose: Detect sensitive data in code before pushing.
Steps:
Install truffleHog:pip install truffleHog


Scan the repository:truffleHog git file://$(pwd)


Review and remove any detected secrets.
Optionally, set up a pre-commit hook:pip install pre-commit
echo -e "repos:\n- repo: local\n  hooks:\n  - id: trufflehog\n    name: truffleHog\n    entry: trufflehog git file://$(pwd) --json\n    language: system" > .pre-commit-config.yaml
pre-commit install





4. Mock APIs in Tests

Purpose: Avoid real API calls during testing.
Steps:
Ensure test_agents.py uses mocks (already implemented):
Stripe: Mocked with requests_mock.
Web3: Mocked with unittest.mock.
Supabase/DynamoDB/SQS: Mocked with MagicMock.


Run tests locally:pytest tests/ --verbose


Verify no real API keys are required (mocked in setup_env fixture).



5. Secure AWS Credentials

Purpose: Limit AWS IAM permissions and secure credentials.
Steps:
Create an IAM user with minimal permissions:
Services: DynamoDB (read/write), SQS (send/receive).
Example policy:{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "sqs:SendMessage",
        "sqs:ReceiveMessage"
      ],
      "Resource": "*"
    }
  ]
}




Store AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY in .env locally and GitHub Secrets for CI.
Test AWS access locally:aws dynamodb list-tables





6. Use Testnet for Ethereum

Purpose: Prevent real fund loss with ETH_PRIVATE_KEY.
Steps:
Use a Sepolia testnet private key:
Create a wallet (e.g., MetaMask).
Fund it via a Sepolia faucet (e.g., Infura’s faucet).


Set ETH_PRIVATE_KEY in .env with the testnet key.
Verify in SmartContractManager.py:chain_id = int(os.environ.get('CHAIN_ID', 11155111))  # Sepolia





7. Rotate Keys Periodically

Purpose: Reduce risk of exposed keys.
Steps:
Schedule key rotation every 3-6 months:
Stripe: Generate new test key in dashboard.
Supabase: Regenerate anon key.
Ethereum: Create new testnet wallet.
AWS: Rotate IAM access keys.


Update .env and GitHub Secrets after rotation.
Test after updates:pytest tests/





8. Separate Development and Production

Purpose: Avoid using production keys in development.
Steps:
Create separate .env files:
.env.development:STRIPE_API_KEY=sk_test_...
ETH_PRIVATE_KEY=sepolia-test-key


.env.production (stored securely, e.g., AWS Secrets Manager):STRIPE_API_KEY=sk_live_...
ETH_PRIVATE_KEY=mainnet-key




Load appropriate .env:cp .env.development .env


Use test keys for local testing.



9. Secure GitHub Actions

Purpose: Protect secrets in CI workflows.
Steps:
Add secrets to GitHub:
Go to Repository > Settings > Secrets and variables > Actions > New repository secret.
Add: SUPABASE_URL, SUPABASE_KEY, STRIPE_API_KEY, etc.


Use secrets in .github/workflows/ci.yml (already implemented).
Restrict workflow permissions:
Go to Settings > Actions > General > Workflow permissions > Read-only.


Monitor workflow runs for unauthorized access.



Testing Instructions

Install Dependencies:
python -m venv venv
source venv/bin/activate  # Unix/Mac
venv\Scripts\activate     # Windows
pip install -r requirements.txt
cd frontend && npm install


Run Backend Tests:
pytest tests/ --verbose


Tests mock all APIs, so no real keys are needed.
Review test_agents.py output for agent/assistant results.


Run Frontend Tests:
cd frontend
npm test


Push to GitHub:
git add .
git commit -m "Update project with secure testing"
git push origin main


Ensure .gitignore is set up.
Run truffleHog before pushing.


Verify CI:

Check GitHub Actions runs (Repository > Actions).
Fix failures using workflow logs.



Additional Resources

Supabase: Dashboard for keys and migrations.
Stripe: Test Keys.
AWS IAM: Console for credentials.
Sepolia Faucet: Infura.
truffleHog: GitHub.
GitHub Actions: Docs.

