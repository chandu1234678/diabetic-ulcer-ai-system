# Quick Start - Deploy in 10 Minutes

## 1. Backend (Render)

```bash
# 1. Push code to GitHub
git add .
git commit -m "Ready for deployment"
git push

# 2. Go to Render Dashboard
# https://dashboard.render.com

# 3. New → Blueprint → Connect GitHub repo

# 4. Generate secure keys (run locally):
python -c "import secrets; print('SECRET_KEY:', secrets.token_hex(32)); print('JWT_SECRET_KEY:', secrets.token_hex(32))"

# 5. Update environment variables in Render:
# - SECRET_KEY=<generated-key-1>
# - JWT_SECRET_KEY=<generated-key-2>

# 6. Deploy and copy backend URL
# Example: https://medvision-ai-backend.onrender.com
```

## 2. Frontend (Vercel)

```bash
# 1. Update frontend/.env.production
VITE_API_BASE_URL=https://your-backend.onrender.com

# 2. Commit and push
git add frontend/.env.production
git commit -m "Update production API URL"
git push

# 3. Go to Vercel Dashboard
# https://vercel.com/dashboard

# 4. New Project → Import GitHub repo

# 5. Configure:
# - Framework: Vite
# - Root Directory: frontend
# - Build Command: npm run build
# - Output Directory: dist

# 6. Add environment variable:
# VITE_API_BASE_URL=https://your-backend.onrender.com

# 7. Deploy and copy frontend URL
# Example: https://your-app.vercel.app
```

## 3. Update CORS

```bash
# Go back to Render → Environment → Update:
FRONTEND_URL=https://your-app.vercel.app
ALLOWED_ORIGINS=https://your-app.vercel.app

# Save and redeploy
```

## 4. Test

```bash
# Backend health check
curl https://your-backend.onrender.com/health

# Frontend
# Visit: https://your-app.vercel.app
```

## Done! 🚀

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

---

## Local Development

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.template ../.env
# Edit .env with local settings
uvicorn app.main:app --reload

# Frontend (new terminal)
cd frontend
npm install
cp .env.template .env.local
# Edit .env.local: VITE_API_BASE_URL=http://localhost:8000
npm run dev
```

Visit: http://localhost:5173

---

## Troubleshooting

**Backend 502 Error**: Wait 2-3 minutes (cold start)

**CORS Error**: Update `ALLOWED_ORIGINS` in Render with Vercel URL

**Models Missing**: OK! Backend uses pretrained weights

**Build Fails**: Check logs in Render/Vercel dashboard

---

## Environment Variables Checklist

### Render (Backend)
- [x] SECRET_KEY (generated)
- [x] JWT_SECRET_KEY (generated)
- [x] FRONTEND_URL (Vercel URL)
- [x] ALLOWED_ORIGINS (Vercel URL)

### Vercel (Frontend)
- [x] VITE_API_BASE_URL (Render URL)

---

**Need help?** See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)
