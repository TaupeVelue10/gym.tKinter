# Workout Program Generator - Deployment Guide

## Deploy to Render

### Quick Deploy (Recommended)

1. **Push your code to GitHub** (if not already done):
   ```bash
   git add .
   git commit -m "Add Render deployment files"
   git push origin kivy-version
   ```

2. **Sign up/Login to Render**:
   - Go to [render.com](https://render.com)
   - Sign up with your GitHub account

3. **Create a New Web Service**:
   - Click "New +" → "Web Service"
   - Connect your GitHub account if needed
   - Select your repository: `AlexPeirano/gym.tKinter`
   - Select branch: `kivy-version`

4. **Configure the service**:
   - **Name**: `workout-program-generator` (or any name you prefer)
   - **Region**: Choose closest to you
   - **Root Directory**: `version_site`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `gunicorn app:app`
   - **Plan**: Select "Free"

5. **Add Environment Variable**:
   - Click "Advanced"
   - Add environment variable:
     - Key: `FLASK_SECRET_KEY`
     - Value: Generate a random string (or let Render auto-generate)
   - Add another variable:
     - Key: `FLASK_ENV`
     - Value: `production`

6. **Deploy**:
   - Click "Create Web Service"
   - Render will automatically build and deploy your app
   - Wait 2-5 minutes for the first deployment

7. **Access your app**:
   - Once deployed, you'll get a URL like: `https://workout-program-generator.onrender.com`
   - Your app will be live at this URL!

### Alternative: Blueprint Deploy

If you see a `render.yaml` file, you can use Blueprint:
1. Go to Render Dashboard
2. Click "New +" → "Blueprint"
3. Connect your repository
4. Render will auto-detect the `render.yaml` and set everything up

## Files Created for Deployment

- `requirements.txt` - Python dependencies
- `Procfile` - Tells Render how to run the app
- `runtime.txt` - Specifies Python version
- `render.yaml` - Optional blueprint configuration

## Important Notes

- **Free tier limitations**:
  - App goes to sleep after 15 minutes of inactivity
  - First request after sleep takes 30-60 seconds to wake up
  - Sufficient for personal projects and demos

- **Custom Domain** (optional):
  - You can add a custom domain in Render settings
  - Requires paid plan or can use free `.onrender.com` subdomain

## Local Development

To run locally:
```bash
cd version_site
python app.py
```

## Troubleshooting

If deployment fails:
1. Check Render logs in the dashboard
2. Ensure all files are committed and pushed to GitHub
3. Verify `version_site` is set as root directory
4. Check that Python version in `runtime.txt` is supported by Render
