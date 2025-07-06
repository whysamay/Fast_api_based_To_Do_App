# 🚀 Deployment Guide

This guide will help you deploy your Todo Hub application to production.

## 📋 Prerequisites

- GitHub account
- Railway account (free at railway.app)
- Vercel account (free at vercel.com)

## 🎯 Step-by-Step Deployment

### **Step 1: Deploy Backend to Railway**

1. **Push your code to GitHub:**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Deploy to Railway:**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository
   - Railway will automatically detect it's a Python app

3. **Configure Environment Variables:**
   - In Railway dashboard, go to your project
   - Click "Variables" tab
   - Add: `FRONTEND_URL=https://your-frontend-domain.vercel.app`
   - Railway will provide your backend URL (e.g., `https://your-app.railway.app`)

4. **Get your backend URL:**
   - Railway will give you a URL like: `https://your-app.railway.app`
   - Save this URL for the next step

### **Step 2: Deploy Frontend to Vercel**

1. **Go to Vercel:**
   - Visit [vercel.com](https://vercel.com)
   - Sign up with GitHub

2. **Import your repository:**
   - Click "New Project"
   - Import your GitHub repository
   - Set the root directory to: `ToDoApp/todo-frontend`

3. **Configure Environment Variables:**
   - In Vercel project settings
   - Go to "Environment Variables"
   - Add: `REACT_APP_API_URL=https://your-backend-url.railway.app`
   - Replace with your actual Railway backend URL

4. **Deploy:**
   - Click "Deploy"
   - Vercel will build and deploy your React app
   - You'll get a URL like: `https://your-app.vercel.app`

### **Step 3: Update CORS Settings**

1. **Update your backend CORS:**
   - Go back to Railway
   - Add environment variable: `FRONTEND_URL=https://your-frontend-url.vercel.app`
   - Replace with your actual Vercel frontend URL

2. **Redeploy backend:**
   - Railway will automatically redeploy when you add environment variables

## 🔧 Alternative Deployment Options

### **Backend Alternatives:**
- **Render**: Similar to Railway, free tier available
- **Heroku**: Classic choice (paid now)
- **DigitalOcean App Platform**: Good performance
- **AWS EC2**: More control, requires more setup

### **Frontend Alternatives:**
- **Netlify**: Great alternative to Vercel
- **GitHub Pages**: Free static hosting
- **AWS S3 + CloudFront**: Scalable solution

## 🐛 Troubleshooting

### **Common Issues:**

1. **CORS Errors:**
   - Make sure your backend CORS includes your frontend URL
   - Check environment variables are set correctly

2. **API Connection Issues:**
   - Verify `REACT_APP_API_URL` is set correctly in Vercel
   - Check your backend URL is accessible

3. **Database Issues:**
   - Railway provides a PostgreSQL database
   - Update your database connection if needed

### **Debugging:**
- Check Railway logs for backend errors
- Check Vercel build logs for frontend errors
- Use browser dev tools to see API calls

## 🎉 Success!

Once deployed, your app will be available at:
- **Frontend**: `https://your-app.vercel.app`
- **Backend**: `https://your-app.railway.app`

## 📝 Next Steps

1. **Custom Domain** (optional):
   - Add custom domain in Vercel
   - Update CORS settings accordingly

2. **Database Migration**:
   - If using Railway's PostgreSQL, update database.py
   - Run migrations: `alembic upgrade head`

3. **Environment Variables**:
   - Set `SECRET_KEY` for production
   - Configure database URLs

4. **Monitoring**:
   - Set up logging
   - Monitor performance

---

**Your app is now live! 🚀** 