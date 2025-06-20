#!/usr/bin/env python3
"""
Simple GitHub Setup with Personal Access Token - Fixed Version
"""

import os
import sys
import subprocess
from pathlib import Path

def setup():
    print("GitHub Personal Access Token Setup")
    print("=" * 40)
    print()
    
    # Get token
    print("Enter your GitHub Personal Access Token (starts with ghp_):")
    token = input("Token: ").strip()
    
    if not token.startswith('ghp_'):
        print("Error: Invalid token format")
        return False
    
    # Get user info
    print("\nEnter your GitHub username:")
    username = input("Username: ").strip()
    
    print("\nEnter your GitHub email:")
    email = input("Email: ").strip()
    
    print("\nEnter repository name (default: study):")
    repo_name = input("Repository name: ").strip() or "study"
    
    print("\nConfiguring Git...")
    
    # Initialize Git FIRST if needed
    if not Path('.git').exists():
        try:
            subprocess.run(['git', 'init'], check=True)
            print("OK: Git initialized")
        except:
            print("Error: Failed to initialize Git")
            return False
    
    # NOW set Git config (after git init)
    try:
        subprocess.run(['git', 'config', 'user.name', username], check=True)
        subprocess.run(['git', 'config', 'user.email', email], check=True)
        print("OK: Git config set")
    except:
        print("Error: Failed to set Git config")
        return False
    
    # Set remote
    remote_url = f"https://{username}:{token}@github.com/{username}/{repo_name}.git"
    
    try:
        # Check if remote exists
        result = subprocess.run(['git', 'remote', 'get-url', 'origin'], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            # Update existing remote
            subprocess.run(['git', 'remote', 'set-url', 'origin', remote_url], check=True)
            print("OK: Remote URL updated")
        else:
            # Add new remote
            subprocess.run(['git', 'remote', 'add', 'origin', remote_url], check=True)
            print("OK: Remote URL added")
    except:
        print("Error: Failed to set remote")
        return False
    
    # Create .gitignore if not exists
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        gitignore_content = """# Python
__pycache__/
*.py[cod]
.venv/
venv/

# Config
config.py
.env

# IDE
.vscode/
.idea/

# Logs
*.log

# Data
*.csv
*.pkl
data/raw/
models/
"""
        gitignore_path.write_text(gitignore_content)
        print("OK: .gitignore created")
    
    # Update config.py if exists
    config_file = Path('config.py')
    if config_file.exists():
        print("\nUpdating config.py...")
        
        try:
            content = config_file.read_text(encoding='utf-8')
            
            # Update values
            content = content.replace('GITHUB_TOKEN = ""', f'GITHUB_TOKEN = "{token}"')
            content = content.replace('GITHUB_USERNAME = ""', f'GITHUB_USERNAME = "{username}"')
            content = content.replace('REPOSITORY_NAME = ""', f'REPOSITORY_NAME = "{repo_name}"')
            content = content.replace('GITHUB_EMAIL = ""', f'GITHUB_EMAIL = "{email}"')
            
            config_file.write_text(content, encoding='utf-8')
            print("OK: config.py updated")
        except Exception as e:
            print(f"Warning: Could not update config.py: {e}")
    
    print("\nSetup Complete!")
    print("\nConfiguration:")
    print(f"  Username: {username}")
    print(f"  Repository: {username}/{repo_name}")
    print(f"  Remote URL: https://github.com/{username}/{repo_name}")
    
    print("\nIMPORTANT: Create the repository on GitHub first!")
    print(f"Go to: https://github.com/new")
    print(f"Repository name: {repo_name}")
    
    print("\nThen run these commands:")
    print("1. git add .")
    print("2. git commit -m 'Initial commit'")
    print("3. git branch -M main")
    print("4. git push -u origin main")
    
    print("\nOr use the quick commit command:")
    print("python simple_setup_fixed.py --commit -m 'Initial commit'")
    
    return True

def commit_push(message="Update"):
    """Quick commit and push"""
    try:
        # Check if git is initialized
        if not Path('.git').exists():
            print("Error: Not a git repository. Run setup first.")
            return
        
        # Check status
        result = subprocess.run(['git', 'status', '--porcelain'], 
                               capture_output=True, text=True)
        
        if not result.stdout:
            print("No changes to commit")
            return
        
        print("Changed files:")
        print(result.stdout)
        
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)
        print("OK: Files added")
        
        # Commit
        subprocess.run(['git', 'commit', '-m', message], check=True)
        print("OK: Changes committed")
        
        # Try to push
        try:
            # First try to push to main
            result = subprocess.run(['git', 'push', 'origin', 'main'], 
                                   capture_output=True, text=True)
            if result.returncode != 0:
                # If main doesn't exist, try master
                result = subprocess.run(['git', 'push', 'origin', 'master'], 
                                       capture_output=True, text=True)
                if result.returncode != 0:
                    # If neither exists, set upstream
                    subprocess.run(['git', 'branch', '-M', 'main'], check=True)
                    subprocess.run(['git', 'push', '-u', 'origin', 'main'], check=True)
            
            print("Success: Pushed to GitHub!")
        except subprocess.CalledProcessError as e:
            print("Warning: Could not push. Make sure the repository exists on GitHub.")
            print("Create it at: https://github.com/new")
            print("Then run: git push -u origin main")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

def status():
    """Show git status"""
    try:
        # Check if git is initialized
        if not Path('.git').exists():
            print("Error: Not a git repository. Run setup first.")
            return
        
        # Show status
        subprocess.run(['git', 'status'], check=True)
        
        # Show remote
        print("\nRemote repository:")
        subprocess.run(['git', 'remote', '-v'], check=True)
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple GitHub Setup")
    parser.add_argument('--setup', action='store_true', help='Run setup')
    parser.add_argument('--commit', action='store_true', help='Commit and push')
    parser.add_argument('--status', action='store_true', help='Show status')
    parser.add_argument('-m', '--message', default='Update', help='Commit message')
    
    args = parser.parse_args()
    
    if args.setup:
        setup()
    elif args.commit:
        commit_push(args.message)
    elif args.status:
        status()
    else:
        print("Simple GitHub Setup - Fixed Version")
        print()
        print("Commands:")
        print("  Setup:  python simple_setup_fixed.py --setup")
        print("  Commit: python simple_setup_fixed.py --commit -m 'Your message'")
        print("  Status: python simple_setup_fixed.py --status")
        print()
        print("Start with --setup")