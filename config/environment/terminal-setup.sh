#\!/bin/bash
# Terminal Setup Script for Research Project

echo "🚀 Research Project Terminal Setup"
echo "=================================="

# Environment Check
echo "📋 Environment Information:"
echo "  Working Directory: $(pwd)"
echo "  Shell: $SHELL"
echo "  Node.js: $(node --version 2>/dev/null || echo 'Not found')"
echo "  npm: $(npm --version 2>/dev/null || echo 'Not found')"
echo "  Python: $(python3 --version 2>/dev/null || echo 'Not found')"
echo "  Git: $(git --version 2>/dev/null || echo 'Not found')"
echo ""

# Quick Commands Setup
echo "🔧 Setting up quick commands..."
cat > .terminal_aliases << 'ALIASES'
# Research Project Quick Commands
alias rs-status="npm run auto:status"
alias rs-lint="npm run lint"
alias rs-dev="npm run dev"
alias rs-deploy="npm run deploy"
alias rs-auto="npm run auto:dev"
alias rs-watch="npm run textlint:watch"
alias rs-organize="python3 auto_organize_and_save.py"
alias rs-colab="echo 'Use Research_Colab_Simple.ipynb for main research'"
alias rs-help="echo 'Research Commands:
  rs-status   - Check automation status
  rs-lint     - Run textlint check
  rs-dev      - Start development server
  rs-deploy   - Deploy to production
  rs-auto     - Run auto development workflow
  rs-watch    - Start file watcher
  rs-organize - Run file organization
  rs-colab    - Colab research info'"
ALIASES

echo "source $(pwd)/.terminal_aliases" >> ~/.bashrc 2>/dev/null || true

# Project Status Check
echo "📊 Project Status Check:"
if [ -f "package.json" ]; then
    echo "  ✅ package.json found"
    if [ -d "node_modules" ]; then
        echo "  ✅ node_modules installed"
    else
        echo "  ⚠️  node_modules missing - run 'npm install'"
    fi
else
    echo "  ❌ package.json not found"
fi

if [ -f ".textlintrc.json" ]; then
    echo "  ✅ textlint configured"
else
    echo "  ⚠️  textlint not configured"
fi

if [ -d ".github/workflows" ]; then
    echo "  ✅ GitHub Actions configured"
else
    echo "  ⚠️  GitHub Actions not configured"
fi

if [ -f "vercel.json" ]; then
    echo "  ✅ Vercel configured"
else
    echo "  ⚠️  Vercel not configured"
fi

echo ""
echo "🎯 Quick Start Commands:"
echo "  npm install           - Install dependencies"
echo "  npm run auto:status   - Check system status"
echo "  npm run lint          - Check text quality"
echo "  npm run dev           - Start development"
echo "  rs-help               - Show research commands"
echo ""
echo "✅ Terminal setup complete\!"
echo "Run 'source ~/.bashrc' or restart terminal to use aliases"
EOF < /dev/null
