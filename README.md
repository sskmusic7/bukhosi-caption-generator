# BUKHOSI CAPTION GENERATOR
**AI-Powered Instagram Captions in Thandiwe's Authentic Voice**

Automatically generate on-brand, personality-driven Instagram captions for Bukhosi Royal Wines using Google Gemini Vision API.

---

## 🎯 Features

✅ **Image Analysis** - Google Gemini Vision understands context, wine bottles, vineyard scenes, people, etc.  
✅ **Brand Voice Embedded** - All brand guidelines, values, and messaging baked into the system  
✅ **Thandiwe's Personality** - Warm, proud, family-oriented, culturally rich voice  
✅ **Smart Hashtags** - Automatically selects 5-8 relevant hashtags  
✅ **Caption History** - SQLite database tracks all generated captions  
✅ **Edit & Refine** - Manual editing before posting  
✅ **Instagram Auto-Post** - Optional direct posting to @bukhosi_royal_wines  
✅ **Drag & Drop Interface** - Beautiful, easy-to-use web UI  

---

## 🏗️ Architecture

### Option 1: Simple HTML (No Server Required)
- **File:** `bukhosi_caption_generator.html`
- **Tech:** Pure HTML/JavaScript + Gemini API
- **Setup:** Just open in browser, add API key
- **Pros:** Zero installation, works offline (except API calls)
- **Cons:** No caption history persistence, no auto-posting

### Option 2: Python Backend (Full Features)
- **File:** `caption_generator_backend.py`
- **Tech:** Flask + Gemini API + SQLite + instagrapi
- **Setup:** Install dependencies, run server
- **Pros:** Caption history, database, Instagram posting, production-ready
- **Cons:** Requires Python environment

---

## 🚀 Quick Start

### Option 1: HTML Version (Easiest)

1. **Get Google Gemini API Key**
   ```
   Visit: https://makersuite.google.com/app/apikey
   Create new API key (free tier available)
   ```

2. **Open the HTML file**
   ```bash
   # Just double-click bukhosi_caption_generator.html
   # Or open in browser
   ```

3. **Configure API**
   - Paste your Gemini API key in the settings
   - Click "Save Configuration"

4. **Generate Captions**
   - Drag & drop an image
   - Click "Generate Caption"
   - Copy and use!

### Option 2: Python Backend (Full Features)

1. **Clone/Download Files**
   ```bash
   # Make sure you have these files:
   # - caption_generator_backend.py
   # - requirements.txt
   # - .env.example
   # - bukhosi_caption_generator.html
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure Environment**
   ```bash
   # Copy the example env file
   cp .env.example .env
   
   # Edit .env and add your keys:
   GEMINI_API_KEY=your_key_here
   INSTAGRAM_USERNAME=bukhosi_royal_wines  # optional
   INSTAGRAM_PASSWORD=your_password  # optional
   ```

4. **Run the Server**
   ```bash
   python caption_generator_backend.py
   ```

5. **Open in Browser**
   ```
   Navigate to: http://localhost:5000
   ```

---

## 📖 How It Works

### 1. Image Upload
User drags/drops or selects an image of:
- Wine bottles
- Vineyard scenes
- Harvest activities
- Tasting events
- Behind-the-scenes moments
- Awards/recognition
- Family/team photos

### 2. AI Analysis (Gemini Vision)
The system:
- Analyzes image content (wine type, setting, people, mood)
- Identifies relevant brand themes (heritage, quality, celebration, etc.)
- Determines appropriate tone (proud, educational, celebratory, etc.)

### 3. Caption Generation
Using embedded brand guidelines + Thandiwe's personality, generates:
- **Hook** - Attention-grabbing opening (1-2 lines)
- **Context** - What's happening in the image
- **Connection** - Link to brand values/mission
- **CTA** - Natural invitation (optional)
- **Hashtags** - 5-8 relevant tags
- **Emojis** - 2-3 max, purposeful

### 4. Human Review
Thandiwe can:
- Review the caption
- Edit any parts
- Regenerate if needed
- Copy to clipboard

### 5. Post (Optional)
- Manually paste into Instagram, OR
- Auto-post directly via Instagram API

---

## 🎨 Brand Voice System

The caption generator uses embedded guidelines covering:

### Brand Identity
- Only black-owned Cape Winelands vineyard
- Royal Zulu heritage (Princess Ntombifuthi & Thandiwe)
- "Bukhosi" = "royalty" in isiZulu
- 15+ years excellence (since 2008)
- Award-winning (Gold & Double Gold Gilbert & Gaillard)

### Voice Characteristics
- **Warm & Welcoming** (not cold or exclusive)
- **Proud but Humble** (celebrate without arrogance)
- **Educational** (share knowledge approachably)
- **Premium** (quality speaks for itself)
- **Culturally Rich** (natural Zulu heritage embrace)
- **Family-Focused** (mother-daughter business)

### Content Themes
1. Heritage & History (royal family, old vines, legacy)
2. Awards & Recognition (Gilbert & Gaillard, international praise)
3. Winemaking Process (harvest, cellar, craftsmanship)
4. Wine Portfolio (Bukhosi, Zulu Contessa, LeSizwe)
5. Experiences (tastings, pasta, tours)
6. Lifestyle (celebration, togetherness)
7. Behind the Scenes (team, vineyard life)

---

## 🧠 Thandiwe's Personality Training

For the most authentic voice, use the personality training system:

### Training Process

1. **Answer 70 Questions**
   - Background & identity (10 Q's)
   - Wine philosophy & craft (10 Q's)
   - Famous pasta & experiences (10 Q's)
   - Values & vision (10 Q's)
   - Social media style (10 Q's)
   - Rapid fire voice calibration (20 Q's)

2. **AI Analysis**
   - Vocabulary patterns
   - Sentence structure
   - Tone & energy
   - Storytelling style
   - Cultural identity
   - Humor & personality
   - Values emphasis

3. **Voice Profile Generation**
   - Creates custom personality model
   - Captures unique phrases
   - Identifies communication preferences
   - Builds authentic voice fingerprint

4. **Continuous Learning**
   - Tracks edits to generated captions
   - Learns from Thandiwe's modifications
   - Adapts to evolving style

### Running Personality Training

```bash
# Option A: Interactive Q&A
python personality_trainer.py --interactive

