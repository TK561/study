#!/bin/bash

# AI-Enhanced Research Discussion Site Deployment Script
# Generated with Claude Code

echo "🚀 Starting AI-Enhanced Research Discussion Site Deployment..."

# Check if Vercel CLI is installed
if ! command -v vercel &> /dev/null; then
    echo "❌ Vercel CLI not found. Installing..."
    npm install -g vercel
fi

# Check if package.json exists
if [ ! -f "package.json" ]; then
    echo "❌ package.json not found. Please run this script from the project root."
    exit 1
fi

# Install dependencies
echo "📦 Installing dependencies..."
npm install

# Check for environment variables
if [ ! -f ".env.local" ]; then
    echo "⚠️  .env.local not found. Creating from example..."
    if [ -f ".env.example" ]; then
        cp .env.example .env.local
        echo "✅ Created .env.local from example"
        echo "🔧 Please edit .env.local and add your API keys before deploying to production"
    else
        echo "❌ .env.example not found"
    fi
fi

# Run deployment
echo "🚀 Deploying to Vercel..."
vercel --prod

echo ""
echo "✅ Deployment completed!"
echo ""
echo "🎯 Features deployed:"
echo "   📊 Enhanced Research Discussion Records"
echo "   🤖 AI Bidirectional Consultation System"
echo "   🎯 Next Directions Planning"
echo "   💾 History & Save functionality"
echo "   🔒 Secure API Integration"
echo ""
echo "📖 Usage:"
echo "   1. Visit the deployed URL"
echo "   2. Navigate to 'AI提案・議論' tab"
echo "   3. Input your research questions"
echo "   4. Experience AI-powered consultation"
echo ""
echo "🔧 Next Steps:"
echo "   - Add real Gemini API key to .env.local"
echo "   - Test AI consultation functionality"
echo "   - Customize responses for your research domain"
echo ""
echo "Generated with Claude Code - AI Research Assistant"