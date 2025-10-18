#!/usr/bin/env python3
"""
Setup fresh repository copy and initialize git
"""

import os
import shutil
import subprocess
from pathlib import Path

# Define paths
source_dir = Path("/Users/michaelkim/code/Bernstein")
fresh_dir = Path("/Users/michaelkim/code/bernstein_fresh_copy")

# Ensure fresh directory exists
fresh_dir.mkdir(parents=True, exist_ok=True)

# Essential files to copy
files_to_copy = [
    "Dockerfile",
    "main.py",
    "requirements.txt",
    "parameterized_field_mapper.py",
    "GENERIC_FIELD_MAPPINGS.csv",
    "index.html",
]

print("📋 Copying essential files...")
for file in files_to_copy:
    src = source_dir / file
    if src.exists():
        dst = fresh_dir / file
        shutil.copy2(src, dst)
        print(f"  ✅ {file}")

# Change to fresh directory
os.chdir(fresh_dir)

# Initialize git
print("\n🔧 Initializing git...")
commands = [
    "git init",
    'git config user.email "mike@adgoios.com"',
    'git config user.name "MikeVenge"',
    "git add .",
    'git commit -m "Fix Railway deployment with Dockerfile - bypass Nixpacks pip error"',
    "git branch -M main",
    "git remote add origin https://github.com/MikeVenge/bernstein.git",
]

for cmd in commands:
    print(f"  ➤ {cmd}")
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=fresh_dir)
    if result.returncode != 0 and "already exists" not in result.stderr:
        print(f"    ⚠️ {result.stderr}")

print(f"\n✅ Fresh repository created at: {fresh_dir}")
print("\n📁 Files in fresh repository:")
for file in fresh_dir.iterdir():
    if file.is_file():
        print(f"  • {file.name}")

print("\n🚀 To push to GitHub, run:")
print(f"  cd {fresh_dir}")
print("  git push -f origin main")
