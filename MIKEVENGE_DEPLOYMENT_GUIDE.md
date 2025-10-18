# MikeVenge/bernstein Deployment Guide

## 🎯 Repository: https://github.com/MikeVenge/bernstein.git

### **🚂 Railway Configuration (Backend)**

**Update Railway Settings:**
1. **Go to Railway project**: `a33c9b9d-889b-427d-aba8-6240ca22d770`
2. **Settings → Source**
3. **Disconnect** current repository
4. **Connect** new repository: `MikeVenge/bernstein`
5. **Set Root Directory**: `backend`

**Environment Variables (keep existing):**
```bash
RAILWAY_PROJECT_ID=a33c9b9d-889b-427d-aba8-6240ca22d770
RAILWAY_ENVIRONMENT=production
CORS_ORIGINS=https://bernstein-eight.vercel.app
```

### **🌐 Vercel Configuration (Frontend)**

**Update Vercel Settings:**
1. **Go to Vercel project**: https://vercel.com/mike-adgoios-projects/bernstein
2. **Settings → Git**
3. **Disconnect** current repository
4. **Connect** new repository: `MikeVenge/bernstein`
5. **Set Root Directory**: `frontend`

**Build Settings:**
```bash
Framework: Other
Root Directory: frontend
Build Command: npm run build
Output Directory: build
Install Command: npm install
```

**Environment Variables:**
```bash
REACT_APP_API_URL=https://backend-production-a33c.up.railway.app
REACT_APP_APP_NAME=Quarterly Earning Field Mapper
```

### **📁 Repository Structure**

The `MikeVenge/bernstein` repository now contains:

```
bernstein/
├── backend/                 ← Railway deploys from here
│   ├── main.py             ← FastAPI application
│   ├── requirements.txt    ← Python dependencies
│   ├── railway.json        ← Railway configuration
│   ├── nixpacks.toml       ← Build configuration
│   ├── start.sh           ← Startup script
│   └── runtime.txt        ← Python version
├── frontend/               ← Vercel deploys from here
│   ├── package.json        ← React dependencies
│   ├── public/index.html   ← Main application
│   ├── vercel.json         ← Vercel configuration
│   └── src/               ← React components
├── GENERIC_FIELD_MAPPINGS.csv     ← Reusable mapping template
├── CONSOLIDATED_FIELD_MAPPINGS.csv ← Complete field mappings
└── README_FULLSTACK_SETUP.md      ← Documentation
```

### **🔗 Expected Deployment URLs**

After connecting to `MikeVenge/bernstein`:
- **Frontend**: `https://bernstein-eight.vercel.app/`
- **Backend**: `https://backend-production-a33c.up.railway.app/`

### **🚀 Deployment Steps**

1. **Railway**:
   - Connect `MikeVenge/bernstein` repository
   - Set root directory to `backend`
   - Deploy automatically

2. **Vercel**:
   - Connect `MikeVenge/bernstein` repository  
   - Set root directory to `frontend`
   - Deploy automatically

### **✅ What's Included**

The repository now contains:
- ✅ **Complete field mapping solution** (134 verified mappings)
- ✅ **Full-stack web application** (Python FastAPI + React)
- ✅ **Railway deployment configuration** with your project ID
- ✅ **Vercel deployment configuration** with proxy setup
- ✅ **Generic mapping format** for reusability
- ✅ **CORS configuration** for cross-platform communication
- ✅ **Complete documentation** and setup guides

### **🎯 Next Steps**

1. **Update Railway**: Connect to `MikeVenge/bernstein` repository
2. **Update Vercel**: Connect to `MikeVenge/bernstein` repository
3. **Test deployment**: Both platforms should auto-deploy
4. **Verify connection**: Frontend should connect to Railway backend

**Your complete Quarterly Earning Field Mapper is now available in the `MikeVenge/bernstein` repository and ready for deployment!** 🚀
