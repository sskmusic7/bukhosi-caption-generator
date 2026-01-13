# GCP Cloud Storage Setup Guide

This guide will help you set up Google Cloud Storage (free tier) to automatically save Thandiwe's personality training progress.

## 📋 Prerequisites

- Google account
- 5 minutes to set up

## 🚀 Setup Steps

### Step 1: Create GCP Project (Free)

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/
   - Sign in with your Google account

2. **Create a New Project**
   - Click the project dropdown at the top
   - Click "New Project"
   - Project name: `bukhosi-caption-generator`
   - Click "Create"
   - Wait for project creation (30 seconds)

3. **Enable Free Tier**
   - GCP offers $300 free credit for new accounts
   - Cloud Storage free tier: 5 GB storage, 1 GB egress per month
   - This is MORE than enough for personality profiles

### Step 2: Create Storage Bucket

1. **Navigate to Cloud Storage**
   - In the left menu, go to "Cloud Storage" → "Buckets"
   - Or visit: https://console.cloud.google.com/storage/browser

2. **Create Bucket**
   - Click "Create Bucket"
   - Bucket name: `bukhosi-personality-profiles` (must be globally unique, add numbers if needed)
   - Location type: `Region`
   - Location: Choose closest to you (e.g., `us-central1`)
   - Storage class: `Standard`
   - Access control: `Uniform`
   - Click "Create"

### Step 3: Create Service Account

1. **Navigate to IAM & Admin**
   - Go to "IAM & Admin" → "Service Accounts"
   - Or visit: https://console.cloud.google.com/iam-admin/serviceaccounts

2. **Create Service Account**
   - Click "Create Service Account"
   - Service account name: `netlify-storage`
   - Service account ID: `netlify-storage` (auto-filled)
   - Description: `Netlify function for saving personality profiles`
   - Click "Create and Continue"

3. **Grant Permissions**
   - Role: `Storage Object Admin` (allows read/write to bucket)
   - Click "Continue"
   - Click "Done"

### Step 4: Create and Download Key

1. **Create Key**
   - Click on the service account you just created
   - Go to "Keys" tab
   - Click "Add Key" → "Create new key"
   - Key type: `JSON`
   - Click "Create"
   - JSON file will download automatically

2. **Save the JSON File**
   - Keep this file secure - it contains credentials
   - Don't commit it to git!
   - We'll add it to Netlify environment variables

### Step 5: Configure Netlify

1. **Add Environment Variables to Netlify**
   
   **Option A: Via Netlify CLI**
   ```bash
   # Get the bucket name from GCP
   netlify env:set GCP_BUCKET_NAME bukhosi-personality-profiles
   
   # Add credentials (copy the entire JSON file content)
   # Open the downloaded JSON file and copy ALL contents
   netlify env:set GCP_CREDENTIALS '{"type":"service_account","project_id":"..."}'
   ```

   **Option B: Via Netlify Dashboard (Recommended)**
   1. Go to: https://app.netlify.com/sites/bukhosi-caption-generator/configuration/env
   2. Click "Add a variable"
   3. Add `GCP_BUCKET_NAME` = `bukhosi-personality-profiles` (or your bucket name)
   4. Click "Add a variable" again
   5. Add `GCP_CREDENTIALS` = (paste entire JSON file content from Step 4)
   6. Save

2. **Install Dependencies**
   ```bash
   cd netlify/functions
   npm install
   ```

### Step 6: Test the Setup

1. **Redeploy to Netlify**
   ```bash
   netlify deploy --prod
   ```

2. **Test the Personality Trainer**
   - Go to the personality trainer page
   - Answer a question
   - Check browser console for "✅ Saved to cloud" message
   - Check GCP Storage bucket - you should see a file appear

## 🔒 Security Notes

- **Never commit the JSON credentials file to git**
- The `.gitignore` already excludes credential files
- Credentials are stored securely in Netlify environment variables
- Only the Netlify function can access GCP Storage

## 💰 Cost Estimate

**Free Tier Includes:**
- 5 GB storage (free)
- 1 GB egress per month (free)
- 5,000 Class A operations per month (free)
- 50,000 Class B operations per month (free)

**Estimated Usage:**
- Each personality profile: ~50 KB
- 100 profiles = 5 MB (well within free tier)
- You can store thousands of profiles for free!

**After Free Tier:**
- Storage: $0.020 per GB per month (very cheap)
- Operations: $0.05 per 10,000 operations

## 📁 File Structure in GCP

Files are saved as:
```
thandiwe_personality_training_2024-01-13.json
```

Each save creates/updates the file for that day.

## 🔍 Monitoring

1. **View Files in GCP Console**
   - Go to Cloud Storage → Buckets
   - Click your bucket name
   - See all saved files

2. **Check Netlify Function Logs**
   - Go to Netlify Dashboard → Functions
   - View logs for `save-personality-progress`

## 🆘 Troubleshooting

### "GCP credentials not configured"
- Check that `GCP_CREDENTIALS` is set in Netlify
- Make sure the JSON is valid (copy entire file content)

### "Bucket not found"
- Check that `GCP_BUCKET_NAME` matches your bucket name exactly
- Verify bucket exists in GCP Console

### "Permission denied"
- Check service account has `Storage Object Admin` role
- Verify the JSON credentials are for the correct service account

### Function fails silently
- Check Netlify function logs
- Check browser console for errors
- Local storage still works as backup

## ✅ Success Checklist

- [ ] GCP project created
- [ ] Storage bucket created
- [ ] Service account created with Storage Object Admin role
- [ ] JSON key downloaded
- [ ] Environment variables set in Netlify
- [ ] Dependencies installed (`npm install` in functions folder)
- [ ] Redeployed to Netlify
- [ ] Tested - file appears in GCP bucket

## 📞 Need Help?

If you encounter issues:
1. Check GCP Console for errors
2. Check Netlify function logs
3. Verify environment variables are set correctly
4. Ensure bucket name matches exactly

---

**Note:** Even if cloud save fails, local storage backup ensures no data is lost!
