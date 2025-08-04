#!/bin/bash

echo "🚀 Deploying Taofu Bot to Railway..."

# Check if Railway CLI is installed
if ! command -v railway &> /dev/null; then
    echo "❌ Railway CLI not found. Installing..."
    npm install -g @railway/cli
fi

# Login to Railway (if not already logged in)
echo "🔐 Logging into Railway..."
railway login

# Deploy the project
echo "📦 Deploying to Railway..."
railway up

echo "✅ Deployment complete!"
echo "🔗 Your bot should now be running on Railway"
echo "📝 Don't forget to set your environment variables in Railway dashboard" 