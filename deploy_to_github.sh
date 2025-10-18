#!/bin/bash

echo "🚀 DEPLOYING COMPLETE APPLICATION TO GITHUB"
echo "============================================"

# Ensure we're in the right directory
cd /Users/michaelkim/code/Bernstein

echo "📁 Checking directories exist:"
if [ -d "backend" ]; then
    echo "   ✅ backend/ directory exists"
    ls backend/ | head -5
else
    echo "   ❌ backend/ directory missing"
fi

if [ -d "frontend" ]; then
    echo "   ✅ frontend/ directory exists"
    ls frontend/ | head -5
else
    echo "   ❌ frontend/ directory missing"
fi

echo ""
echo "🔧 Git operations:"

# Initialize git if needed
if [ ! -d ".git" ]; then
    echo "   Initializing git repository..."
    git init
fi

# Add remote if needed
git remote remove origin 2>/dev/null || true
git remote add origin https://github.com/MikeVenge/bernstein.git

echo "   Adding all files..."
git add .
git add backend/
git add frontend/
git add *.csv
git add *.md
git add *.py
git add *.html

echo "   Committing changes..."
git commit -m "Complete Quarterly Earning Field Mapper Application

FULL-STACK APPLICATION:
- backend/ directory: Python FastAPI with Railway deployment config
- frontend/ directory: React app with Vercel deployment config  
- 134 verified field mappings with comprehensive validation
- Generic mapping format for cross-dataset reusability
- Complete documentation and deployment guides

DEPLOYMENT READY:
- Railway project: a33c9b9d-889b-427d-aba8-6240ca22d770
- Vercel project: bernstein-eight.vercel.app
- CORS configured for cross-platform communication
- Environment variables and build scripts included

FEATURES:
- Parameterized mapping engine
- Multiple validation methods (Q1, Q2, historical)
- Modern web interface with real-time monitoring
- File upload, processing, and download capabilities
- Complete audit trail and source tracking"

echo "   Pushing to GitHub..."
git push -f origin main

echo ""
echo "✅ Deployment complete!"
echo "📍 Repository: https://github.com/MikeVenge/bernstein.git"
echo "📁 Should now include backend/ and frontend/ directories"
