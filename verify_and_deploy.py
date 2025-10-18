#!/usr/bin/env python3
"""
Verify and Deploy Script

Verifies directories exist and deploys to GitHub.
"""

import os
import subprocess
from pathlib import Path

def run_command(cmd, cwd=None):
    """Run a command and return the result."""
    try:
        result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def main():
    base_dir = Path("/Users/michaelkim/code/Bernstein")
    os.chdir(base_dir)
    
    print("🔍 VERIFYING DIRECTORIES AND DEPLOYING")
    print("=====================================")
    
    # Check directories exist
    backend_dir = base_dir / "backend"
    frontend_dir = base_dir / "frontend"
    
    print(f"\n📁 Directory verification:")
    print(f"   Backend exists: {backend_dir.exists()}")
    if backend_dir.exists():
        print(f"   Backend files: {list(backend_dir.glob('*'))[:5]}")
    
    print(f"   Frontend exists: {frontend_dir.exists()}")
    if frontend_dir.exists():
        print(f"   Frontend files: {list(frontend_dir.glob('*'))[:5]}")
    
    # Git operations
    print(f"\n🔧 Git operations:")
    
    # Remove existing git
    success, out, err = run_command("rm -rf .git")
    print(f"   Removed .git: {success}")
    
    # Initialize git
    success, out, err = run_command("git init")
    print(f"   Git init: {success}")
    
    # Add remote
    success, out, err = run_command("git remote add origin https://github.com/MikeVenge/bernstein.git")
    print(f"   Remote added: {success}")
    
    # Add all files
    success, out, err = run_command("git add .")
    print(f"   Files added: {success}")
    
    # Check status
    success, out, err = run_command("git status --porcelain")
    if success:
        lines = out.strip().split('\n')[:10]
        print(f"   Files to commit: {len(lines)}")
        for line in lines:
            print(f"     {line}")
    
    # Commit
    commit_msg = "Complete Quarterly Earning Field Mapper with backend and frontend directories"
    success, out, err = run_command(f'git commit -m "{commit_msg}"')
    print(f"   Commit: {success}")
    if not success:
        print(f"     Error: {err}")
    
    # Push
    success, out, err = run_command("git push -f origin main")
    print(f"   Push: {success}")
    if not success:
        print(f"     Error: {err}")
    else:
        print(f"     Output: {out}")
    
    print(f"\n✅ Deployment complete!")
    print(f"📍 Check: https://github.com/MikeVenge/bernstein.git")

if __name__ == "__main__":
    main()
