# Vercel Deployment Guide

## 🚀 Deploy in 3 Steps

### Step 1: Create Vercel Account
Go to: https://vercel.com/signup
Sign up with GitHub

### Step 2: Connect Repository
1. Go to https://vercel.com/new
2. Select "Import Git Repository"
3. Paste: https://github.com/Ahmed123alam/ai-crypto-trading-os
4. Click "Import"

### Step 3: Configure Environment
1. Add Environment Variables:
   - NEXT_PUBLIC_API_URL = http://localhost:8000
   - NEXT_PUBLIC_WS_URL = ws://localhost:8000/ws
2. Click "Deploy"

### Done! 🎉
Your dashboard is now live at: https://your-project-name.vercel.app

---

## 📌 Important Notes

⚠️ For full functionality, you still need to run the backend locally:

```bash
docker-compose up -d
```

OR upgrade to a paid plan to host backend on cloud.

---

## 🔗 After Deployment

Your live URL will look like:
```
https://ai-crypto-trading-os.vercel.app
```

Share this URL to access your dashboard from anywhere! 🌍
