# Deployment Guide

This guide provides step-by-step instructions for deploying the Interactive Dictionary application to Render.

## Prerequisites

- A GitHub account
- A Render account (free tier works fine)
- A Mistral AI API key (get one at https://console.mistral.ai/)

## Step-by-Step Deployment

### 1. Prepare Your Code

Ensure your code is pushed to a GitHub repository:

```bash
git add .
git commit -m "Prepare for Render deployment"
git push origin main
```

### 2. Create Render Account

1. Go to [Render.com](https://render.com/)
2. Sign up for a free account (or log in if you already have one)
3. Connect your GitHub account when prompted

### 3. Create New Web Service

1. In the Render dashboard, click **"New +"** button
2. Select **"Web Service"**
3. Connect your GitHub repository
4. Select the repository containing this project

### 4. Configure Service

Render will auto-detect settings from `render.yaml`, but you can also configure manually:

**Basic Settings:**
- **Name:** `interactive-dictionary` (or your preferred name)
- **Region:** Choose closest to your users
- **Branch:** `main` (or your default branch)
- **Root Directory:** Leave empty (if project is at repo root)

**Build & Deploy:**
- **Build Command:** `pip install -r requirements.txt`
- **Start Command:** `gunicorn app:app`
- **Environment:** `Python 3`

### 5. Set Environment Variables

In the Render dashboard, go to **Environment** section and add:

- **Key:** `MISTRAL_API_KEY`
- **Value:** Your Mistral AI API key (keep this secret!)

Optional environment variables:
- **Key:** `FLASK_DEBUG`
- **Value:** `False` (for production)

- **Key:** `PORT`
- **Value:** Automatically set by Render (don't override)

### 6. Deploy

1. Click **"Create Web Service"**
2. Render will start building your application
3. Watch the build logs for any errors
4. Once deployed, you'll get a URL like: `https://interactive-dictionary.onrender.com`

### 7. Test Your Deployment

Visit your app URL and test:
- Loading the main page
- Clicking on words to get translations
- Batch processing words

## Troubleshooting

### Build Fails

- Check build logs in Render dashboard
- Ensure all dependencies are in `requirements.txt`
- Verify Python version in `runtime.txt` is compatible

### App Crashes on Start

- Check logs in Render dashboard
- Verify `MISTRAL_API_KEY` is set correctly
- Ensure `Procfile` has correct start command

### 502 Bad Gateway

- Check if app is running in logs
- Verify port configuration
- Check if gunicorn is properly installed

### API Errors

- Verify `MISTRAL_API_KEY` environment variable is set
- Check Mistral AI API status
- Review application logs for detailed error messages

## Important Notes

### Free Tier Limitations

- **Spin-down:** Apps on free tier spin down after 15 minutes of inactivity
- **First request:** May take 30-60 seconds to wake up
- **Persistent storage:** File-based cache (`data/translations.json`) is ephemeral and resets on each deploy

### Upgrade Considerations

For production use, consider:
- Upgrading to a paid Render plan for always-on service
- Using a database (PostgreSQL) for persistent cache storage
- Adding monitoring and alerting
- Setting up custom domain with SSL

### Scaling

For higher traffic:
- Upgrade Render service plan
- Consider adding a database for caching
- Implement rate limiting
- Use CDN for static assets

## Alternative Platforms

### Heroku

1. Install Heroku CLI
2. Run: `heroku create`
3. Set environment variables: `heroku config:set MISTRAL_API_KEY=your_key`
4. Deploy: `git push heroku main`

### Railway

1. Connect GitHub repository
2. Railway auto-detects Python app
3. Set environment variables
4. Deploy automatically

### Fly.io

1. Install flyctl: `curl -L https://fly.io/install.sh | sh`
2. Run: `fly launch`
3. Set secrets: `fly secrets set MISTRAL_API_KEY=your_key`
4. Deploy: `fly deploy`

## Monitoring

After deployment, monitor:
- Application logs in Render dashboard
- Response times
- API usage and costs
- Error rates

For production monitoring, consider:
- Sentry for error tracking
- Datadog or New Relic for performance monitoring
- Uptime monitoring services

