# Deployment Guide: Quarterly Earning Field Mapper

## 🚀 Railway Backend Deployment

### Project Details:
- **Railway Project ID**: `a33c9b9d-889b-427d-aba8-6240ca22d770`
- **Service**: Quarterly Earning Field Mapper Backend API

### Deployment Steps:

1. **Connect Repository to Railway**:
   - Go to [Railway Dashboard](https://railway.app/dashboard)
   - Select your project: `a33c9b9d-889b-427d-aba8-6240ca22d770`
   - Connect your GitHub repository (`Bernstein`)

2. **Configure Service Settings**:
   ```bash
   Root Directory: backend
   Build Command: pip install -r requirements.txt
   Start Command: uvicorn main:app --host 0.0.0.0 --port $PORT --workers 1
   ```

3. **Environment Variables**:
   ```bash
   RAILWAY_PROJECT_ID=a33c9b9d-889b-427d-aba8-6240ca22d770
   RAILWAY_ENVIRONMENT=production
   CORS_ORIGINS=https://bernstein-mike-adgoios-projects.vercel.app
   ```

4. **Deploy**:
   - Push changes to GitHub
   - Railway will automatically deploy from the `backend` directory

### Expected Railway URLs:
- **API**: `https://backend-production-xxxx.up.railway.app`
- **Health Check**: `https://backend-production-xxxx.up.railway.app/`
- **API Docs**: `https://backend-production-xxxx.up.railway.app/docs`

## 🌐 Vercel Frontend Deployment

### Project Details:
- **Vercel Project**: [https://vercel.com/mike-adgoios-projects/bernstein](https://vercel.com/mike-adgoios-projects/bernstein)

### Deployment Steps:

1. **In Vercel Dashboard**:
   - Click "Connect Git" 
   - Select your `Bernstein` repository
   - Configure build settings:

2. **Build Configuration**:
   ```bash
   Framework Preset: Other
   Root Directory: frontend
   Build Command: npm run build
   Output Directory: build
   Install Command: npm install
   ```

3. **Environment Variables**:
   ```bash
   REACT_APP_API_URL=https://backend-production-xxxx.up.railway.app
   REACT_APP_APP_NAME=Quarterly Earning Field Mapper
   ```

4. **Domain Configuration**:
   - Primary domain: `https://bernstein-mike-adgoios-projects.vercel.app`
   - Custom domain (optional): `quarterly-earning-field-mapper.vercel.app`

## 🔗 Cross-Platform Configuration

### Update Backend CORS for Vercel:
After Vercel deployment, update Railway environment variables:
```bash
CORS_ORIGINS=https://bernstein-mike-adgoios-projects.vercel.app,https://quarterly-earning-field-mapper.vercel.app
```

### Update Frontend API URL:
After Railway deployment, update Vercel environment variables:
```bash
REACT_APP_API_URL=https://your-railway-backend-url.up.railway.app
```

## 📊 Deployment Checklist

### Railway Backend:
- [ ] Repository connected
- [ ] Root directory set to `backend`
- [ ] Environment variables configured
- [ ] Deployment successful
- [ ] Health check responding
- [ ] API docs accessible

### Vercel Frontend:
- [ ] Repository connected
- [ ] Root directory set to `frontend`
- [ ] Build settings configured
- [ ] Environment variables set
- [ ] Deployment successful
- [ ] Frontend accessible
- [ ] Backend connectivity working

## 🧪 Testing Production Deployment

### Backend Testing:
```bash
curl https://your-railway-url.up.railway.app/
curl https://your-railway-url.up.railway.app/docs
```

### Frontend Testing:
1. Visit your Vercel URL
2. Check backend connection status (should be green)
3. Upload test files
4. Execute mapping
5. Download results

## 🎯 Final URLs

Once deployed, your application will be available at:
- **Frontend**: `https://bernstein-mike-adgoios-projects.vercel.app`
- **Backend**: `https://backend-production-[hash].up.railway.app`

## 🔧 Troubleshooting

### Common Issues:
1. **CORS Errors**: Ensure Vercel URL is in Railway CORS_ORIGINS
2. **Build Failures**: Check that root directories are set correctly
3. **API Connection**: Verify REACT_APP_API_URL points to Railway backend
4. **File Upload Limits**: Railway has file size limits for uploads

### Monitoring:
- **Railway**: Check logs in Railway dashboard
- **Vercel**: Check function logs in Vercel dashboard
- **Health Checks**: Monitor `/` endpoint for backend health

Your Quarterly Earning Field Mapper is configured for professional deployment on Railway and Vercel!
