# Deploy FREE Rembg Background Removal Service

## ✅ What You Get
- **100% FREE** background removal (no API costs!)
- Unlimited usage
- Same quality as remove.bg
- Self-hosted, no rate limits

## 🚀 Quick Deploy to Railway (Recommended - FREE)

### Step 1: Deploy Rembg Service

1. Go to https://railway.app
2. Sign up with GitHub (free)
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your `jogotop` repo
5. Set **Root Directory**: `rembg-service`
6. Railway will auto-detect the Dockerfile and deploy!
7. Copy the public URL (e.g., `https://your-app.railway.app`)

### Step 2: Update Supabase Edge Function

1. Go to Supabase Dashboard → Edge Functions
2. Add environment variable:
   - Key: `REMBG_SERVICE_URL`
   - Value: `https://your-app.railway.app` (from Railway)

3. Redeploy the `generate-genesis-portrait` function:
```bash
npx supabase functions deploy generate-genesis-portrait
```

### Step 3: Test It!

Redeem a crest and watch the logs - you should see:
```
🎭 Removing background with Rembg (FREE)...
✅ Background removed (FREE with Rembg)
```

## 🎯 Alternative: Deploy to Render.com (Also FREE)

1. Go to https://render.com
2. New → Web Service
3. Connect your GitHub repo
4. Root Directory: `rembg-service`
5. Build Command: `pip install -r requirements.txt`
6. Start Command: `python app.py`
7. Copy the URL and add to Supabase as `REMBG_SERVICE_URL`

## 🎯 Alternative: Deploy to Hugging Face Spaces (FREE)

1. Go to https://huggingface.co/spaces
2. Create new Space
3. Upload `app.py` and `requirements.txt`
4. Space type: Gradio (or Flask)
5. Copy the URL and add to Supabase

## 💰 Cost Comparison

| Service | Cost per 1000 images | Quality |
|---------|---------------------|---------|
| remove.bg | $200 | Excellent |
| **Rembg (Railway)** | **$0** | Very Good |
| Clipdrop free tier | $0 (100 limit) | Excellent |

## 🔧 Troubleshooting

**If background removal fails:**
1. Check Railway logs for errors
2. Verify `REMBG_SERVICE_URL` is set correctly in Supabase
3. Test the service directly: `curl https://your-app.railway.app/`

**If Railway goes to sleep (free tier):**
- First request might be slow (cold start)
- Consider upgrading to Railway Pro ($5/mo) for always-on

## ✅ You're Done!

Your gangster portraits now use FREE background removal! 🎉

No more API costs, unlimited usage, same quality!
