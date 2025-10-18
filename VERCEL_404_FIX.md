# Fixing Vercel 404 Error for Quarterly Earning Field Mapper

## 🚨 Issue: https://bernstein-eight.vercel.app/ showing 404

The 404 error is happening because Vercel isn't properly configured to build and serve the React application from the `frontend` directory.

## ✅ Solution Steps

### **1. Update Vercel Project Settings**

In your Vercel dashboard for the `bernstein` project:

**Go to Settings → General:**
- **Root Directory**: `frontend` (IMPORTANT!)
- **Framework Preset**: `Other`
- **Build Command**: `npm run build`
- **Output Directory**: `build`
- **Install Command**: `npm install`

### **2. Add Environment Variables**

In Vercel Settings → Environment Variables:

| Key | Value |
|-----|-------|
| `REACT_APP_API_URL` | `https://backend-production-a33c.up.railway.app` |
| `REACT_APP_APP_NAME` | `Quarterly Earning Field Mapper` |

### **3. Update Build Configuration**

The updated `frontend/vercel.json` I created will handle:
- Static file serving
- API proxying to Railway
- SPA routing

### **4. Redeploy**

After making these changes:
1. **Trigger a new deployment** in Vercel
2. Or **push changes to GitHub** (if auto-deploy is enabled)

### **5. Alternative: Direct HTML Deployment**

If the React build is still having issues, you can deploy the simple HTML version:

**Option A: Deploy frontend_simple.html directly**
1. Copy `frontend_simple.html` to `frontend/public/index.html` (already done)
2. Update Vercel settings to serve static files

**Option B: Create build directory manually**
```bash
mkdir -p frontend/build
cp frontend_simple.html frontend/build/index.html
```

### **6. Test the Connection**

After deployment:
1. Visit: `https://bernstein-eight.vercel.app/`
2. Check for green "Backend: Connected" status
3. Test file upload functionality

### **7. Railway Backend URL**

Once Railway is deployed, update the Vercel environment variable:
```bash
REACT_APP_API_URL=https://your-actual-railway-url.up.railway.app
```

And update the `frontend/vercel.json` proxy destination to match.

## 🔧 Key Configuration Points

### **Vercel Settings:**
- ✅ **Root Directory**: `frontend` (not root)
- ✅ **Framework**: `Other` (not auto-detect)
- ✅ **Build Command**: `npm run build`
- ✅ **Output Directory**: `build`

### **File Structure:**
```
Bernstein/
├── frontend/           ← Vercel root directory
│   ├── package.json
│   ├── public/
│   │   └── index.html  ← Main app file
│   ├── vercel.json     ← Deployment config
│   └── ...
└── backend/           ← Railway root directory
    ├── main.py
    ├── railway.json
    └── ...
```

## 🎯 Expected Result

After fixing the configuration:
- **Frontend**: `https://bernstein-eight.vercel.app/` → Working React app
- **Backend**: `https://backend-production-a33c.up.railway.app/` → API endpoints
- **Connection**: Vercel proxy forwards `/api/*` calls to Railway

The 404 error should be resolved once the root directory is set to `frontend` in Vercel settings!
