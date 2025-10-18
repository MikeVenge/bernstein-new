#!/usr/bin/env python3
"""
Create a fresh copy of the repository and push to GitHub
"""

import os
import shutil
import subprocess
from pathlib import Path

def run_cmd(cmd, cwd=None):
    """Run command and print output"""
    print(f"➤ {cmd}")
    try:
        result = subprocess.run(
            cmd, 
            shell=True, 
            cwd=cwd, 
            capture_output=True, 
            text=True
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr and 'warning' not in result.stderr.lower():
            print(f"⚠️ {result.stderr}")
        return result.returncode == 0
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("🚀 CREATING FRESH REPOSITORY COPY")
    print("=" * 50)
    
    # Define paths
    source_dir = Path("/Users/michaelkim/code/Bernstein")
    fresh_dir = Path("/Users/michaelkim/code/bernstein_fresh_copy")
    
    # Remove old fresh directory if exists
    if fresh_dir.exists():
        print(f"🗑️ Removing old directory: {fresh_dir}")
        shutil.rmtree(fresh_dir)
    
    # Create fresh directory
    print(f"📁 Creating fresh directory: {fresh_dir}")
    fresh_dir.mkdir(parents=True, exist_ok=True)
    
    # Copy essential files only (avoid .git and temp files)
    essential_files = [
        "Dockerfile",
        "main.py", 
        "requirements.txt",
        "parameterized_field_mapper.py",
        "GENERIC_FIELD_MAPPINGS.csv",
        "index.html",
        "railway.json",
        "vercel.json",
        "railway_config.py",
        "nixpacks.toml",
        "Procfile",
        "runtime.txt",
        "start.sh"
    ]
    
    print("\n📋 Copying essential files...")
    for file in essential_files:
        src = source_dir / file
        if src.exists():
            dst = fresh_dir / file
            shutil.copy2(src, dst)
            print(f"  ✅ {file}")
        else:
            print(f"  ⚠️ {file} not found")
    
    # Copy directories
    dirs_to_copy = ["backend", "frontend"]
    for dir_name in dirs_to_copy:
        src_dir = source_dir / dir_name
        if src_dir.exists():
            dst_dir = fresh_dir / dir_name
            print(f"\n📂 Copying {dir_name}/ directory...")
            shutil.copytree(src_dir, dst_dir, ignore=shutil.ignore_patterns(
                '__pycache__', '*.pyc', '.git', 'node_modules', 
                'uploads', 'results', 'temp_*', 'venv'
            ))
            print(f"  ✅ {dir_name}/ copied")
    
    # Initialize git in fresh directory
    print("\n🔧 Initializing git repository...")
    os.chdir(fresh_dir)
    
    commands = [
        "git init",
        'git config user.email "mike@adgoios.com"',
        'git config user.name "MikeVenge"',
        "git add -A",
        'git commit -m "Fresh repository with Dockerfile to fix Railway deployment"',
        "git branch -M main",
        "git remote add origin https://github.com/MikeVenge/bernstein.git"
    ]
    
    for cmd in commands:
        if not run_cmd(cmd, cwd=fresh_dir):
            print(f"⚠️ Command might have failed: {cmd}")
    
    print("\n📊 Repository status:")
    run_cmd("git status --short", cwd=fresh_dir)
    
    print("\n📁 Files in repository:")
    run_cmd("ls -la", cwd=fresh_dir)
    
    print("\n" + "=" * 50)
    print("✅ FRESH REPOSITORY CREATED!")
    print(f"📂 Location: {fresh_dir}")
    print("\n🚀 To push to GitHub, run:")
    print(f"   cd {fresh_dir}")
    print("   git push -f origin main")
    print("\n📋 Key files included:")
    print("   • Dockerfile (fixes Railway Nixpacks issue)")
    print("   • main.py (FastAPI backend)")
    print("   • requirements.txt")
    print("   • All other essential files")
    print("\n🔗 Repository: https://github.com/MikeVenge/bernstein")

if __name__ == "__main__":
    main()
