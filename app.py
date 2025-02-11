import logging
import random
import string
from urllib.parse import urlparse
from flask import Flask, render_template, request, redirect, jsonify, url_for, abort

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

app = Flask(__name__)
app.secret_key = "url_shortener_secret_key"

# In-memory storage for URLs and analytics
url_database = {}
url_analytics = {}

def generate_short_code():
    """Generate a random 6-character string for short URLs."""
    characters = string.ascii_letters + string.digits
    while True:
        code = ''.join(random.choice(characters) for _ in range(6))
        if code not in url_database:
            return code

def is_valid_url(url):
    """Validate URL format."""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except ValueError:
        return False

@app.route('/')
def index():
    """Render the main page."""
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten_url():
    """Handle URL shortening requests."""
    long_url = request.form.get('url')
    
    if not long_url:
        return jsonify({'error': 'URL is required'}), 400
    
    if not is_valid_url(long_url):
        return jsonify({'error': 'Invalid URL format'}), 400

    # Check if URL already exists
    for short_code, url in url_database.items():
        if url == long_url:
            return jsonify({
                'short_url': url_for('redirect_url', short_code=short_code, _external=True),
                'visits': url_analytics.get(short_code, 0)
            })

    # Generate new short URL
    short_code = generate_short_code()
    url_database[short_code] = long_url
    url_analytics[short_code] = 0

    return jsonify({
        'short_url': url_for('redirect_url', short_code=short_code, _external=True),
        'visits': 0
    })

@app.route('/<short_code>')
def redirect_url(short_code):
    """Handle URL redirection."""
    if short_code not in url_database:
        abort(404)
    
    # Increment visit counter
    url_analytics[short_code] = url_analytics.get(short_code, 0) + 1
    
    return redirect(url_database[short_code])

@app.errorhandler(404)
def page_not_found(e):
    return render_template('index.html', error="Short URL not found"), 404
