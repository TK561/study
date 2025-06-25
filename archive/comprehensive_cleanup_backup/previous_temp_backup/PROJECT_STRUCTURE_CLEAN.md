# 📁 Project Structure - Research System (Cleaned)

## 🏗️ Directory Overview
```
/mnt/c/Desktop/Research/
├── 📄 Core Files
│   ├── README.md                    # Main project documentation
│   ├── CLAUDE.md                    # Claude Code configuration
│   ├── vercel.json                  # Vercel deployment config
│   ├── package.json                 # Node.js dependencies
│   └── requirements.txt             # Python dependencies
│
├── 🌐 public/                       # Main website files
│   ├── index.html                   # Research Project home
│   ├── main-system/                 # Semantic Classification System
│   │   └── index.html              
│   └── discussion-site/             # Research Discussion Records
│       └── index.html              
│
├── 🔬 study/                        # Research content
│   ├── analysis/                    # Analysis results
│   ├── analysis_reports/            # Detailed reports
│   ├── docs/                        # Research documentation
│   ├── references/                  # PDF references & slides
│   ├── reports/                     # Project reports
│   ├── research_content/            # Python research scripts
│   └── tools/                       # Analysis tools
│
├── 🛠️ core/                         # Core system files
│   ├── gemini_html_optimizer.py
│   ├── html_auto_updater.py
│   └── vercel_deploy.py
│
├── 🤖 automation/                   # Automation scripts
│   ├── auto_backup_system.py
│   ├── auto_git_manager.py
│   └── [other automation tools]
│
├── 🔧 tools/                        # Utility tools
│   ├── research/                    # Research-specific tools
│   ├── system/                      # System management tools
│   └── utilities/                   # General utilities
│
├── 📊 data/                         # Data storage
│   ├── research_toolkit.db          # Research database
│   └── [log files]
│
├── 📝 docs/                         # Documentation
│   ├── guides/                      # How-to guides
│   └── archives/                    # Old documentation
│
├── ⚙️ config/                       # Configuration files
│   └── [JSON config files]
│
├── 📦 archive/                      # Archived content
│   ├── old_code/                    # Deprecated scripts
│   ├── old_sessions/                # Old session files
│   ├── old_backups/                 # Old backup files
│   └── old_logs/                    # Old log files
│
├── 🌐 discussion-site/              # Discussion site source
│   ├── index.html
│   ├── package.json
│   └── node_modules/
│
├── 📁 .claude/                      # Claude-related files
│   ├── claude_master/
│   ├── claude_project/
│   └── claude_sessions/
│
└── 📂 Hidden Directories
    ├── .git/                        # Git repository
    └── .vscode/                     # VS Code settings
```

## 📋 Key Files Description

### 🏠 Main Website (public/)
- **index.html**: Research project homepage with project cards
- **main-system/index.html**: Interactive semantic classification system with charts
- **discussion-site/index.html**: Research discussion records with AI consultation

### 🔬 Research Content (study/)
- **analysis_reports/**: Detailed analysis including Cohen's Power, specialization studies
- **research_content/**: Python scripts for dataset analysis and experiments
- **references/**: Original research papers and presentations

### 🤖 Automation System
- **auto_master_controller.py**: Central automation controller
- **auto_git_manager.py**: Automatic Git commit management
- **auto_vercel_monitor.py**: Vercel deployment monitoring

### 📊 Data Management
- **research_toolkit.db**: SQLite database for research data
- **config/**: JSON configuration files for various systems

## 🚀 Quick Access Commands

```bash
# Start automation system
./automation/start_auto_system.sh

# Deploy to Vercel
python3 core/vercel_deploy.py

# View research analysis
python3 tools/research/integrated_research_toolkit.py
```

## 📁 Cleanup Summary
- ✅ Removed duplicate index.html files
- ✅ Archived old scripts and backups
- ✅ Consolidated Claude directories into .claude/
- ✅ Cleaned up unused node_modules (saved ~178MB)
- ✅ Organized configuration files
- ✅ Created clear archive structure

## 🔗 Important URLs
- **Live Site**: https://study-research-final.vercel.app/
- **Main System**: https://study-research-final.vercel.app/main-system/
- **Discussion Site**: https://study-research-final.vercel.app/discussion-site/

---
*Last updated: 2025-06-25*