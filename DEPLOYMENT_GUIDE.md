# Deployment Guide - Render + Vercel

This guide walks you through deploying the Diabetic Ulcer AI Detection System to production.

## Architecture

- **Backend**: FastAPI on Render (Free tier)
- **Frontend**: React on Vercel (Free tier)
- **Database**: SQLite (included with backend)
- **ML Models**: Deployed with backend (or use pretrained weights)

---

## Prerequisites

1. GitHub account with your code pushed
2. Render account (https://render.com)
3. Vercel account (https://vercel.com)

---

## Part 1: Deploy Backend to Render

### Step 1: Prepare Your Repository

Ensure these files are in your repo:
- ✅ `render.yaml` (already configured)
- ✅ `backend/requirements.txt`
- ✅ `.gitignore` (excludes large folders)

### Step 2: Connect to Render

1. Go to https://dashboard.render.com
2. Click **"New +"** → **"Blueprint"**
3. Connect your GitHub repository
4. Render will automatically detect `render.yaml`
5. Click **"Apply"**

### Step 3: Configure Environment Variables

Render will use the variables from `render.yaml`, but you should update:

1. Go to your service → **Environment** tab
2. Update these critical variables:

```bash
# Generate secure keys (run locally):
python -c "import secrets; print(secrets.token_hex(32))"

# Update in Render dashboard:
SECRET_KEY=<generated-key-1>
JWT_SECRET_KEY=<generated-key-2>
```

3. After frontend deployment, update:
```bash
FRONTEND_URL=https://your-app.vercel.app
ALLOWED_ORIGINS=https://your-app.vercel.app
```

### Step 4: Deploy

- Render will automatically build and deploy
- Wait 5-10 minutes for first deployment
- Check logs for any errors

### Step 5: Verify Backend

Visit your backend URL (e.g., `https://medvision-ai-backend.onrender.com`):

- `/health` - Should return `{"status": "healthy"}`
- `/docs` - Should show API documentation
- `/` - Should return API info

**Copy your backend URL** - you'll need it for frontend deployment.

---

## Part 2: Deploy Frontend to Vercel

### Step 1: Prepare Frontend

1. Update `frontend/.env.production`:
```bash
VITE_API_BASE_URL=https://your-backend.onrender.com
```

2. Commit and push changes

### Step 2: Connect to Vercel

1. Go to https://vercel.com/dashboard
2. Click **"Add New"** → **"Project"**
3. Import your GitHub repository
4. Configure project:
   - **Framework Preset**: Vite
   - **Root Directory**: `frontend`
   - **Build Command**: `npm run build`
   - **Output Directory**: `dist`

### Step 3: Configure Environment Variables

In Vercel project settings → **Environment Variables**:

```bash
VITE_API_BASE_URL=https://your-backend.onrender.com
```

### Step 4: Deploy

- Click **"Deploy"**
- Wait 2-3 minutes
- Vercel will provide your frontend URL

### Step 5: Update Backend CORS

Go back to Render → Your service → **Environment**:

```bash
FRONTEND_URL=https://your-app.vercel.app
ALLOWED_ORIGINS=https://your-app.vercel.app
```

Save and redeploy backend.

---

## Part 3: Verify Full Deployment

### Test Backend
```bash
curl https://your-backend.onrender.com/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "medvision_ai_diabetic_ulcer_detection",
  "version": "1.0.0"
}
```

### Test Frontend
1. Visit `https://your-app.vercel.app`
2. Try uploading an image
3. Check browser console for errors
4. Verify API calls are going to Render backend

---

## Local Development

### Backend
```bash
# Create virtual environment
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp ../.env.template ../.env

# Edit .env with your local settings

# Run backend
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend
```bash
cd frontend

# Install dependencies
npm install

# Copy environment template
cp .env.template .env.local

# Edit .env.local
# VITE_API_BASE_URL=http://localhost:8000

# Run frontend
npm run dev
```

Visit: http://localhost:5173

---

## Troubleshooting

### Backend Issues

**Problem**: Build fails on Render
- Check `render.yaml` build command
- Verify `requirements.txt` is in `backend/` folder
- Check Render logs for specific errors

**Problem**: Backend crashes on startup
- Check environment variables in Render dashboard
- Verify `DATABASE_URL` is set
- Check logs: Models missing is OK (uses pretrained weights)

**Problem**: 502 Bad Gateway
- Backend is still starting (wait 2-3 minutes)
- Check Render logs for errors
- Verify health check endpoint works

### Frontend Issues

**Problem**: API calls fail (CORS errors)
- Verify `ALLOWED_ORIGINS` in Render includes your Vercel URL
- Check browser console for exact error
- Verify `VITE_API_BASE_URL` in Vercel environment variables

**Problem**: Build fails on Vercel
- Check build logs
- Verify `package.json` has correct scripts
- Ensure `vite.config.js` is present

**Problem**: 404 on page refresh
- Vercel should handle this with `vercel.json` rewrites
- Verify `vercel.json` is in `frontend/` folder

### Database Issues

**Problem**: Database resets on Render
- Free tier uses ephemeral storage
- Upgrade to paid tier for persistent disk
- Or use external PostgreSQL database

---

## ML Models

### Option 1: Deploy with Models (Recommended)
```bash
# Ensure models are in backend/models/
backend/models/best_dfu_model.pth
backend/models/segmentation_model.pth
backend/models/multimodal_model.pth

# Commit to git (if < 100MB each)
git add backend/models/*.pth
git commit -m "Add ML models"
git push
```

### Option 2: Use Pretrained Weights
- Backend will automatically use ImageNet pretrained weights
- Accuracy may be lower but system will work
- Train models later and redeploy

### Option 3: External Model Storage
- Upload models to cloud storage (S3, Google Cloud Storage)
- Update model loading logic to download from cloud
- Recommended for large models (>100MB)

---

## Environment Variables Reference

### Backend (Render)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `SECRET_KEY` | ✅ Yes | - | JWT signing key |
| `JWT_SECRET_KEY` | ✅ Yes | - | JWT token key |
| `DATABASE_URL` | No | SQLite | Database connection |
| `FRONTEND_URL` | ✅ Yes | - | Frontend URL for CORS |
| `ALLOWED_ORIGINS` | ✅ Yes | - | CORS allowed origins |
| `ENVIRONMENT` | No | production | Environment name |
| `DEBUG` | No | False | Debug mode |

### Frontend (Vercel)

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `VITE_API_BASE_URL` | ✅ Yes | - | Backend API URL |

---

## Cost Estimate

### Free Tier (Both platforms)
- **Render**: 750 hours/month free
- **Vercel**: Unlimited deployments
- **Total**: $0/month

### Limitations
- Render free tier sleeps after 15 min inactivity
- First request after sleep takes 30-60 seconds
- SQLite database resets on redeploy

### Paid Tier (Recommended for production)
- **Render**: $7/month (persistent disk, no sleep)
- **Vercel**: Free (sufficient for most use cases)
- **Total**: $7/month

---

## Next Steps

1. ✅ Deploy backend to Render
2. ✅ Deploy frontend to Vercel
3. ✅ Update CORS settings
4. ✅ Test full application
5. 🔄 Set up custom domain (optional)
6. 🔄 Configure monitoring (optional)
7. 🔄 Set up CI/CD (optional)

---

## Support

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **FastAPI Docs**: https://fastapi.tiangolo.com
- **Vite Docs**: https://vitejs.dev

---

## Security Checklist

- [ ] Changed `SECRET_KEY` from default
- [ ] Changed `JWT_SECRET_KEY` from default
- [ ] Updated `ALLOWED_ORIGINS` with actual frontend URL
- [ ] Removed sensitive data from `.env` (not committed)
- [ ] Verified `.gitignore` excludes secrets
- [ ] Enabled HTTPS (automatic on Render/Vercel)
- [ ] Reviewed API authentication endpoints

---

**Deployment complete!** 🚀

Your Diabetic Ulcer AI Detection System is now live in production.
