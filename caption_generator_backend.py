"""
BUKHOSI CAPTION GENERATOR - PYTHON BACKEND
Thandiwe's Voice + Brand Guidelines + Auto Instagram Posting

Setup:
1. pip install -r requirements.txt
2. Create .env file with your API keys
3. Run: python caption_generator_backend.py
"""

import os
import base64
import json
import sqlite3
from datetime import datetime
from flask import Flask, request, jsonify, render_template, send_from_directory
from dotenv import load_dotenv
import google.generativeai as genai
from PIL import Image
import io

# Optional: Instagram posting
try:
    from instagrapi import Client as InstaClient
    INSTAGRAM_AVAILABLE = True
except ImportError:
    INSTAGRAM_AVAILABLE = False

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
app.config['UPLOAD_FOLDER'] = 'uploads'

# Create uploads folder if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Configure Gemini
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# Instagram credentials (optional)
INSTAGRAM_USERNAME = os.getenv('INSTAGRAM_USERNAME')
INSTAGRAM_PASSWORD = os.getenv('INSTAGRAM_PASSWORD')

# Brand Voice System Prompt
BRAND_VOICE_PROMPT = """You are Thandiwe Ngubane-Zulu, co-owner of Bukhosi Royal Wines.

BRAND IDENTITY:
- South Africa's ONLY black-owned vineyard in Cape Winelands
- Founded 2008 by H.R.H. Princess Ntombifuthi Zulu (your mother) & you
- "Bukhosi" means "royalty" in isiZulu
- Tagline: "Heritage in Every Pour"
- Awards: Gold & Double Gold by Gilbert & Gaillard
- Old Vine Project certified (1976 & 1983 vintage bush vines)

YOUR VOICE:
- Warm, welcoming, PROUD (not arrogant)
- Family-oriented ("we" language - mother-daughter business)
- Educational but approachable
- Premium without pretension
- Culturally rich (embrace Zulu heritage naturally)

CAPTION STRUCTURE:
1. HOOK (1-2 compelling lines that grab attention)
2. CONTEXT (what's happening in the image)
3. CONNECTION (link to heritage/values/mission)
4. CTA (optional, natural invitation)

CRITICAL - NEVER USE THESE AI-SOUNDING PHRASES:
- "It's not just..." / "This isn't just..."
- "It's more than..." / "This is more than..."
- "Beyond just..." / "More than just..."
- "Not only... but also..."
- Any variation of these clichéd patterns
Write naturally and directly. Be specific. Avoid meta-commentary about what things "are" or "aren't".

LENGTH: 150-300 characters typical, but no strict limit. Write naturally and fully.

EMOJIS: Sparingly (max 2-3): 🍷 👑 🏆 🌍 ✨ 🍇

HASHTAGS: 5-8 maximum
Branded: #BukhosiRoyalWines #HeritageInEveryPour
Wine: #SouthAfricanWine #CapeWinelands #Pinotage #CheninBlanc
Cultural: #ZuluHeritage #BlackOwnedBusiness #AfricanExcellence
Occasion: #WineLovers #WineTasting #Celebration

KEY FACTS (weave in when relevant):
- Only black-owned Cape Winelands vineyard
- 15+ years winemaking heritage
- Three ranges: Bukhosi (premium), Zulu Contessa (ultra-premium), LeSizwe (accessible)
- Thandiwesizwe's world-famous pasta (signature experience)
- Wine tastings: R195-R295
- Location: Cape Winelands, South Africa

CONTENT THEMES:
- Heritage & History (royal family, 15 years, old vines)
- Awards & Recognition (Gilbert & Gaillard, international praise)
- Winemaking Process (harvest, cellar, craftsmanship)
- Wine Portfolio (specific wines, tasting notes, pairings)
- Experiences (tastings, pasta, tours)
- Lifestyle & Celebration (people enjoying wine)
- Behind the Scenes (team, vineyard life, family)

ANALYZE THE IMAGE AND WRITE AN AUTHENTIC INSTAGRAM CAPTION IN YOUR VOICE."""


def init_db():
    """Initialize SQLite database for caption history"""
    conn = sqlite3.connect('caption_history.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS captions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            caption TEXT NOT NULL,
            image_path TEXT,
            image_analysis TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            posted_to_instagram BOOLEAN DEFAULT 0
        )
    ''')
    conn.commit()
    conn.close()


def save_caption_to_db(caption, image_path=None, image_analysis=None):
    """Save generated caption to database"""
    conn = sqlite3.connect('caption_history.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO captions (caption, image_path, image_analysis)
        VALUES (?, ?, ?)
    ''', (caption, image_path, image_analysis))
    conn.commit()
    caption_id = c.lastrowid
    conn.close()
    return caption_id


def get_caption_history(limit=10):
    """Retrieve caption history from database"""
    conn = sqlite3.connect('caption_history.db')
    c = conn.cursor()
    c.execute('''
        SELECT id, caption, image_path, image_analysis, timestamp, posted_to_instagram
        FROM captions
        ORDER BY timestamp DESC
        LIMIT ?
    ''', (limit,))
    results = c.fetchall()
    conn.close()
    
    return [{
        'id': row[0],
        'caption': row[1],
        'image_path': row[2],
        'image_analysis': row[3],
        'timestamp': row[4],
        'posted': row[5]
    } for row in results]


