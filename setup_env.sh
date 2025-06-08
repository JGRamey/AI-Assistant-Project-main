# setup_env.sh
echo "Creating .env file..."
cat > .env << EOL
SUPABASE_URL=https://your-supabase-project-id.supabase.co
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
EOL
echo "Please update .env with your actual credentials."