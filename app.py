"""
Flask-based Interactive Dictionary Web Application.
Converts markdown to clickable words with AI-generated examples.
"""
import os
import json
import logging
from pathlib import Path
from typing import Dict, List

from flask import Flask, render_template, jsonify, request
from bs4 import BeautifulSoup
import markdown

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Production configuration
if os.getenv('FLASK_DEBUG', 'False').lower() != 'true':
    app.config['DEBUG'] = False

# Paths
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)
DATA_FILE = DATA_DIR / "translations.json"
CONTENT_FILE = Path(__file__).parent / "content.md"


def load_translations() -> Dict[str, any]:
    """Load translations from JSON file."""
    try:
        if DATA_FILE.exists():
            with open(DATA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
    except (json.JSONDecodeError, IOError) as e:
        logger.error(f"Error loading translations: {e}")
    return {}


def save_translation(word: str, result: Dict[str, any]) -> None:
    """Save translation result to JSON file."""
    try:
        translations = load_translations()
        translations[word] = result
        
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(translations, f, ensure_ascii=False, indent=2)
    except IOError as e:
        logger.error(f"Error saving translation: {e}")


def process_markdown() -> str:
    """
    Convert markdown content to HTML with clickable words.
    
    Returns:
        HTML string with wrapped words
    """
    try:
        if not CONTENT_FILE.exists():
            logger.warning(f"Content file not found: {CONTENT_FILE}")
            return "<p>No content file found. Please create content.md</p>"
        
        with open(CONTENT_FILE, 'r', encoding='utf-8') as f:
            md_content = f.read()
        
        # Convert markdown to HTML
        html = markdown.markdown(md_content, extensions=['extra'])
        
        # Parse with BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')
        
        # Get all text nodes and wrap words
        for element in soup.find_all(text=True):
            if element.parent.name not in ['script', 'style']:
                wrapped_text = wrap_words(element)
                if wrapped_text != str(element):
                    element.replace_with(BeautifulSoup(wrapped_text, 'html.parser'))
        
        return str(soup)
        
    except IOError as e:
        logger.error(f"Error processing markdown: {e}")
        return f"<p>Error loading content: {e}</p>"


def wrap_words(text: str) -> str:
    """
    Wrap each word in a span with class 'cw' (clickable word).
    
    Args:
        text: Input text to wrap
        
    Returns:
        HTML string with wrapped words
    """
    import re
    # Split by whitespace but preserve it
    parts = re.split(r'(\s+)', text)
    result = []
    
    for part in parts:
        if re.match(r'^\s+$', part):
            # Preserve whitespace
            result.append(part)
        elif part.strip():
            # Wrap word
            result.append(f'<span class="cw" data-word="{escape_html(part.strip())}">{escape_html(part)}</span>')
        else:
            result.append(part)
    
    return ''.join(result)


def escape_html(text: str) -> str:
    """Escape HTML special characters."""
    return (text.replace('&', '&amp;')
                .replace('<', '&lt;')
                .replace('>', '&gt;')
                .replace('"', '&quot;')
                .replace("'", '&#39;'))


@app.route('/')
def index():
    """Render the main page with processed content."""
    html_content = process_markdown()
    return render_template('template.html', content=html_content)


@app.route('/t/<word>')
def translate(word: str):
    """
    Get translation/examples for a word.
    Checks cache first, then calls API if needed.
    
    Args:
        word: The word or phrase to translate
        
    Returns:
        JSON response with examples or error
    """
    # Input validation
    if not word or len(word) > 100:
        return jsonify({'error': 'Invalid word'}), 400
    
    # Check cache first
    translations = load_translations()
    if word in translations:
        logger.info(f"Cache hit for word: {word}")
        return jsonify(translations[word])
    
    # Import here to avoid circular imports
    from ai_translator import AITranslator
    
    try:
        translator = AITranslator()
        result = translator.get_examples(word)
        
        # Save to cache if successful
        if 'error' not in result:
            save_translation(word, result)
        
        return jsonify(result)
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return jsonify({'error': 'API configuration error'}), 500
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


@app.route('/batch', methods=['POST'])
def batch_translate():
    """
    Translate multiple words in batch.
    
    Expects JSON body with 'words' array.
    """
    try:
        data = request.get_json()
        if not data or 'words' not in data:
            return jsonify({'error': 'Invalid request'}), 400
        
        words = data['words']
        if not isinstance(words, list) or len(words) > 50:
            return jsonify({'error': 'Invalid words array'}), 400
        
        translations = load_translations()
        results = {}
        
        # Import here
        from ai_translator import AITranslator
        
        translator = AITranslator()
        
        for word in words:
            if word in translations:
                results[word] = translations[word]
            else:
                result = translator.get_examples(word)
                if 'error' not in result:
                    save_translation(word, result)
                results[word] = result
        
        return jsonify(results)
        
    except Exception as e:
        logger.error(f"Batch translate error: {e}")
        return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8080))
    debug = os.getenv('FLASK_DEBUG', 'False').lower() == 'true'
    app.run(host='0.0.0.0', port=port, debug=debug)

