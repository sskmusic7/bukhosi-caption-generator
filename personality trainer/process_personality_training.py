#!/usr/bin/env python3
"""
PERSONALITY TRAINING PROCESSOR
Takes Thandiwe's voice profile JSON and updates the caption generator system prompt

Usage:
    python process_personality_training.py thandiwe_voice_profile_2024-01-13.json
"""

import json
import sys
import re
from collections import Counter
from datetime import datetime

def load_voice_profile(filepath):
    """Load the voice profile JSON file"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"❌ Error: File not found: {filepath}")
        sys.exit(1)
    except json.JSONDecodeError:
        print(f"❌ Error: Invalid JSON file: {filepath}")
        sys.exit(1)


def analyze_vocabulary(answers):
    """Extract common words and phrases"""
    all_text = ' '.join([a['answer'] for a in answers if a['answer']]).lower()
    
    # Remove common words
    stop_words = {
        'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for',
        'of', 'with', 'by', 'from', 'is', 'are', 'was', 'were', 'be', 'been',
        'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
        'should', 'can', 'may', 'might', 'must', 'that', 'this', 'these', 'those',
        'i', 'you', 'he', 'she', 'it', 'we', 'they', 'my', 'your', 'his', 'her',
        'its', 'our', 'their', 'me', 'him', 'us', 'them'
    }
    
    words = re.findall(r'\b[a-z]{4,}\b', all_text)
    filtered_words = [w for w in words if w not in stop_words]
    
    word_freq = Counter(filtered_words)
    top_words = word_freq.most_common(20)
    
    return top_words


def analyze_phrases(answers):
    """Extract commonly used phrases"""
    all_text = ' '.join([a['answer'] for a in answers if a['answer']])
    
    # Look for 2-4 word phrases
    phrases = []
    sentences = re.split(r'[.!?]+', all_text)
    
    for sentence in sentences:
        words = sentence.lower().split()
        for i in range(len(words) - 1):
            phrase_2 = ' '.join(words[i:i+2])
            phrase_3 = ' '.join(words[i:i+3]) if i < len(words) - 2 else None
            
            if len(phrase_2) > 10:
                phrases.append(phrase_2)
            if phrase_3 and len(phrase_3) > 15:
                phrases.append(phrase_3)
    
    phrase_freq = Counter(phrases)
    return phrase_freq.most_common(15)


def analyze_sentence_structure(answers):
    """Analyze sentence length and structure"""
    sentences = []
    for a in answers:
        if a['answer']:
            sents = re.split(r'[.!?]+', a['answer'])
            sentences.extend([s.strip() for s in sents if s.strip()])
    
    lengths = [len(s.split()) for s in sentences]
    avg_length = sum(lengths) / len(lengths) if lengths else 0
    
    # Count questions vs statements
    questions = sum(1 for s in sentences if s.strip().endswith('?'))
    exclamations = sum(1 for s in sentences if s.strip().endswith('!'))
    
    return {
        'avg_sentence_length': round(avg_length, 1),
        'total_sentences': len(sentences),
        'question_ratio': round(questions / len(sentences) * 100, 1) if sentences else 0,
        'exclamation_ratio': round(exclamations / len(sentences) * 100, 1) if sentences else 0
    }


def analyze_cultural_references(answers):
    """Find references to heritage, culture, etc."""
    cultural_terms = {
        'heritage', 'zulu', 'royal', 'mother', 'princess', 'legacy', 
        'tradition', 'ancestors', 'family', 'generations', 'bukhosi',
        'isizulu', 'african', 'south african', 'cape winelands'
    }
    
    all_text = ' '.join([a['answer'] for a in answers if a['answer']]).lower()
    
    found_terms = {}
    for term in cultural_terms:
        count = len(re.findall(r'\b' + term + r'\b', all_text))
        if count > 0:
            found_terms[term] = count
    
    return dict(sorted(found_terms.items(), key=lambda x: x[1], reverse=True))


def analyze_emoji_usage(answers):
    """Extract emoji usage patterns"""
    all_text = ' '.join([a['answer'] for a in answers if a['answer']])
    
    # Simple emoji detection (could be improved)
    emoji_pattern = re.compile("["
        u"\U0001F600-\U0001F64F"  # emoticons
        u"\U0001F300-\U0001F5FF"  # symbols & pictographs
        u"\U0001F680-\U0001F6FF"  # transport & map symbols
        u"\U0001F700-\U0001F77F"  # alchemical symbols
        u"\U0001F780-\U0001F7FF"  # Geometric Shapes Extended
        u"\U0001F800-\U0001F8FF"  # Supplemental Arrows-C
        u"\U0001F900-\U0001F9FF"  # Supplemental Symbols and Pictographs
        u"\U0001FA00-\U0001FA6F"  # Chess Symbols
        u"\U0001FA70-\U0001FAFF"  # Symbols and Pictographs Extended-A
        u"\U00002702-\U000027B0"  # Dingbats
        u"\U000024C2-\U0001F251" 
        "]+", flags=re.UNICODE)
    
    emojis = emoji_pattern.findall(all_text)
    emoji_freq = Counter(emojis)
    
    return {
        'total_emojis': len(emojis),
        'unique_emojis': len(set(emojis)),
        'most_common': emoji_freq.most_common(5)
    }


def generate_updated_prompt(profile):
    """Generate an updated system prompt based on voice profile"""
    
    answers = profile['questions']
    
    # Run analyses
    vocab = analyze_vocabulary(answers)
    phrases = analyze_phrases(answers)
    structure = analyze_sentence_structure(answers)
    cultural = analyze_cultural_references(answers)
    emoji_data = analyze_emoji_usage(answers)
    
    # Build updated prompt
    prompt = f"""You are Thandiwe Ngubane-Zulu, co-owner of Bukhosi Royal Wines.

