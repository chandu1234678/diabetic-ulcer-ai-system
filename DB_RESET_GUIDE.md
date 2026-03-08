# Database Reset Guide for Render Deployment

## Problem Summary
You're getting "email already exists" when creating account and "invalid credentials" when logging in. This indicates the Render PostgreSQL database has corrupted or old test data.

## Quick Fix (Recommended)

### Option 1: Reset via Render Shell (Fastest)

1. **Go to Render Dashboard**: https://dashboard.render.com

2. **Select your medvision-db PostgreSQL service**

3. **Click "Shell"** at the top right

4. **Run this command** to connect to database:
   ```bash
   psql $DATABASE_URL
   ```

5. **Drop all tables** (this clears all data):
   ```sql
   -- Clear all user data
   DELETE FROM users;
   DELETE FROM patients;
   DELETE FROM prediction_logs;
   DELETE FROM ulcer_images;
   DELETE FROM health_metrics;
   
   \q
   ```

6. **Restart your backend service**:
   - Go to medvision-backend service
   - Click "Manual Deploy" > "Latest" in bottom right

7. **Try creating account again** - should work now!

---

### Option 2: Run Python Diagnostic Script

**Locally** (to test, or to prepare for Render):

```bash
# 1. Navigate to backend folder
cd backend

# 2. Activate virtual environment
# Windows:
venv\Scripts\activate

# 3. Check database status
python fix_database.py --check

# 4. List all users
python fix_database.py --list-users

# 5. Remove test users
python fix_database.py --clean-users

# 6. NUCLEAR OPTION: Reset everything (deletes ALL data)
python fix_database.py --reset
```

Then commit and push to trigger Render redeploy.

---

### Option 3: Via Render CLI

```bash
# 1. Install Render CLI (if not already)
npm install -g @render-com/cli

# 2. Login to Render
render login

# 3. Run the fix script on Render
render run python fix_database.py --reset
```

---

## Verification

After reset, test these:

1. **Create Account**:
   - Email: test@example.com  
   - Password: Test@1234567

2. **Try Login** with same credentials

3. **Check Dashboard** - should show health metrics

---

## What Causes This Issue

- Old test data in database from previous deployments
- Duplicate email entries  
- Schema mismatch between code and database
- Database wasn't properly initialized on deployment

## Prevention

To prevent future issues:

1. **Use fresh database** for each major deployment
2. **Add database version checks** to backend startup
3. **Create database backups** before major changes
4. **Use migration tools** (Alembic) instead of `create_all()`

---

## Recommended Next Steps

After database is reset:

1. ✅ Create your real account
2. ✅ Test the health metrics form we just added
3. ✅ Verify auto-fill works on upload page
4. ✅ Test full workflow (upload → analyze → results)

---

## Still Having Issues?

If problem persists after reset:

1. Check backend logs on Render:
   ```
   Render Dashboard > medvision-backend > Logs
   ```

2. Look for errors like:
   - "DATABASE_URL not set"
   - "Connection refused"  
   - "Permission denied"

3. Verify environment variables:
   ```
   Render Dashboard > medvision-backend > Environment
   ```
   Should have: `DATABASE_URL`, `JWT_SECRET_KEY`, etc.

---
