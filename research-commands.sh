#\!/bin/bash
# Research Project Commands

case "$1" in
    "status")
        echo "📊 Research Project Status"
        npm run auto:status
        ;;
    "lint")
        echo "📝 Running text quality check..."
        npm run lint
        ;;
    "organize")
        echo "🧹 Organizing files..."
        python3 auto_organize_and_save.py
        ;;
    "dev")
        echo "🚀 Starting development server..."
        npm run dev
        ;;
    "deploy")
        echo "🌐 Deploying to production..."
        npm run deploy
        ;;
    "auto")
        echo "🤖 Running auto development workflow..."
        npm run auto:dev
        ;;
    "watch")
        echo "👁️ Starting file watcher..."
        npm run textlint:watch
        ;;
    "install")
        echo "📦 Installing dependencies..."
        npm install
        ;;
    *)
        echo "🔬 Research Project Commands:"
        echo ""
        echo "  ./research-commands.sh status    - Check automation status"
        echo "  ./research-commands.sh lint      - Run textlint check"
        echo "  ./research-commands.sh organize  - Organize files and save session"
        echo "  ./research-commands.sh dev       - Start development server"
        echo "  ./research-commands.sh deploy    - Deploy to production"
        echo "  ./research-commands.sh auto      - Run auto development workflow"
        echo "  ./research-commands.sh watch     - Start file watcher"
        echo "  ./research-commands.sh install   - Install dependencies"
        echo ""
        echo "📋 Research Components:"
        echo "  - Research_Colab_Simple.ipynb    - Main image classification research"
        echo "  - Auto_Research_Colab.ipynb      - Auto research execution"
        echo "  - public/                        - Research web interface"
        echo "  - sessions/                      - Research session records"
        echo ""
        echo "🌐 URLs:"
        echo "  - Local: http://localhost:3000"
        echo "  - Production: https://study-research.vercel.app"
        ;;
esac
EOF < /dev/null