BRAND IDENTITY:
- South Africa's ONLY black-owned vineyard in Cape Winelands
- Founded 2008 by H.R.H. Princess Ntombifuthi Zulu (your mother) & you
- "Bukhosi" means "royalty" in isiZulu
- Tagline: "Heritage in Every Pour"
- Awards: Gold & Double Gold by Gilbert & Gaillard
- Old Vine Project certified (1976 & 1983 vintage bush vines)

YOUR AUTHENTIC VOICE (Based on Personality Training - {profile['timestamp'][:10]}):

VOCABULARY & PHRASES:
You frequently use these words: {', '.join([word for word, _ in vocab[:10]])}

Your signature phrases include:
{chr(10).join([f'- "{phrase}"' for phrase, _ in phrases[:5]])}

SENTENCE STRUCTURE:
- Average sentence length: {structure['avg_sentence_length']} words
- Question usage: {structure['question_ratio']}% ({"high - you engage with questions" if structure['question_ratio'] > 10 else "moderate - statements preferred"})
- Exclamation usage: {structure['exclamation_ratio']}% ({"enthusiastic" if structure['exclamation_ratio'] > 5 else "measured"})

CULTURAL REFERENCES:
You reference these heritage themes frequently:
{chr(10).join([f'- {term} ({count} times)' for term, count in list(cultural.items())[:5]])}

EMOJI USAGE:
- Total emojis in training: {emoji_data['total_emojis']}
- Usage frequency: {"High (3-5 per post)" if emoji_data['total_emojis'] > 50 else "Moderate (2-3 per post)" if emoji_data['total_emojis'] > 20 else "Minimal (0-2 per post)"}
- Most used: {', '.join([emoji for emoji, _ in emoji_data['most_common']])}

TONE CHARACTERISTICS:
- {profile['analysis']['tone']}
- {profile['analysis']['energy']} energy
- {profile['analysis']['perspective']}
- {profile['analysis']['style']}

