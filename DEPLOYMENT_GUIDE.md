# 🚀 Budget Coach Deployment Guide

## Quick Deployment Options

### Option 1: Streamlit Cloud (Recommended - FREE)

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Ready for deployment"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud:**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file path to: `streamlit_app.py`
   - Click "Deploy!"

3. **Your app will be live at:** `https://your-app-name.streamlit.app`

### Option 2: Railway (Alternative)

1. **Connect to Railway:**
   - Go to [railway.app](https://railway.app)
   - Connect your GitHub repository
   - Railway will auto-detect it's a Streamlit app

2. **Set environment variables (if needed):**
   - DATABASE_PATH=/tmp/budget_coach.db

### Option 3: Heroku

1. **Create these files:**
   - `Procfile` (already created)
   - `setup.sh` (already created)

2. **Deploy to Heroku:**
   ```bash
   heroku create your-app-name
   git push heroku main
   ```

## Files in Your Project

- ✅ `streamlit_app.py` - Main app file
- ✅ `requirements.txt` - Dependencies  
- ✅ `.streamlit/config.toml` - Configuration
- ✅ `Procfile` - For Heroku deployment
- ✅ `setup.sh` - For Heroku setup

## Troubleshooting

### Common Issues:

1. **"Module not found" errors:**
   - Check that all dependencies are in `requirements.txt`
   - Make sure versions are compatible

2. **Database issues:**
   - The app automatically falls back to in-memory database if file system is read-only
   - Data won't persist between sessions on some platforms

3. **Authentication problems:**
   - Clear browser cache and cookies
   - Try incognito/private browsing mode

### Need Help?

Contact **K.Muhammad Obi**:
- 📧 Email: [muhammadkarangwa07@gmail.com](mailto:muhammadkarangwa07@gmail.com)
- 📱 Instagram: [@obi_karangwa](https://instagram.com/obi_karangwa)

## Quick Test

Test your app locally first:
```bash
pip install -r requirements.txt
streamlit run streamlit_app.py
``` 