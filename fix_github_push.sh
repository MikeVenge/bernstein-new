#!/bin/bash

echo "🔧 FIXING GITHUB REPOSITORY PUSH"
echo "================================"

# Navigate to project directory
cd /Users/michaelkim/code/Bernstein

# Initialize git if needed
if [ ! -d .git ]; then
    echo "📂 Initializing git repository..."
    git init
fi

# Set git config
echo "⚙️ Setting git configuration..."
git config user.email "mike@adgoios.com" 2>/dev/null || true
git config user.name "MikeVenge" 2>/dev/null || true

# Add remote
echo "🔗 Setting remote origin..."
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/MikeVenge/bernstein.git

# Add all files
echo "📁 Adding all files..."
git add -A

# Create commit
echo "💾 Creating commit..."
git commit -m "Fix Railway deployment with Dockerfile and update all files" || true

# Force push to main branch
echo "🚀 Pushing to GitHub (main branch)..."
git push -f origin HEAD:main

echo ""
echo "✅ DONE! Check https://github.com/MikeVenge/bernstein"
echo ""
echo "📋 Key files that should now be in GitHub:"
echo "   • Dockerfile (NEW - fixes Railway Nixpacks issue)"
echo "   • main.py (backend)"
echo "   • requirements.txt"
echo "   • index.html (frontend)"
echo "   • backend/ directory"
echo "   • frontend/ directory"
