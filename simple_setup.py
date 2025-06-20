#!/usr/bin/env python3
"""
Simple GitHub Setup with Personal Access Token
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
    
    # Set Git config
    try:
        subprocess.run(['git', 'config', 'user.name', username], check=True)
        subprocess.run(['git', 'config', 'user.email', email], check=True)
        print("OK: Git config set")
    except:
        print("Error: Failed to set Git config")
        return False
    
    # Initialize Git
    if not Path('.git').exists():
        try:
            subprocess.run(['git', 'init'], check=True)
            print("OK: Git initialized")
        except:
            print("Error: Failed to initialize Git")
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
    
    # Update config.py if exists
    config_file = Path('config.py')
    if config_file.exists():
        print("\nUpdating config.py...")
        
        content = config_file.read_text(encoding='utf-8')
        
        # Update values
        content = content.replace('GITHUB_TOKEN = ""', f'GITHUB_TOKEN = "{token}"')
        content = content.replace('GITHUB_USERNAME = ""', f'GITHUB_USERNAME = "{username}"')
        content = content.replace('REPOSITORY_NAME = ""', f'REPOSITORY_NAME = "{repo_name}"')
        content = content.replace('GITHUB_EMAIL = ""', f'GITHUB_EMAIL = "{email}"')
        
        config_file.write_text(content, encoding='utf-8')
        print("OK: config.py updated")
    
    print("\nSetup Complete!")
    print("\nConfiguration:")
    print(f"  Username: {username}")
    print(f"  Repository: {username}/{repo_name}")
    print(f"  Remote URL: https://github.com/{username}/{repo_name}")
    
    print("\nNext steps:")
    print("1. Add files: git add .")
    print("2. Commit: git commit -m 'Initial commit'")
    print("3. Push: git push -u origin main")
    
    return True

def commit_push(message="Update"):
    """Quick commit and push"""
    try:
        # Check status
        result = subprocess.run(['git', 'status', '--porcelain'], 
                               capture_output=True, text=True)
        
        if not result.stdout:
            print("No changes to commit")
            return
        
        print("Changed files:")
        print(result.stdout)
        
        # Add, commit, push
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', message], check=True)
        subprocess.run(['git', 'push'], check=True)
        
        print("Success: Committed and pushed!")
        
    except subprocess.CalledProcessError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Simple GitHub Setup")
    parser.add_argument('--setup', action='store_true', help='Run setup')
    parser.add_argument('--commit', action='store_true', help='Commit and push')
    parser.add_argument('-m', '--message', default='Update', help='Commit message')
    
    args = parser.parse_args()
    
    if args.setup:
        setup()
    elif args.commit:
        commit_push(args.message)
    else:
        print("Simple GitHub Setup")
        print()
        print("Usage:")
        print("  Setup: python simple_setup.py --setup")
        print("  Commit: python simple_setup.py --commit -m 'Your message'")
        print()
        print("Run with --setup to start")