# Option B: Import from interview transcript
python personality_trainer.py --import interview.txt

# Option C: Learn from past Instagram posts
python personality_trainer.py --scrape @bukhosi_royal_wines
```

---

## 📸 Instagram Auto-Posting

### Setup (Optional)

1. **Install Instagram library**
   ```bash
   pip install instagrapi
   ```

2. **Add credentials to .env**
   ```env
   INSTAGRAM_USERNAME=bukhosi_royal_wines
   INSTAGRAM_PASSWORD=your_password
   ```

3. **Use the "Post to Instagram" button**
   - Reviews caption one last time
   - Uploads image + caption
   - Returns Instagram post URL

### Security Notes
- Instagram may require 2FA - handle in code
- Use app-specific passwords if enabled
- Consider Instagram Graph API for business accounts
- Rate limits apply (don't spam posts)

### Alternative: Manual Posting
If auto-posting seems risky:
1. Generate caption
2. Click "Copy Caption"
3. Open Instagram app
4. Paste caption manually
5. Add image and post

---

## 🗄️ Database Structure

### Caption History Table
```sql
CREATE TABLE captions (
    id INTEGER PRIMARY KEY,
    caption TEXT NOT NULL,
    image_path TEXT,
    image_analysis TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    posted_to_instagram BOOLEAN DEFAULT 0
);
```

### Query Examples
```python
# Get last 10 captions
SELECT * FROM captions ORDER BY timestamp DESC LIMIT 10;

# Get all unposted captions
SELECT * FROM captions WHERE posted_to_instagram = 0;

