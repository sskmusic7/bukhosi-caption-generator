# Deployment Guide

## GitHub Deployment ✅ COMPLETED

Your code has been successfully pushed to GitHub:
**Repository:** https://github.com/sskmusic7/bukhosi-caption-generator

---

## Netlify Deployment

### Option 1: Deploy via Netlify CLI (Interactive)

Since Netlify CLI requires interactive setup, run these commands:

```bash
# 1. Initialize and create site (interactive)
netlify init

# When prompted:
# - Choose: "Create & configure a new project"
# - Site name: bukhosi-caption-generator (or leave blank for random name)
# - Build command: (leave blank - no build needed)
# - Publish directory: . (current directory)

# 2. Deploy to production
netlify deploy --prod
```

### Option 2: Deploy via Netlify Dashboard (Recommended)

1. **Go to Netlify Dashboard**
   - Visit: https://app.netlify.com
   - Sign in with your GitHub account

2. **Add New Site**
   - Click "Add new site" → "Import an existing project"
   - Choose "GitHub"
   - Authorize Netlify if prompted

3. **Select Repository**
   - Choose: `sskmusic7/bukhosi-caption-generator`
   - Click "Import"

4. **Configure Build Settings**
   - **Build command:** (leave blank - no build needed)
   - **Publish directory:** `.` (or leave as root)
   - Click "Deploy site"

5. **Site Settings** (Optional)
   - Go to Site settings → Domain management
   - Change site name if desired
   - Set up custom domain if needed

### Option 3: Quick Deploy (One Command - If Site Already Exists)

If you've already created the site via dashboard:

```bash
# Link to existing site
netlify link

# Deploy
netlify deploy --prod
```

---

## After Deployment

Once deployed, your site will be live at:
`https://[your-site-name].netlify.app`

The HTML file will be accessible at:
`https://[your-site-name].netlify.app/bukhosi_caption_generator.html`

### Important Notes:

1. **API Key**: Users will need to add their own Gemini API key in the app
2. **CORS**: The Gemini API should work from the deployed site
3. **Updates**: Future deployments can be done with:
   ```bash
   git push  # (if using GitHub integration)
   # OR
   netlify deploy --prod  # (if using CLI)
   ```

---

## Troubleshooting

### If deployment fails:
- Check that `netlify.toml` is in the root directory
- Ensure all files are committed to git
- Check Netlify build logs in the dashboard

### If the site loads but API doesn't work:
- Verify CORS settings (Gemini API should allow all origins)
- Check browser console for errors
- Ensure users add their API key in the settings

---

## Repository Links

- **GitHub:** https://github.com/sskmusic7/bukhosi-caption-generator
- **Netlify Dashboard:** https://app.netlify.com
