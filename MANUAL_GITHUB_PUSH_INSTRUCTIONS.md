# 🚨 MANUAL GITHUB PUSH INSTRUCTIONS

## The Issue
Railway is failing because it's using Nixpacks which has a bug with pip. The solution is to use Docker instead.

## ✅ Solution: Push Dockerfile to GitHub

### Step 1: Open Terminal
Open a **new terminal window** (not the one in VS Code) and run these commands:

```bash
cd /Users/michaelkim/code/Bernstein
```

### Step 2: Initialize Git (if needed)
```bash
git init
git remote add origin https://github.com/MikeVenge/bernstein.git
```

### Step 3: Add and Commit Files
```bash
git add -A
git commit -m "Add Dockerfile to fix Railway deployment - bypass Nixpacks pip error"
```

### Step 4: Push to GitHub
```bash
git push -f origin HEAD:main
```

If that doesn't work, try:
```bash
git push --set-upstream origin main
```

### Step 5: Verify on GitHub
Go to: https://github.com/MikeVenge/bernstein

**You should see these files:**
- ✅ `Dockerfile` (NEW - this fixes Railway!)
- ✅ `main.py`
- ✅ `requirements.txt`
- ✅ `parameterized_field_mapper.py`
- ✅ `GENERIC_FIELD_MAPPINGS.csv`
- ✅ `index.html`

## 🚂 Step 6: Redeploy on Railway

Once the Dockerfile is on GitHub:

1. Go to your Railway project
2. Click on your service
3. Go to **Settings → Deploy**
4. Click **Redeploy** or trigger a new deployment

**Railway will automatically detect the Dockerfile and use it instead of Nixpacks!**

## 🎯 Why This Works

- **Dockerfile > Nixpacks**: Railway prioritizes Dockerfile over Nixpacks
- **No pip errors**: Standard Python Docker image has working pip
- **Simple build**: Just installs requirements and runs the app

## 📝 The Dockerfile Contents

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .
COPY parameterized_field_mapper.py .
COPY GENERIC_FIELD_MAPPINGS.csv .
RUN mkdir -p uploads results
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## 🔧 Alternative: Direct GitHub Upload

If git push still doesn't work:

1. Go to https://github.com/MikeVenge/bernstein
2. Click **"Add file" → "Upload files"**
3. Drag and drop the `Dockerfile` from `/Users/michaelkim/code/Bernstein/`
4. Commit with message: "Add Dockerfile to fix Railway deployment"

## ✅ Expected Result

After Railway redeploys with the Dockerfile:
- ✅ No more Nixpacks pip errors
- ✅ Clean Docker build
- ✅ FastAPI backend running
- ✅ Your app deployed successfully!

---

**Need help?** The Dockerfile is ready at:
`/Users/michaelkim/code/Bernstein/Dockerfile`
