# Environment Variables Setup

To use the Python backend version of the Bukhosi Caption Generator, you need to set up environment variables.

## Step 1: Create .env file

Create a file named `.env` in the project root directory.

## Step 2: Add Configuration

Copy and paste the following into your `.env` file, then replace the placeholder values:

```env
# Google Gemini API Key (Required)
# Get your key from: https://makersuite.google.com/app/apikey
GEMINI_API_KEY=your_gemini_api_key_here

# Instagram Credentials (Optional - for auto-posting)
# Only needed if you want to enable Instagram auto-posting feature
INSTAGRAM_USERNAME=bukhosi_royal_wines
INSTAGRAM_PASSWORD=your_instagram_password_here

# Flask Configuration (Optional)
FLASK_ENV=development
FLASK_DEBUG=True
```

## Step 3: Get Your Gemini API Key

1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the key
5. Paste it in your `.env` file after `GEMINI_API_KEY=`

## Step 4: Instagram Setup (Optional)

If you want to use Instagram auto-posting:

1. Add your Instagram username and password to the `.env` file
2. Note: Instagram may require 2FA - you may need to use an app-specific password
3. The system uses `instagrapi` library for Instagram integration

## Security Note

**Never commit your `.env` file to version control!** It contains sensitive credentials. The `.env` file should be in your `.gitignore`.

## Quick Start

After setting up your `.env` file:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python caption_generator_backend.py
```

Then open your browser to: http://localhost:5000
