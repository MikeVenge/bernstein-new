# Simple Deployment Guide - Root Level Files

## 🚨 Issue: Subdirectories Not Showing in GitHub

Since the `backend/` and `frontend/` subdirectories aren't appearing in GitHub, I've created root-level files for immediate deployment.

## ✅ Root-Level Files Created

### **For Railway (Backend):**
- `main.py` - FastAPI application (moved to root)
- `requirements.txt` - Python dependencies  
- `railway.json` - Railway configuration

### **For Vercel (Frontend):**
- `index.html` - React application (moved to root)
- `vercel.json` - Vercel configuration and API proxy

## 🚀 Deployment Instructions

### **Railway Setup:**
1. **Project ID**: `a33c9b9d-889b-427d-aba8-6240ca22d770`
2. **Repository**: `MikeVenge/bernstein`
3. **Root Directory**: Leave empty (deploy from root)
4. **Environment Variables**:
   ```
   RAILWAY_PROJECT_ID=a33c9b9d-889b-427d-aba8-6240ca22d770
   RAILWAY_ENVIRONMENT=production
   CORS_ORIGINS=https://bernstein-eight.vercel.app
   ```

### **Vercel Setup:**
1. **Repository**: `MikeVenge/bernstein`
2. **Root Directory**: Leave empty (deploy from root)
3. **Framework**: Other
4. **Build Command**: Leave empty
5. **Output Directory**: Leave empty

## 🎯 Simplified Architecture

```
MikeVenge/bernstein (root)
├── main.py              ← Railway will deploy this as FastAPI backend
├── requirements.txt     ← Python dependencies
├── railway.json         ← Railway configuration
├── index.html          ← Vercel will deploy this as frontend
├── vercel.json         ← Vercel configuration with API proxy
└── ... (mapping files)
```

## 🔗 Expected URLs

- **Frontend**: `https://bernstein-eight.vercel.app/`
- **Backend**: `https://backend-production-a33c.up.railway.app/`

## ✅ Benefits of Root-Level Deployment

1. **Simpler Configuration**: No subdirectory issues
2. **Direct Deployment**: Both platforms deploy from root
3. **Immediate Visibility**: All files visible in GitHub
4. **Same Functionality**: Full application capabilities maintained

**This approach avoids the subdirectory deployment issues while maintaining all functionality!** 🎯