def analyze_image_with_gemini(image_path):
    """Analyze image using Google Gemini Vision"""
    try:
        # Load image
        img = Image.open(image_path)
        
        # Configure Gemini model
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Generate caption
        response = model.generate_content([
            BRAND_VOICE_PROMPT,
            img
        ], generation_config={
            'temperature': 0.9,
            'top_p': 0.95,
            'top_k': 40,
            'max_output_tokens': 4096,
        })
        
        caption = response.text
        
        # Extract image analysis (optional, for debugging/refinement)
        analysis_prompt = "Briefly describe what you see in this image (1-2 sentences):"
        analysis_response = model.generate_content([analysis_prompt, img])
        image_analysis = analysis_response.text
        
        return {
            'caption': caption,
            'image_analysis': image_analysis,
            'success': True
        }
        
    except Exception as e:
        return {
            'error': str(e),
            'success': False
        }


def post_to_instagram(image_path, caption):
    """Post to Instagram using instagrapi"""
    if not INSTAGRAM_AVAILABLE:
        return {'error': 'Instagram library not installed', 'success': False}
    
    if not INSTAGRAM_USERNAME or not INSTAGRAM_PASSWORD:
        return {'error': 'Instagram credentials not configured', 'success': False}
    
    try:
        # Initialize Instagram client
        cl = InstaClient()
        cl.login(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
        
        # Upload photo
        media = cl.photo_upload(image_path, caption)
        
        # Update database
        # (You'd need to pass caption_id here to mark as posted)
        
        return {
            'success': True,
            'media_id': media.id,
            'media_code': media.code,
            'url': f"https://instagram.com/p/{media.code}/"
        }
        
    except Exception as e:
        return {'error': str(e), 'success': False}


# Routes

@app.route('/')
def index():
    """Serve the main HTML interface"""
    return send_from_directory('.', 'bukhosi_caption_generator.html', mimetype='text/html')


@app.route('/api/generate-caption', methods=['POST'])
def generate_caption():
    """Generate caption from uploaded image"""
    
    # Check if API key is configured
    if not GEMINI_API_KEY:
        return jsonify({
            'error': 'Gemini API key not configured. Please set GEMINI_API_KEY in .env file',
            'success': False
        }), 500
    
    # Check if image was uploaded
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded', 'success': False}), 400
    
    file = request.files['image']
    
    if file.filename == '':
        return jsonify({'error': 'No image selected', 'success': False}), 400
    
    # Save uploaded image
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"{timestamp}_{file.filename}"
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(filepath)
    
    # Generate caption
    result = analyze_image_with_gemini(filepath)
    
    if result['success']:
        # Save to database
        caption_id = save_caption_to_db(
            caption=result['caption'],
            image_path=filepath,
            image_analysis=result.get('image_analysis')
        )
        
        return jsonify({
            'success': True,
            'caption': result['caption'],
            'image_analysis': result.get('image_analysis'),
            'caption_id': caption_id,
            'image_url': f"/uploads/{filename}"
        })
    else:
        return jsonify(result), 500


@app.route('/api/post-to-instagram', methods=['POST'])
def post_instagram():
    """Post caption + image to Instagram"""
    data = request.json
    
    if not data or 'caption' not in data or 'image_path' not in data:
        return jsonify({'error': 'Missing caption or image_path', 'success': False}), 400
    
    result = post_to_instagram(data['image_path'], data['caption'])
    
    if result['success']:
        return jsonify(result)
    else:
        return jsonify(result), 500


@app.route('/api/caption-history', methods=['GET'])
def caption_history():
    """Get caption history"""
    limit = request.args.get('limit', 10, type=int)
    history = get_caption_history(limit)
    return jsonify({'success': True, 'history': history})


@app.route('/api/save-config', methods=['POST'])
def save_config():
    """Save API configuration (in production, use secure storage)"""
    data = request.json
    
    # In production, save to secure location/database
    # For now, just validate
    if 'gemini_api_key' in data:
        return jsonify({'success': True, 'message': 'Configuration saved'})
    
    return jsonify({'error': 'Invalid configuration', 'success': False}), 400


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    """Serve uploaded images"""
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)


if __name__ == '__main__':
    # Initialize database
    init_db()
    
    print("""
    ╔════════════════════════════════════════════╗
    ║   BUKHOSI CAPTION GENERATOR - BACKEND     ║
    ║   Thandiwe's Voice + Brand Guidelines      ║
    ╚════════════════════════════════════════════╝
    
    Status:
    ✓ Flask server starting...
    ✓ Database initialized
    {} Gemini API configured
    {} Instagram posting available
    
    Access the app at: http://localhost:5000
    """.format(
        '✓' if GEMINI_API_KEY else '✗',
        '✓' if INSTAGRAM_AVAILABLE and INSTAGRAM_USERNAME else '✗'
    ))
    
    app.run(debug=True, host='0.0.0.0', port=5000)
