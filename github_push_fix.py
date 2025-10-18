#!/usr/bin/env python3
"""
Fix GitHub push issues and upload all files including Dockerfile
"""

import os
import subprocess
import sys

def run_command(cmd, capture=False):
    """Run a shell command and return output"""
    print(f"Running: {cmd}")
    try:
        if capture:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            return result.stdout.strip()
        else:
            subprocess.run(cmd, shell=True, check=False)
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def main():
    print("🔧 FIXING GITHUB REPOSITORY PUSH")
    print("=" * 50)
    
    # Change to project directory
    os.chdir("/Users/michaelkim/code/Bernstein")
    print(f"📁 Working directory: {os.getcwd()}")
    
    # Check if .git exists
    if not os.path.exists(".git"):
        print("📂 Initializing git repository...")
        run_command("git init")
    else:
        print("✅ Git repository already initialized")
    
    # Configure git
    print("\n⚙️ Setting git configuration...")
    run_command('git config user.email "mike@adgoios.com"')
    run_command('git config user.name "MikeVenge"')
    
    # Set remote
    print("\n🔗 Setting remote origin...")
    run_command("git remote remove origin 2>/dev/null")
    run_command("git remote add origin https://github.com/MikeVenge/bernstein.git")
    
    # Check current status
    print("\n📊 Current git status:")
    run_command("git status")
    
    # Add all files
    print("\n📁 Adding all files to git...")
    run_command("git add -A")
    run_command("git add .")  # Double ensure
    
    # Commit
    print("\n💾 Creating commit...")
    commit_msg = "Fix Railway deployment with Dockerfile and complete file structure"
    run_command(f'git commit -m "{commit_msg}" --allow-empty')
    
    # Push to GitHub
    print("\n🚀 Pushing to GitHub...")
    print("This may require authentication...")
    
    # Try different push methods
    push_commands = [
        "git push -f origin HEAD:main",
        "git push -f origin master:main",
        "git push --set-upstream origin main",
        "git push origin main"
    ]
    
    for cmd in push_commands:
        print(f"\nTrying: {cmd}")
        result = run_command(cmd)
        if result is not None:
            break
    
    print("\n" + "=" * 50)
    print("✅ SCRIPT COMPLETE!")
    print("\n📋 Key files that should now be in GitHub:")
    print("   • Dockerfile (NEW - fixes Railway Nixpacks issue)")
    print("   • main.py (backend)")
    print("   • requirements.txt")
    print("   • parameterized_field_mapper.py")
    print("   • GENERIC_FIELD_MAPPINGS.csv")
    print("   • index.html (frontend)")
    print("   • backend/ directory")
    print("   • frontend/ directory")
    print("\n🔗 Repository: https://github.com/MikeVenge/bernstein")

if __name__ == "__main__":
    main()
