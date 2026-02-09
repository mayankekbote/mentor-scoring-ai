# Render.com Deployment Guide

## Prerequisites

1. **GitHub Account** - Your code must be on GitHub
2. **Render.com Account** - Sign up at https://render.com (free)

---

## Step-by-Step Deployment

### 1. Push Code to GitHub

First, push your code to GitHub (if not already done):

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/mayankekbote/mentor-scoring-ai.git
git push -u origin main
```

### 2. Create Render.com Account

1. Go to https://render.com
2. Sign up with GitHub
3. Authorize Render to access your repositories

### 3. Create New Web Service

1. Click **"New +"** → **"Web Service"**
2. Connect your GitHub repository: `mentor-scoring-ai`
3. Configure the service:

   **Settings:**
   - **Name**: `mentor-scoring-ai`
   - **Region**: Choose closest to you
   - **Branch**: `main`
   - **Root Directory**: (leave empty)
   - **Runtime**: `Python 3`
   - **Build Command**: `./render-build.sh`
   - **Start Command**: `streamlit run app.py --server.port=$PORT --server.address=0.0.0.0`

### 4. Add Environment Variables

In the **Environment** section, add:

```
OPENAI_API_KEY=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

GROQ_API_KEY=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
```

### 5. Choose Plan

- **Free Tier**: Available (with limitations)
  - 750 hours/month free
  - Sleeps after 15 min of inactivity
  - Slower performance

- **Starter Plan**: $7/month
  - Always on
  - Better performance

### 6. Deploy

1. Click **"Create Web Service"**
2. Wait for deployment (~5-10 minutes)
3. Your app will be live at: `https://mentor-scoring-ai.onrender.com`

---

## Important Notes

### ✅ What Works on Render.com

- ✅ ffmpeg (installed via build script)
- ✅ All Python dependencies
- ✅ File uploads (temporary)
- ✅ API calls (OpenAI, Groq)

### ⚠️ Limitations

- **Free tier sleeps** after 15 min inactivity (takes ~30s to wake up)
- **Slow video processing** on free tier (CPU-only)
- **No persistent storage** - uploaded videos deleted after processing
- **750 hours/month limit** on free tier

### 💡 Performance Tips

1. **Use shorter videos** for demos (1-5 minutes)
2. **Upgrade to Starter plan** ($7/month) for better performance
3. **Keep app awake** with a ping service (e.g., UptimeRobot)

---

## Troubleshooting

### Build Fails

**Error**: `permission denied: ./render-build.sh`

**Solution**: Make script executable:
```bash
chmod +x render-build.sh
git add render-build.sh
git commit -m "Make build script executable"
git push
```

### App Crashes

**Error**: `ModuleNotFoundError`

**Solution**: Check `requirements.txt` has all dependencies

### ffmpeg Not Found

**Error**: `ffmpeg: command not found`

**Solution**: Verify `render-build.sh` is running correctly in build logs

---

## Cost Estimate

### Free Tier
- **Cost**: $0
- **Limitations**: Sleeps after 15 min, slower

### Starter Plan ($7/month)
- **Cost**: $7/month
- **Benefits**: Always on, faster

### Usage Costs (APIs)
- **OpenAI**: ~$0.01 per 10-min video
- **Groq**: FREE

**Total for 100 videos/month**: ~$1 (OpenAI) + $0-7 (Render)

---

## Alternative: Local Deployment

For a college project, **running locally** might be better:

**Pros:**
- ✅ Free
- ✅ Faster (uses your CPU)
- ✅ No deployment complexity
- ✅ Privacy (videos stay local)

**Cons:**
- ❌ Not accessible online
- ❌ Each team member needs to run it

---

## Next Steps

1. **Push to GitHub** (if not done)
2. **Sign up on Render.com**
3. **Follow steps above**
4. **Share the URL** with your team!

Your app will be live at: `https://mentor-scoring-ai.onrender.com`