# Search captions by keyword
SELECT * FROM captions WHERE caption LIKE '%harvest%';
```

---

## 🎛️ Customization

### Adjusting Brand Voice

Edit `BRAND_VOICE_PROMPT` in `caption_generator_backend.py`:

```python
BRAND_VOICE_PROMPT = """
[Your custom instructions here]

KEY ADJUSTMENTS:
- Tone: [warmer, more formal, playful, etc.]
- Length: [shorter, longer]
- Hashtags: [more, fewer, different strategy]
- Emojis: [more, none, specific ones]
- Cultural: [more isiZulu, less, etc.]
"""
```

### Adding Custom Themes

```python
# In the prompt, add:
CONTENT THEMES:
- [Your new theme]: [description and examples]
```

### Personality Fine-Tuning

1. Collect Thandiwe's edits to captions
2. Analyze patterns in changes
3. Update system prompt to reflect preferences
4. Re-test and iterate

---

## 🔧 Troubleshooting

### "API Key Invalid"
- Double-check key from https://makersuite.google.com/app/apikey
- Ensure no extra spaces when copying
- Check if Gemini API is enabled for your account

### "Image Too Large"
- Maximum size: 16MB
- Compress image before uploading
- Use JPEG instead of PNG for photos

### "Caption Doesn't Sound Like Thandiwe"
- Run personality training module
- Provide sample Instagram posts for reference
- Adjust temperature setting (0.7-1.0 for more creativity)

### "Instagram Login Failed"
- Check username/password in .env
- Handle 2FA if enabled
- Use app-specific password
- Consider Instagram Graph API (more stable)

### "Caption History Not Saving"
- Check if `caption_history.db` file exists
- Ensure write permissions in directory
- Verify SQLite is installed (built into Python)

---

## 📊 Caption Quality Metrics

### Good Caption Indicators
✅ Hook grabs attention  
✅ Specific to image content  
✅ Connects to brand values  
✅ Authentic to Thandiwe's voice  
✅ Appropriate length (150-300 chars)  
✅ Natural hashtag integration  
✅ Emojis used sparingly  
✅ Includes relevant brand facts  

### Red Flags
❌ Generic wine clichés  
❌ Too salesy/pushy  
❌ Overly formal/stuffy  
❌ Too many emojis  
❌ Hashtag stuffing  
❌ Doesn't sound like Thandiwe  
❌ Missing brand differentiation  

---

## 🚀 Future Enhancements

### Phase 2
- [ ] Instagram Stories generation (vertical format)
- [ ] Video caption generation (Reels)
- [ ] Multi-image carousel captions
- [ ] A/B testing different caption styles
- [ ] Analytics tracking (which captions perform best)

### Phase 3
- [ ] WhatsApp integration (send to Thandiwe for approval)
- [ ] Scheduling system (queue posts in advance)
- [ ] Brand voice training from ALL past Instagram content
- [ ] Multi-language support (isiZulu, Afrikaans)
- [ ] Voice-to-caption (Thandiwe speaks, AI writes)

### Phase 4
- [ ] Facebook/LinkedIn auto-adapt
- [ ] Email newsletter generation
- [ ] Website blog post creation
- [ ] Press release writing
- [ ] Full content suite automation

---

## 📝 File Structure

```
bukhosi-caption-generator/
│
├── bukhosi_caption_generator.html      # Standalone web app
├── caption_generator_backend.py        # Python Flask server
├── requirements.txt                     # Python dependencies
├── .env.example                        # Environment variables template
├── .env                                # Your actual env vars (don't commit!)
│
├── uploads/                            # Uploaded images (auto-created)
├── caption_history.db                  # SQLite database (auto-created)
│
├── bukhosi_brand_voice_system.md       # Brand guidelines document
├── thandiwe_personality_training.md    # Personality training system
├── bukhosi_brand_analysis_COMPLETE.md  # Full brand research
│
└── README.md                           # This file
```

---

## 🤝 Usage Workflow

### Daily Use by Thandiwe

1. **Morning**: Take photos during vineyard activities
2. **Afternoon**: Upload images to caption generator
3. **Review**: Check AI-generated captions
4. **Edit**: Make any personal tweaks
5. **Post**: Either auto-post or copy to Instagram
6. **Track**: Review caption history and performance

### Batch Processing

For multiple images:
```python
# Process folder of images
python batch_generate.py --folder ./photos/harvest2024/
```

---

## 📞 Support & Contact

For issues, questions, or enhancements:
- **Big Mitch** (System Creator): [Your contact info]
- **System Status**: Check /api/health endpoint
- **Logs**: Available in Flask console output

---

## 📜 License & Usage

Built specifically for **Bukhosi Royal Wines**.  
Thandiwe's personality model is proprietary and trained on her unique voice.

---

## 🎉 Success Metrics

After implementing this system, expect:
- ⏱️ **Time Saved:** 15-20 mins per caption → 2 mins
- 📈 **Consistency:** Brand voice maintained across all posts
- ✨ **Quality:** Professional, on-brand captions every time
- 🎯 **Authenticity:** Sounds genuinely like Thandiwe
- 📊 **Frequency:** Easier to post consistently (3-5x/week)

---

**Built with 🍷 for Bukhosi Royal Wines**  
*Heritage in Every Pour • Heritage in Every Caption*
