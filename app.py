import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import time
import requests
import httpx
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from flask import Flask, jsonify, render_template, request, g, session, redirect, url_for
import secrets
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import stripe
from flask_babel import Babel, _
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookRequestError
import google_ai
import json
import sqlite3

load_dotenv(dotenv_path=".env")

# --- Languages ---
LANGUAGES = {
    'en': 'English',
    'es': 'Español'
}

# --- Database Setup ---
db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    api_key = db.Column(db.String(120), unique=True, nullable=False)
    subscription_status = db.Column(db.String(20), default='inactive')
    subscription_plan = db.Column(db.String(20), default='free')
    stripe_customer_id = db.Column(db.String(120), unique=True, nullable=True)

    def __repr__(self):
        return f'<User {self.username}>'

class Project(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    image_url = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<Project {self.title}>'

class Payment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    currency = db.Column(db.String(10), nullable=False)
    status = db.Column(db.String(20), nullable=False, default='pending')
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    meta_payment_id = db.Column(db.String(120), unique=True, nullable=True)
    user = db.relationship('User', backref=db.backref('payments', lazy=True))
    def __repr__(self):
        return f'<Payment {self.id}>'

# --- Flask App Setup ---
app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.config['SECRET_KEY'] = secrets.token_hex(16)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///project.db'
app.config['LANGUAGES'] = LANGUAGES
app.config['BABEL_DEFAULT_LOCALE'] = 'en'
babel = Babel()
db.init_app(app)
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY")

# --- Meta/Facebook Business SDK Integration ---
def initialize_meta_sdk():
    """Initializes the Meta Business SDK."""
    meta_app_id = os.environ.get('META_APP_ID')
    meta_app_secret = os.environ.get('META_APP_SECRET')
    meta_access_token = os.environ.get('META_ACCESS_TOKEN')
    if all([meta_app_id, meta_app_secret, meta_access_token]):
        try:
            FacebookAdsApi.init(app_id=meta_app_id, app_secret=meta_app_secret, access_token=meta_access_token)
            print("Meta Business SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Meta Business SDK: {e}")
    else:
        print("Meta Business SDK credentials not found in environment variables. Skipping initialization.")

with app.app_context():
    initialize_meta_sdk()
    google_ai.init_vertexai()

def get_locale():
    if 'language' in session:
        return session['language']
    return request.accept_languages.best_match(app.config['LANGUAGES'].keys()) or app.config['BABEL_DEFAULT_LOCALE']

babel.init_app(app, locale_selector=get_locale)

@app.context_processor
def inject_conf_var():
    return dict(
        LANGUAGES=app.config['LANGUAGES'],
        get_locale=get_locale
    )

@app.route('/language/<language>')
def set_language(language=None):
    session['language'] = language
    return redirect(url_for('index'))

# --- Services ---
def get_weather(prompt):
    api_key = os.environ.get("WEATHER_API_KEY")
    if not api_key:
        return _("Error: WEATHER_API_KEY environment variable not set.")
    location = prompt.strip()
    if not location:
        return _("Please provide a location.")
    try:
        url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={location}"
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        if "error" in data:
            return _("Error: %(message)s", message=data['error']['message'])
        location_data = data.get('location', {})
        current_data = data.get('current', {})
        city = location_data.get('name')
        region = location_data.get('region')
        country = location_data.get('country')
        temp_c = current_data.get('temp_c')
        temp_f = current_data.get('temp_f')
        condition = current_data.get('condition', {}).get('text')
        wind_mph = current_data.get('wind_mph')
        humidity = current_data.get('humidity')
        message = (
            _("Weather in %(city)s, %(region)s, %(country)s:\n", city=city, region=region, country=country) +
            _("Temperature: %(temp_c)s°C / %(temp_f)s°F\n", temp_c=temp_c, temp_f=temp_f) +
            _("Condition: %(condition)s\n", condition=condition) +
            _("Wind: %(wind_mph)s mph\n", wind_mph=wind_mph) +
            _("Humidity: %(humidity)s%%", humidity=humidity)
        )
        return message
    except requests.RequestException as e:
        return _("Error fetching weather data: %(error)s", error=e)
    except Exception as e:
        return _("An unexpected error occurred: %(error)s", error=e)

def generate_game(prompt):
    name = _("Guess the Number")
    description = _("A simple number guessing game.")
    for line in prompt.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            if key.strip().lower() == 'name':
                name = value.strip()
            elif key.strip().lower() == 'description':
                description = value.strip()

    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{name}</h1>
    <p>{description}</p>
    <p>{_("I'm thinking of a number between 1 and 100.")}</p>
    <input type="number" id="guess-input" min="1" max="100">
    <button id="guess-btn">{_("Guess")}</button>
    <p id="message"></p>
    <script src="script.js"></script>
</body>
</html>
    """
    css_content = """
body { font-family: sans-serif; text-align: center; margin-top: 50px; }
h1 { color: #333; }
input { padding: 5px; }
button { padding: 5px 10px; }
#message { margin-top: 20px; font-weight: bold; }
    """
    js_content = f"""
document.addEventListener('DOMContentLoaded', () => {{
    const guessInput = document.getElementById('guess-input');
    const guessBtn = document.getElementById('guess-btn');
    const message = document.getElementById('message');
    let randomNumber = Math.floor(Math.random() * 100) + 1;
    let attempts = 0;
    guessBtn.addEventListener('click', () => {{
        const userGuess = parseInt(guessInput.value);
        attempts++;
        if (isNaN(userGuess) || userGuess < 1 || userGuess > 100) {{
            message.textContent = '{_("Please enter a valid number between 1 and 100.")}';
            return;
        }}
        if (userGuess === randomNumber) {{
            message.textContent = '{_("Congratulations! You guessed the number in %(attempts)s attempts.", attempts="{attempts}")}';
            message.style.color = 'green';
            guessBtn.disabled = true;
        }} else if (userGuess < randomNumber) {{
            message.textContent = '{_("Too low! Try again.")}';
            message.style.color = 'red';
        }} else {{
            message.textContent = '{_("Too high! Try again.")}';
            message.style.color = 'red';
        }}
    }});
}});
"""
    response_message = f"""
{_("Here is the generated code for your game.")}
**index.html:**
```html
{html_content.strip()}
```
**style.css:**
```css
{css_content.strip()}
```
**script.js:**
```javascript
{js_content.strip()}
```
"""
    return response_message.strip()

def generate_app(prompt):
    name = _("To-Do App")
    description = _("A simple to-do list application.")
    for line in prompt.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            if key.strip().lower() == 'name':
                name = value.strip()
            elif key.strip().lower() == 'description':
                description = value.strip()
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <h1>{name}</h1>
    <p>{description}</p>
    <input type="text" id="task-input" placeholder="{_("Add a new task...")}">
    <button id="add-task-btn">{_("Add Task")}</button>
    <ul id="task-list"></ul>
    <script src="script.js"></script>
</body>
</html>
    """
    css_content = """
body { font-family: sans-serif; margin: 2rem; }
h1 { color: #333; }
input { padding: 10px; width: 300px; }
button { padding: 10px 15px; }
ul { list-style-type: none; padding: 0; }
li { padding: 10px; border-bottom: 1px solid #ccc; display: flex; justify-content: space-between; align-items: center; }
li button { background: #ff4d4d; color: white; border: none; padding: 5px 10px; cursor: pointer; }
    """
    js_content = f"""
document.addEventListener('DOMContentLoaded', () => {{
    const taskInput = document.getElementById('task-input');
    const addTaskBtn = document.getElementById('add-task-btn');
    const taskList = document.getElementById('task-list');
    addTaskBtn.addEventListener('click', () => {{
        const taskText = taskInput.value.trim();
        if (taskText !== '') {{
            addTask(taskText);
            taskInput.value = '';
        }}
    }});
    function addTask(taskText) {{
        const li = document.createElement('li');
        li.textContent = taskText;
        const deleteBtn = document.createElement('button');
        deleteBtn.textContent = '{_("Delete")}';
        deleteBtn.addEventListener('click', () => {{
            li.remove();
        }});
        li.appendChild(deleteBtn);
        taskList.appendChild(li);
    }}
}});
"""
    response_message = f"""
{_("Here is the generated code for your app.")}
**index.html:**
```html
{html_content.strip()}
```
**style.css:**
```css
{css_content.strip()}
```
**script.js:**
```javascript
{js_content.strip()}
```
"""
    return response_message.strip()

def generate_website(prompt):
    import datetime
    structure = {'sections': []}
    current_section = None
    errors = []
    for i, line in enumerate(prompt.splitlines()):
        if not line.strip():
            continue
        indentation = len(line) - len(line.lstrip(' '))
        try:
            key, value = line.strip().split(':', 1)
            key = key.strip().lower()
            value = value.strip()
        except ValueError:
            return _("Error on line %(line_number)s: Invalid format. Each line must be in 'key: value' format.", line_number=i+1)

        if indentation == 0:
            if key == 'section':
                current_section = {'title': value, 'content': {}}
                structure['sections'].append(current_section)
            else:
                structure[key] = value
                current_section = None
        elif indentation > 0 and current_section:
            current_section['content'][key] = value
        else:
            return _("Error on line %(line_number)s: Indentation error or item outside of a section.", line_number=i+1)

    title = structure.get('title', _('My Website'))
    header_content = structure.get('header', '')
    footer_content = structure.get('footer', '')
    main_content = ""
    for section in structure['sections']:
        main_content += f"    <section>\n"
        main_content += f"      <h2>{section.get('title', '')}</h2>\n"
        if 'text' in section['content']:
            main_content += f"      <p>{section['content']['text']}</p>\n"
        if 'images' in section['content']:
            try:
                num_images = int(section['content']['images'])
                if not (0 <= num_images <= 10):
                    return _("Error: Number of images must be between 0 and 10.")
                for i in range(num_images):
                    main_content += f"      <img src='https://via.placeholder.com/150' alt='{_("placeholder image %(number)s", number=i+1)}'>\n"
            except ValueError:
                return _("Error: Invalid number for images. Please use an integer.")
        main_content += f"    </section>\n"
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{title}</title>
    <link rel="stylesheet" href="style.css">
</head>
<body>
    <header>
        <h1>{header_content}</h1>
    </header>
    <main>
{main_content}
    </main>
    <footer>
        <p>{footer_content}</p>
    </footer>
</body>
</html>
    """
    css_content = """
body { font-family: sans-serif; line-height: 1.6; margin: 0; padding: 0; background: #f4f4f4; color: #333; }
.container { max-width: 960px; margin: auto; overflow: auto; padding: 0 2rem; }
header { background: #333; color: #fff; padding: 1rem 0; text-align: center; }
main { padding: 1rem; background: #fff; }
section { margin-bottom: 1.5rem; }
h2 { color: #333; }
img { max-width: 100%; height: auto; margin: 0.5rem; }
footer { text-align: center; padding: 1rem 0; background: #333; color: #fff; margin-top: 1rem; }
    """
    response_message = f"""
{_("Here is the generated code for your website.")}
**index.html:**
```html
{html_content.strip()}
```
**style.css:**
```css
{css_content.strip()}
```
"""
    return response_message.strip()

def generate_backend(prompt):
    route = "/api/data"
    message = "Hello from your new backend!"
    for line in prompt.splitlines():
        if ':' in line:
            key, value = line.split(':', 1)
            if key.strip().lower() == 'route':
                route = value.strip()
            elif key.strip().lower() == 'message':
                message = value.strip()

    backend_code = f"""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route('{route}', methods=['GET'])
def get_data():
    return jsonify({{'message': '{message}'}})

if __name__ == '__main__':
    app.run(debug=True, port=5001)
"""
    response_message = f"""
{_("Here is the generated code for your Python backend.")}
**backend.py:**
```python
{backend_code.strip()}
```
"""
    return response_message.strip()

def generate_art_criticism(prompt):
    criticism = _("This is a placeholder for an art criticism based on your prompt: %(prompt)s", prompt=prompt)
    # In a real application, this would connect to a generative AI model
    # to produce a more meaningful and context-aware art criticism.
    return criticism

def generate_automation_script(prompt):
    script = f"""#!/bin/bash
# Automation script generated by AI

# Task: {prompt}

echo "Starting automation for: {prompt}"

# Add your automation commands here

echo "Automation finished."
"""
    response_message = f"""
{_("Here is the generated automation script for your task.")}
**automation.sh:**
```bash
{script.strip()}
```
"""
    return response_message.strip()

def debug_code(prompt):
    if prompt.strip().startswith('http'):
        code = fetch_github_file(prompt)
        if code.startswith('Error:'):
            return code
    else:
        code = prompt
    errors = []
    if code.strip().startswith('<'):
        lang = 'HTML'
        if not code.lower().strip().startswith('<!doctype html>'):
            errors.append(_("Missing <!DOCTYPE html> declaration at the beginning."))
        if code.lower().count('<html') != code.lower().count('</html>'):
            errors.append(_("Mismatched <html> tags."))
        if code.lower().count('<head') != code.lower().count('</head>'):
            errors.append(_("Mismatched <head> tags."))
        if code.lower().count('<body') != code.lower().count('</body>'):
            errors.append(_("Mismatched <body> tags."))
    else:
        lang = 'CSS'
        if code.count('{') != code.count('}'):
            errors.append(_("Mismatched curly braces {}."))
        lines = code.split('\\n')
        in_block = False
        for i, line in enumerate(lines):
            line = line.strip()
            if '{' in line:
                in_block = True
            if '}' in line:
                in_block = False
            if in_block and line and not line.endswith('{') and not line.endswith('}') and not line.endswith(';'):
                 errors.append(_("Line %(line_number)s: Missing semicolon ';'.", line_number=i+1))
    if not errors:
        return _("No obvious issues found in your %(lang)s code.", lang=lang)
    else:
        return _("Found potential issues in your %(lang)s code:\n", lang=lang) + "\\n".join(f"- {error}" for error in errors)

def generate_social_media_post(prompt):
    post = f"""
🚀 Big News! 🚀
{_("We're excited to announce %(prompt)s!", prompt=prompt)}
{_("Come and check us out! You won't be disappointed.")}
#NewBusiness #GrandOpening #{prompt.replace(" ", "").split(',')[0]} #SupportLocal
    """
    return post.strip()

def optimize_ads(prompt):
    # Basic keyword extraction and ad copy generation
    keywords = [word for word in prompt.split() if len(word) > 4]
    ad_copy = f"Optimized ad for: {prompt}. Try focusing on keywords like {', '.join(keywords[:3])}."
    return {
        "ad_copy": ad_copy,
        "keywords": keywords,
        "recommendations": [
            "Use high-quality images.",
            "A/B test your ad copy.",
            "Target a specific audience."
        ]
    }

async def check_link(client, link_data, results, headers):
    full_url = link_data['url']
    anchor_text = link_data['text']
    try:
        start_time = time.time()
        response = await client.head(full_url, headers=headers, timeout=5)
        end_time = time.time()
        response_time = round((end_time - start_time) * 1000)
        status_code = response.status_code
        link_result = {
            'url': full_url,
            'text': anchor_text,
            'status': status_code,
            'time_ms': response_time
        }
        if status_code >= 400:
            results['broken'].append(link_result)
        elif response_time > 1000:
            results['slow'].append(link_result)
        else:
            results['ok'].append(link_result)
    except httpx.RequestError as e:
        results['broken'].append({
            'url': full_url,
            'text': anchor_text,
            'status': 'Error',
            'error': str(e)
        })

async def analyze_website(url):
    try:
        headers = {'User-Agent': 'AI-Agent-Checker/1.0'}
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=headers, timeout=10)
            response.raise_for_status()
    except httpx.RequestError as e:
        return {'error': _("Error fetching URL: %(error)s", error=e)}

    soup = BeautifulSoup(response.content, 'lxml')
    links_to_check = []
    for a_tag in soup.find_all('a', href=True):
        href = a_tag.get('href')
        full_url = urljoin(url, href)
        if urlparse(full_url).scheme in ['http', 'https']:
            links_to_check.append({
                'url': full_url,
                'text': a_tag.get_text(strip=True)
            })

    results = {'ok': [], 'broken': [], 'slow': []}
    async with httpx.AsyncClient() as client:
        tasks = [check_link(client, link_data, results, headers) for link_data in links_to_check]
        await asyncio.gather(*tasks)

    return results

def fetch_github_file(url):
    try:
        parsed_url = urlparse(url)
        if parsed_url.hostname != 'github.com':
            return _("Error: Not a valid GitHub URL.")
        path_parts = parsed_url.path.strip('/').split('/')
        if len(path_parts) < 4 or path_parts[2] != 'blob':
            return _("Error: URL does not appear to be a valid GitHub file URL (e.g., .../user/repo/blob/branch/file).")
        user, repo, _, branch = path_parts[:4]
        file_path = '/'.join(path_parts[4:])
        raw_url = f"https.raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"
        headers = {'User-Agent': 'AI-Agent-Checker/1.0'}
        response = requests.get(raw_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return _("Error fetching file from GitHub: %(error)s", error=e)
    except Exception as e:
        return _("An unexpected error occurred: %(error)s", error=e)

# --- API Endpoints ---
def require_api_key(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key:
            return jsonify({"error": _("API key is missing")}), 401
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            return jsonify({"error": _("Invalid API key")}), 401
        g.user = user
        return await f(*args, **kwargs) if asyncio.iscoroutinefunction(f) else f(*args, **kwargs)
    return decorated_function

@app.route('/api/config')
def get_config():
    return jsonify({
        'stripePublicKey': os.environ.get('STRIPE_PUBLIC_KEY'),
        'metaAppId': os.environ.get('META_APP_ID')
    })

@app.route('/promotion')
def promotion():
    return render_template('promotion.html')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/v1/develop/website', methods=['POST'])
@require_api_key
def develop_website_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    html, css = google_ai.generate_website(prompt)
    message = f"""
{_("Here is the generated code for your website.")}
**index.html:**
```html
{html.strip()}
```
**style.css:**
```css
{css.strip()}
```
"""
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/develop/game', methods=['POST'])
@require_api_key
def develop_game_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = generate_game(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/develop/app', methods=['POST'])
@require_api_key
def develop_app_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = generate_app(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/develop/backend', methods=['POST'])
@require_api_key
def develop_backend_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = generate_backend(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/debug', methods=['POST'])
@require_api_key
def debug_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    # Simple language detection
    language = 'html'
    if prompt.strip().startswith('{') or '{' in prompt and '}' in prompt:
        language = 'css'

    errors = google_ai.debug_code(prompt, language)
    if not errors:
        message = _("No obvious issues found in your %(lang)s code.", lang=language)
    else:
        message = _("Found potential issues in your %(lang)s code:\n", lang=language) + "\n".join(f"- {error}" for error in errors)

    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/market/post', methods=['POST'])
@require_api_key
def market_post_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.generate_social_media_post(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/optimize/ads', methods=['POST'])
@require_api_key
def optimize_ads_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = optimize_ads(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/analyze/website', methods=['POST'])
@require_api_key
async def analyze_website_endpoint():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": _("URL is required")}), 400
    message = await analyze_website(url)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/weather', methods=['POST'])
@require_api_key
def weather_endpoint():
    data = request.get_json()
    location = data.get('location')
    if not location:
        return jsonify({"error": _("Location is required")}), 400
    message = get_weather(location)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/finance/advice', methods=['POST'])
@require_api_key
def financial_advice_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_financial_advice(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/art/criticism', methods=['POST'])
@require_api_key
def art_criticism_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = generate_art_criticism(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/automate/script', methods=['POST'])
@require_api_key
def automate_script_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = generate_automation_script(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/business/strategy', methods=['POST'])
@require_api_key
def business_strategy_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.generate_business_strategy(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/business/monetization', methods=['POST'])
@require_api_key
def business_monetization_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_monetization_advice(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/business/partnership', methods=['POST'])
@require_api_key
def business_partnership_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_partnership_advice(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/business/fundraising', methods=['POST'])
@require_api_key
def business_fundraising_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_fundraising_advice(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/support/it', methods=['POST'])
@require_api_key
def it_support_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_it_support(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/support/telecommunication', methods=['POST'])
@require_api_key
def telecommunication_support_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_telecommunication_support(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/assistant/telecommunication', methods=['POST'])
@require_api_key
def telecommunication_assistant_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.generate_telecommunication_assistant_response(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/data/analyze', methods=['POST'])
@require_api_key
def analyze_data_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.analyze_data(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/develop/blockchain', methods=['POST'])
@require_api_key
def blockchain_code_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.generate_blockchain_code(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/develop/blogger', methods=['POST'])
@require_api_key
def blogger_bots_page_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.generate_blogger_bots_page(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/develop/messenger', methods=['POST'])
@require_api_key
def messenger_code_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.generate_messenger_code(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/learn/language', methods=['POST'])
@require_api_key
def learn_language_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.learn_language(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/sciences/educator', methods=['POST'])
@require_api_key
def sciences_educator_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_science_education(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/assistance/transaction', methods=['POST'])
@require_api_key
def transaction_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_transaction_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/play/music', methods=['POST'])
@require_api_key
def play_music_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.play_music_instrumental(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/assistance/geometry', methods=['POST'])
@require_api_key
def geometry_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_geometry_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/assistance/cartography', methods=['POST'])
@require_api_key
def cartography_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_cartography_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/assistance/document', methods=['POST'])
@require_api_key
def document_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_document_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/business/plan', methods=['POST'])
@require_api_key
def business_plan_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_business_plan_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/investigation/security', methods=['POST'])
@require_api_key
def investigation_security_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_investigation_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/military/assistance', methods=['POST'])
@require_api_key
def military_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_military_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/gendarmerie/assistance', methods=['POST'])
@require_api_key
def gendarmerie_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_gendarmerie_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/police/assistance', methods=['POST'])
@require_api_key
def police_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_police_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/security/optimization', methods=['POST'])
@require_api_key
def security_optimization_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_security_optimization_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/podcast/assistance', methods=['POST'])
@require_api_key
def podcast_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_podcast_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/supply-chain/assistance', methods=['POST'])
@require_api_key
def supply_chain_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_supply_chain_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/logistics/assistance', methods=['POST'])
@require_api_key
def logistics_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_logistics_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/data-engineering/assistance', methods=['POST'])
@require_api_key
def data_engineering_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_data_engineering_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/incoterms/assistance', methods=['POST'])
@require_api_key
def incoterms_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_incoterms_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/ecommerce/assistance', methods=['POST'])
@require_api_key
def ecommerce_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_ecommerce_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/government/assistance', methods=['POST'])
@require_api_key
def government_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_government_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/togo/assistance', methods=['POST'])
@require_api_key
def togo_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_togo_public_service_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/government/policy', methods=['POST'])
@require_api_key
def public_policy_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_public_policy_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/government/engagement', methods=['POST'])
@require_api_key
def citizen_engagement_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_citizen_engagement_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/government/smart-city', methods=['POST'])
@require_api_key
def smart_city_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_smart_city_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/government/bias-detection', methods=['POST'])
@require_api_key
def government_bias_detection_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_bias_detection_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/biotech/assistance', methods=['POST'])
@require_api_key
def biotech_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_biotech_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/legal/assistance', methods=['POST'])
@require_api_key
def legal_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_legal_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/fintech/assistance', methods=['POST'])
@require_api_key
def fintech_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_fintech_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/music/production', methods=['POST'])
@require_api_key
def music_production_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_music_production_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/aerospace-automotive/assistance', methods=['POST'])
@require_api_key
def aerospace_automotive_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_aerospace_automotive_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/data-science-stewardship/assistance', methods=['POST'])
@require_api_key
def data_science_stewardship_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_data_science_stewardship_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/logo-thumbnail/assistance', methods=['POST'])
@require_api_key
def logo_thumbnail_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_logo_thumbnail_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/fake-content/verification', methods=['POST'])
@require_api_key
def fake_content_verification_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_fake_content_verification_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/automatic-learning/assistance', methods=['POST'])
@require_api_key
def automatic_learning_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_automatic_learning_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/ia-data-engineering/assistance', methods=['POST'])
@require_api_key
def ia_data_engineering_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_ia_data_engineering_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/data-lab-center/assistance', methods=['POST'])
@require_api_key
def data_lab_center_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_data_lab_center_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/computer-vision/assistance', methods=['POST'])
@require_api_key
def computer_vision_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_computer_vision_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/ia-researcher/assistance', methods=['POST'])
@require_api_key
def ia_researcher_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_ia_researcher_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/esports/assistance', methods=['POST'])
@require_api_key
def esports_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_esports_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/dermatology/assistance', methods=['POST'])
@require_api_key
def dermatology_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_dermatology_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/microsoft-ignite/assistance', methods=['POST'])
@require_api_key
def microsoft_ignite_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_microsoft_ignite_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/diagnostic/assistance', methods=['POST'])
@require_api_key
def diagnostic_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_diagnostic_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/eshop/assistance', methods=['POST'])
@require_api_key
def eshop_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_eshop_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/it-operations/assistance', methods=['POST'])
@require_api_key
def it_operations_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_it_operations_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/maintenance/assistance', methods=['POST'])
@require_api_key
def maintenance_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_maintenance_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/google-sites/assistance', methods=['POST'])
@require_api_key
def google_sites_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_google_sites_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/marketing/assistance', methods=['POST'])
@require_api_key
def marketing_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_marketing_bot_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/digital-repair/assistance', methods=['POST'])
@require_api_key
def digital_repair_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_digital_repair_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/investment-trading/assistance', methods=['POST'])
@require_api_key
def investment_trading_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_investment_trading_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/autogpt/assistance', methods=['POST'])
@require_api_key
def autogpt_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_autogpt_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/conflict-debug/assistance', methods=['POST'])
@require_api_key
def conflict_debug_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    media_data = data.get('media_data')
    mime_type = data.get('mime_type')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_conflict_debug_assistance(prompt, media_data, mime_type)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/visual/analysis', methods=['POST'])
@require_api_key
def visual_analysis_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    media_data = data.get('media_data')
    mime_type = data.get('mime_type')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_visual_intelligence(prompt, media_data, mime_type)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/generic/assistance', methods=['POST'])
@require_api_key
def generic_assistance_endpoint():
    data = request.get_json()
    system_message = data.get('system_message')
    prompt = data.get('prompt')
    media_data = data.get('media_data')
    mime_type = data.get('mime_type')
    if not all([system_message, prompt]):
        return jsonify({"error": _("system_message and prompt are required")}), 400
    message = google_ai.generic_ai_service(system_message, prompt, media_data, mime_type)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/automl/feature-engineering', methods=['POST'])
@require_api_key
def automl_feature_engineering_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_feature_engineering_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/automl/hyperparameter-tuning', methods=['POST'])
@require_api_key
def automl_hyperparameter_tuning_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_hyperparameter_tuning_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/automl/model-selection', methods=['POST'])
@require_api_key
def automl_model_selection_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_model_selection_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/automl/mlops', methods=['POST'])
@require_api_key
def automl_mlops_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_mlops_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/cloud-infrastructure/assistance', methods=['POST'])
@require_api_key
def cloud_infrastructure_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_cloud_infrastructure_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/iaas/assistance', methods=['POST'])
@require_api_key
def iaas_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_iaas_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/paas/assistance', methods=['POST'])
@require_api_key
def paas_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_paas_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/saas/assistance', methods=['POST'])
@require_api_key
def saas_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_saas_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/itaas/assistance', methods=['POST'])
@require_api_key
def itaas_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_itaas_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/malware-defense/assistance', methods=['POST'])
@require_api_key
def malware_defense_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_malware_defense_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/ussd-blockchain/assistance', methods=['POST'])
@require_api_key
def ussd_blockchain_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_ussd_blockchain_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/domain-codex/assistance', methods=['POST'])
@require_api_key
def domain_codex_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_domain_codex_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/llama/intelligence', methods=['POST'])
@require_api_key
def llama_intelligence_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_llama_intelligence(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/llama/guard', methods=['POST'])
@require_api_key
def llama_guard_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_llama_guard_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/nvidia/nemotron', methods=['POST'])
@require_api_key
def nvidia_nemotron_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_nemotron_reasoning(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/nvidia/mixtral', methods=['POST'])
@require_api_key
def nvidia_mixtral_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_mixtral_multilingual_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/anthropic/intelligence', methods=['POST'])
@require_api_key
def anthropic_intelligence_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_claude_intelligence(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/anthropic/coding', methods=['POST'])
@require_api_key
def anthropic_coding_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_claude_coding_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/langflow/execute', methods=['POST'])
@require_api_key
def execute_langflow_endpoint():
    data = request.get_json()
    flow_name = data.get('flow_name', 'sample_flow')
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    # In a real scenario, we would use langflow's run_flow or similar
    # For this task, we'll simulate the execution or load the flow config
    try:
        flow_path = os.path.join('langflow_flows', f'{flow_name}.json')
        if not os.path.exists(flow_path):
            return jsonify({"error": _("Flow not found")}), 404

        with open(flow_path, 'r') as f:
            flow_config = json.load(f)

        # Simulate execution using LangChain (as Langflow is built on LangChain)
        message = google_ai.generic_ai_service(f"Executing Langflow: {flow_config.get('name')}", prompt)
        return jsonify({
            "status": "success",
            "message": message,
            "flow_info": {
                "name": flow_config.get('name'),
                "description": flow_config.get('description')
            }
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/api/v1/translate', methods=['POST'])
@require_api_key
def translate_endpoint():
    data = request.get_json()
    text = data.get('text')
    target_language = data.get('target_language', 'English')
    if not text:
        return jsonify({"error": _("Text is required")}), 400
    message = google_ai.translate_text(text, target_language)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/register_public', methods=['POST'])
def register_public():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({"error": _("Username is required")}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": _("Username already exists")}), 400

    api_key = secrets.token_hex(16)
    new_user = User(username=username, api_key=api_key)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "api_key": new_user.api_key
    }), 201

@app.route('/api/v1/login', methods=['POST'])
def login_api():
    data = request.get_json()
    api_key = data.get('api_key')
    if not api_key:
        return jsonify({"error": _("API key is required")}), 400
    user = User.query.filter_by(api_key=api_key).first()
    if not user:
        return jsonify({"error": _("Invalid API key")}), 401

    return jsonify({
        "id": user.id,
        "username": user.username,
        "api_key": user.api_key
    }), 200

@app.route('/api/v1/me_api', methods=['GET'])
@require_api_key
def me_api():
    return jsonify({
        "id": g.user.id,
        "username": g.user.username,
        "subscription_status": g.user.subscription_status,
        "subscription_plan": g.user.subscription_plan
    })

@app.route('/api/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    if not username:
        return jsonify({"error": _("Username is required")}), 400
    if User.query.filter_by(username=username).first():
        return jsonify({"error": _("Username already exists")}), 400
    api_key = secrets.token_hex(16)
    new_user = User(username=username, api_key=api_key)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({
        "id": new_user.id,
        "username": new_user.username,
        "api_key": new_user.api_key
    }), 201

@app.route('/api/me', methods=['GET'])
@require_api_key
def me():
    return jsonify({
        "id": g.user.id,
        "username": g.user.username
    })

@app.route('/api/v1/portfolio/projects', methods=['GET'])
def get_projects():
    projects = Project.query.all()
    return jsonify([
        {
            'id': project.id,
            'title': project.title,
            'description': project.description,
            'image_url': project.image_url
        } for project in projects
    ])

@app.route('/api/v1/projects', methods=['POST'])
@require_api_key
def create_project():
    data = request.get_json()
    title = data.get('title')
    description = data.get('description')

    if not all([title, description]):
        return jsonify({"error": _("Title and description are required")}), 400

    new_project = Project(
        title=title,
        description=description,
        image_url='https://via.placeholder.com/300x200'  # Placeholder image
    )
    db.session.add(new_project)
    db.session.commit()

    return jsonify({
        'id': new_project.id,
        'title': new_project.title,
        'description': new_project.description,
        'image_url': new_project.image_url
    }), 201

@app.route('/api/v1/promotions', methods=['POST'])
@require_api_key
def create_promotion():
    data = request.get_json()
    description = data.get('description')

    if not description:
        return jsonify({"error": _("Description is required")}), 400

    promotion_text = google_ai.generate_social_media_post(description)
    return jsonify({"promotion_text": promotion_text})


@app.route('/api/v1/promote', methods=['POST'])
@require_api_key
def create_promotion_from_url():
    data = request.get_json()
    url = data.get('url')
    if not url:
        return jsonify({"error": _("URL is required")}), 400

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')
        # Extract text from the body, trying to get meaningful content
        text_content = ' '.join(t.strip() for t in soup.body.find_all(string=True) if t.parent.name not in ['style', 'script', 'head', 'title', 'meta', '[document]'])
        if not text_content:
            return jsonify({"error": _("Could not extract meaningful content from the URL.")}), 400
        # Limit the content size to avoid overly large payloads to the AI model
        promotion_text = google_ai.generate_promotion_from_content(url, text_content[:4000])
        return jsonify({"promotion_text": promotion_text})
    except requests.RequestException as e:
        return jsonify({"error": _("Error fetching URL: %(error)s", error=str(e))}), 400
    except Exception as e:
        return jsonify({"error": _("An unexpected error occurred: %(error)s", error=str(e))}), 500

@app.route('/api/v1/payment/create-subscription-checkout', methods=['POST'])
@require_api_key
def create_subscription_checkout():
    data = request.get_json()
    plan = data.get('plan') # 'premium' or 'pro'

    if plan not in ['premium', 'pro']:
        return jsonify({"error": _("Invalid plan")}), 400

    price_id = os.environ.get(f'STRIPE_{plan.upper()}_PRICE_ID')
    if not price_id:
        return jsonify({"error": f"Stripe Price ID for {plan} not configured"}), 500

    try:
        checkout_params = {
            'line_items': [
                {
                    'price': price_id,
                    'quantity': 1,
                },
            ],
            'mode': 'subscription',
            'success_url': request.host_url + 'dashboard?session_id={CHECKOUT_SESSION_ID}',
            'cancel_url': request.host_url + 'dashboard',
            'client_reference_id': str(g.user.id),
            'metadata': {
                'user_id': g.user.id,
                'plan': plan
            }
        }

        if g.user.stripe_customer_id:
            checkout_params['customer'] = g.user.stripe_customer_id
        else:
            checkout_params['customer_email'] = g.user.username if '@' in g.user.username else None

        checkout_session = stripe.checkout.Session.create(**checkout_params)
        return jsonify({'url': checkout_session.url})
    except Exception as e:
        return jsonify(error=str(e)), 403


@app.route('/api/v1/payment/create-payment-intent', methods=['POST'])
@require_api_key
def create_payment_intent():
    data = request.get_json()
    amount = data.get('amount')
    currency = data.get('currency')

    if not all([amount, currency]):
        return jsonify({"error": _("Amount and currency are required")}), 400

    try:
        amount_in_cents = int(float(amount) * 100)
    except ValueError:
        return jsonify({"error": _("Invalid amount")}), 400

    # Create a payment record in our database
    new_payment = Payment(
        user_id=g.user.id,
        amount=amount_in_cents,
        currency=currency,
        status='pending' # Start with pending status
    )
    db.session.add(new_payment)
    db.session.commit()

    try:
        intent = stripe.PaymentIntent.create(
            amount=amount_in_cents,
            currency=currency,
            automatic_payment_methods={"enabled": True},
            metadata={
                'payment_id': new_payment.id # Pass our internal payment ID to Stripe
            }
        )
        return jsonify({
            'clientSecret': intent.client_secret,
            'paymentId': new_payment.id
        })
    except Exception as e:
        # If Stripe fails, we should probably roll back the DB transaction or mark the payment as failed.
        # For now, let's just return an error.
        return jsonify(error=str(e)), 403


@app.route('/api/v1/payment/webhook', methods=['POST'])
def payment_webhook():
    payload = request.data
    sig_header = request.headers.get('Stripe-Signature')
    endpoint_secret = os.environ.get("STRIPE_WEBHOOK_SECRET")

    if not endpoint_secret:
        return jsonify({"error": "Stripe webhook secret not configured"}), 500

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return jsonify(error=str(e)), 400
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return jsonify(error=str(e)), 400

    # Handle the event
    if event['type'] == 'payment_intent.succeeded':
        payment_intent = event['data']['object']
        payment_id = payment_intent['metadata'].get('payment_id')
        if payment_id:
            payment = Payment.query.get(int(payment_id))
            if payment:
                payment.status = 'succeeded'
                payment.meta_payment_id = payment_intent.id # Let's store the stripe payment intent id here
                db.session.commit()
    elif event['type'] == 'checkout.session.completed':
        session_obj = event['data']['object']
        user_id = session_obj.get('client_reference_id')
        customer_id = session_obj.get('customer')
        if user_id:
            user = User.query.get(int(user_id))
            if user:
                user.subscription_status = 'active'
                if customer_id:
                    user.stripe_customer_id = customer_id
                # Plan can be retrieved from metadata if set during session creation
                plan = session_obj.get('metadata', {}).get('plan', 'premium')
                user.subscription_plan = plan
                db.session.commit()
    elif event['type'] == 'customer.subscription.deleted':
        subscription = event['data']['object']
        user = User.query.filter_by(stripe_customer_id=subscription.customer).first()
        if user:
            user.subscription_status = 'inactive'
            user.subscription_plan = 'free'
            db.session.commit()
    elif event['type'] == 'customer.subscription.updated':
        subscription = event['data']['object']
        user = User.query.filter_by(stripe_customer_id=subscription.customer).first()
        if user:
            if subscription.status in ['active', 'trialing']:
                user.subscription_status = 'active'
            else:
                user.subscription_status = 'inactive'
            db.session.commit()
    elif event['type'] == 'payment_intent.payment_failed':
        payment_intent = event['data']['object']
        payment_id = payment_intent['metadata'].get('payment_id')
        if payment_id:
            payment = Payment.query.get(int(payment_id))
            if payment:
                payment.status = 'failed'
                db.session.commit()
    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(status='success')


@app.route('/api/v1/meta/campaigns', methods=['GET'])
@require_api_key
def get_meta_campaigns():
    """Fetches ad campaigns from the Meta Ads API."""
    ad_account_id = os.environ.get('META_AD_ACCOUNT_ID')
    if not ad_account_id:
        return jsonify({"error": "Meta Ad Account ID is not configured."}), 500
    try:
        account = AdAccount(f'act_{ad_account_id}')
        campaigns = account.get_campaigns(fields=[
            'name',
            'status',
            'objective'
        ])
        return jsonify([campaign for campaign in campaigns])
    except FacebookRequestError as e:
        return jsonify({"error": f"Meta API Error: {e.api_error_message()}"}), e.api_error_code()
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# The following block is for development purposes and should not be used in production.
# Use a production-ready WSGI server like Gunicorn to run the.
# Example: gunicorn --bind 0.0.0.0:5000 app:app
# The database initialization is also handled separately in a production environment.
def update_db_schema():
    """Add new columns to existing database if they don't exist."""
    db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
    if os.path.exists(db_path):
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check for subscription_status
        cursor.execute("PRAGMA table_info(user)")
        columns = [column[1] for column in cursor.fetchall()]

        if 'subscription_status' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN subscription_status VARCHAR(20) DEFAULT 'inactive'")
        if 'subscription_plan' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN subscription_plan VARCHAR(20) DEFAULT 'free'")
        if 'stripe_customer_id' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN stripe_customer_id VARCHAR(120)")

        conn.commit()
        conn.close()

if __name__ == '__main__':
    with app.app_context():
        update_db_schema()
        db.create_all()
        if not Project.query.first():
            projects = [
                Project(title='Project One', description='A web application that uses AI to generate recipes based on available ingredients.', image_url='https://via.placeholder.com/300x200'),
                Project(title='Project Two', description='A mobile game that uses AI to create dynamic and challenging levels.', image_url='https://via.placeholder.com/300x200'),
                Project(title='Project Three', description='An e-commerce website that uses AI to provide personalized product recommendations.', image_url='https://via.placeholder.com/300x200')
            ]
            db.session.bulk_save_objects(projects)
            db.session.commit()
    app.run(port=5001)

@app.cli.command("init-db")
def init_db_command():
    """Creates the database tables and populates them with initial data."""
    db.create_all()
    if not Project.query.first():
        projects = [
            Project(title='Project One', description='A web application that uses AI to generate recipes based on available ingredients.', image_url='https://via.placeholder.com/300x200'),
            Project(title='Project Two', description='A mobile game that uses AI to create dynamic and challenging levels.', image_url='https://via.placeholder.com/300x200'),
            Project(title='Project Three', description='An e-commerce website that uses AI to provide personalized product recommendations.', image_url='https://via.placeholder.com/300x200')
        ]
        db.session.bulk_save_objects(projects)
        db.session.commit()
    print("Database initialized.")