CAPTION STRUCTURE (Your Approach):
1. HOOK (1-2 compelling lines)
2. CONTEXT (what's happening in the image)
3. CONNECTION (link to heritage/values/mission)
4. CTA (optional, natural invitation)

LENGTH: {structure['avg_sentence_length']} words per sentence average
Your style: {"Longer, storytelling captions" if structure['avg_sentence_length'] > 15 else "Concise, punchy captions"}

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

ANALYZE THE IMAGE AND WRITE AN AUTHENTIC INSTAGRAM CAPTION IN YOUR VOICE.
"""
    
    return prompt


def save_updated_prompt(prompt, output_file='updated_system_prompt.txt'):
    """Save the updated prompt to a file"""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(prompt)
    print(f"✅ Updated system prompt saved to: {output_file}")


def print_analysis_summary(profile):
    """Print a summary of the voice analysis"""
    print("\n" + "="*60)
    print("🎯 THANDIWE'S VOICE PROFILE ANALYSIS")
    print("="*60)
    
    answers = profile['questions']
    vocab = analyze_vocabulary(answers)
    phrases = analyze_phrases(answers)
    structure = analyze_sentence_structure(answers)
    cultural = analyze_cultural_references(answers)
    
    print(f"\n📊 STATISTICS:")
    print(f"  • Questions answered: {profile['stats']['answeredCount']}/70")
    print(f"  • Total words: {profile['stats']['totalWords']:,}")
    print(f"  • Average answer length: {profile['stats']['avgLength']} words")
    
    print(f"\n💬 VOICE CHARACTERISTICS:")
    print(f"  • Tone: {profile['analysis']['tone']}")
    print(f"  • Energy: {profile['analysis']['energy']}")
    print(f"  • Perspective: {profile['analysis']['perspective']}")
    print(f"  • Style: {profile['analysis']['style']}")
    
    print(f"\n📝 SENTENCE STRUCTURE:")
    print(f"  • Average length: {structure['avg_sentence_length']} words")
    print(f"  • Questions: {structure['question_ratio']}%")
    print(f"  • Exclamations: {structure['exclamation_ratio']}%")
    
    print(f"\n🎯 TOP 10 WORDS:")
    for word, count in vocab[:10]:
        print(f"  • {word} ({count} times)")
    
    print(f"\n💫 TOP 5 PHRASES:")
    for phrase, count in phrases[:5]:
        print(f"  • \"{phrase}\" ({count} times)")
    
    print(f"\n👑 CULTURAL REFERENCES:")
    for term, count in list(cultural.items())[:5]:
        print(f"  • {term} ({count} times)")
    
    print("\n" + "="*60)


def main():
    if len(sys.argv) < 2:
        print("Usage: python process_personality_training.py <voice_profile.json>")
        print("\nExample:")
        print("  python process_personality_training.py thandiwe_voice_profile_2024-01-13.json")
        sys.exit(1)
    
    filepath = sys.argv[1]
    
    print(f"\n🍷 Processing Thandiwe's Voice Profile...")
    print(f"📄 File: {filepath}")
    
    # Load profile
    profile = load_voice_profile(filepath)
    
    # Print analysis
    print_analysis_summary(profile)
    
    # Generate updated prompt
    print("\n✨ Generating updated system prompt...")
    updated_prompt = generate_updated_prompt(profile)
    
    # Save prompt
    save_updated_prompt(updated_prompt)
    
    print("\n🎉 COMPLETE!")
    print("\n📋 NEXT STEPS:")
    print("  1. Review 'updated_system_prompt.txt'")
    print("  2. Copy the prompt to your caption generator")
    print("  3. Test with sample images")
    print("  4. Compare old vs. new captions")
    print("  5. Get Thandiwe's feedback!")
    
    print("\n💡 TIP: The more detailed her answers, the better the voice capture!")
    print()


if __name__ == '__main__':
    main()
