import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import time
import requests
import httpx
import asyncio
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
from flask import Flask, jsonify, render_template, request, g, session, redirect, url_for, send_file
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_cors import CORS
import secrets
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import stripe
from flask_babel import Babel, _
from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.exceptions import FacebookRequestError
import firebase_admin
from firebase_admin import credentials, messaging
import google_ai
import notion_service
import xero_service
import airtable_service
import quickbooks_service
import mailchimp_service
import elevenlabs_service
import runway_service
import tiktok_service
import whatsapp_service
import cloudinary_service
import office_service
import paystack_service
import flutterwave_service
import twilio_service
import calendly_service
import devrev_service
import shopline_service
import zendesk_service
import os_service
import json
import hmac
import hashlib
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
    credits = db.Column(db.Integer, default=1000)
    earnings = db.Column(db.Float, default=0.0)

    def __repr__(self):
        return f'<User {self.username}>'

class Agent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    endpoint_url = db.Column(db.String(200), nullable=False)
    price_per_use = db.Column(db.Integer, default=50)
    category = db.Column(db.String(50), default='General')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    developer = db.relationship('User', backref=db.backref('developed_agents', lazy=True))

class Design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    preview_url = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Integer, default=500)
    category = db.Column(db.String(50), default='Web')
    content = db.Column(db.Text, nullable=True) # Could be code or JSON
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    developer = db.relationship('User', backref=db.backref('developed_designs', lazy=True))

class Purchase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    item_type = db.Column(db.String(20), nullable=False) # 'agent' or 'design'
    item_id = db.Column(db.Integer, nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship('User', backref=db.backref('purchases', lazy=True))

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
    paystack_reference = db.Column(db.String(120), unique=True, nullable=True)
    flutterwave_tx_ref = db.Column(db.String(120), unique=True, nullable=True)
    user = db.relationship('User', backref=db.backref('payments', lazy=True))
    def __repr__(self):
        return f'<Payment {self.id}>'

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    filename = db.Column(db.String(200), nullable=False)
    file_type = db.Column(db.String(50), nullable=False) # 'document', 'image', 'video', etc.
    content = db.Column(db.Text, nullable=True) # For AI-generated documents
    filepath = db.Column(db.String(500), nullable=True) # For uploaded files
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship('User', backref=db.backref('files', lazy=True))

    def __repr__(self):
        return f'<File {self.filename}>'

class ActivityLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    action = db.Column(db.String(100), nullable=False)
    details = db.Column(db.String(500), nullable=True)
    ip_address = db.Column(db.String(45), nullable=True)
    user_agent = db.Column(db.String(200), nullable=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    user = db.relationship('User', backref=db.backref('activity_logs', lazy=True))

    def __repr__(self):
        return f'<ActivityLog {self.action} by {self.user_id}>'

class TrainingData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    completion = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default='General')
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, server_default=db.func.now())

    def __repr__(self):
        return f'<TrainingData {self.id}>'

# --- Flask App Setup ---
app = Flask(__name__, template_folder='frontend/templates', static_folder='frontend/static')
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
CORS(app, resources={r"/api/*": {"origins": ["https://yendoukoa.ai", "http://localhost:5173", "http://localhost:3000"]}}, supports_credentials=True)
app.config['SECRET_KEY'] = secrets.token_hex(16)
# Ensure we use the absolute path for the database to avoid confusion between current working directory and app file location
import os
db_abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'project.db'))
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_abs_path}'
print(f"Using database at: {app.config['SQLALCHEMY_DATABASE_URI']}")
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

def initialize_firebase_sdk():
    """Initializes the Firebase Admin SDK."""
    firebase_creds_path = os.environ.get('FIREBASE_SERVICE_ACCOUNT_JSON')
    if firebase_creds_path and os.path.exists(firebase_creds_path):
        try:
            cred = credentials.Certificate(firebase_creds_path)
            firebase_admin.initialize_app(cred)
            print("Firebase Admin SDK initialized successfully.")
        except Exception as e:
            print(f"Error initializing Firebase Admin SDK: {e}")
    else:
        print("Firebase service account credentials not found. Skipping initialization.")

with app.app_context():
    initialize_meta_sdk()
    initialize_firebase_sdk()
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
        raw_url = f"https://raw.githubusercontent.com/{user}/{repo}/{branch}/{file_path}"
        headers = {'User-Agent': 'AI-Agent-Checker/1.0'}
        response = requests.get(raw_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return _("Error fetching file from GitHub: %(error)s", error=e)
    except Exception as e:
        return _("An unexpected error occurred: %(error)s", error=e)

# --- Helpers ---
def log_activity(action, details=None, user_id=None):
    if user_id is None:
        user_id = g.user.id if hasattr(g, 'user') and g.user else None

    # Check for active request context
    ip_address = None
    user_agent = None
    if request:
        ip_address = request.remote_addr
        user_agent = request.headers.get('User-Agent')

    log = ActivityLog(
        user_id=user_id,
        action=action,
        details=details,
        ip_address=ip_address,
        user_agent=user_agent
    )
    db.session.add(log)
    db.session.commit()

def log_training_data(prompt, completion, category='General'):
    """Logs anonymized prompt-response pairs for AI training contribution."""
    try:
        # Simple anonymization: check for common sensitive patterns (very basic)
        # In a real app, this would be much more robust.
        sensitive_patterns = [r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', r'\b\d{4}-\d{4}-\d{4}-\d{4}\b']
        is_sensitive = any(re.search(pattern, prompt) or re.search(pattern, completion) for pattern in sensitive_patterns)

        if not is_sensitive:
            data = TrainingData(prompt=prompt, completion=completion, category=category)
            db.session.add(data)
            db.session.commit()
    except Exception as e:
        print(f"Error logging training data: {e}")
        db.session.rollback()

# --- API Endpoints ---
def require_api_key(f):
    @wraps(f)
    async def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key') or request.args.get('api_key')
        if not api_key:
            return jsonify({"error": _("API key is missing")}), 401
        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            return jsonify({"error": _("Invalid API key")}), 401
        g.user = user
        return await f(*args, **kwargs) if asyncio.iscoroutinefunction(f) else f(*args, **kwargs)
    return decorated_function

@app.route('/api/config')
@app.route('/api/v1/config')
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
    log_training_data(prompt, message, category='Development')
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
    log_training_data(prompt, message, category='Blockchain')
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
    log_training_data(prompt, message, category='Language')
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/research/dataset', methods=['GET'])
def get_public_dataset():
    category = request.args.get('category')
    query = TrainingData.query.filter_by(is_public=True)
    if category:
        query = query.filter_by(category=category)
    data = query.order_by(TrainingData.created_at.desc()).limit(100).all()
    return jsonify([{
        "id": d.id,
        "prompt": d.prompt,
        "completion": d.completion,
        "category": d.category,
        "created_at": d.created_at.isoformat()
    } for d in data])

@app.route('/api/v1/research/dataset-architect', methods=['POST'])
@require_api_key
def dataset_architect_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_dataset_architect_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/research/training-strategist', methods=['POST'])
@require_api_key
def training_strategist_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_ai_training_strategist_assistance(prompt)
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


@app.route('/api/v1/security/sentinel', methods=['POST'])
@require_api_key
def cybersecurity_sentinel_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_cybersecurity_sentinel_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/automotive/security', methods=['POST'])
@require_api_key
def automotive_security_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_automotive_security_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/security/os-hardening', methods=['POST'])
@require_api_key
def cyber_os_hardening_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_cyber_os_hardening_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/security/scam-detector', methods=['POST'])
@require_api_key
def scam_detector_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_scam_detection_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/develop/android', methods=['POST'])
@require_api_key
def develop_android_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_android_dev_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/develop/ios', methods=['POST'])
@require_api_key
def develop_ios_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_ios_dev_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/mobile/sdk-integration', methods=['POST'])
@require_api_key
def mobile_sdk_integration_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_mobile_sdk_integration_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/mobile/push', methods=['POST'])
@require_api_key
async def send_push_notification():
    data = request.get_json()
    token = data.get('token')
    title = data.get('title')
    body = data.get('body')

    if not all([token, title, body]):
        return jsonify({"error": _("Token, title, and body are required")}), 400

    try:
        # Check if Firebase is initialized
        if not firebase_admin._apps:
            return jsonify({"error": _("Firebase SDK not initialized")}), 500

        message = messaging.Message(
            notification=messaging.Notification(
                title=title,
                body=body,
            ),
            token=token,
        )
        response = await asyncio.to_thread(messaging.send, message)
        return jsonify({"status": "success", "message_id": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


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

@app.route('/api/v1/xero/assistance', methods=['POST'])
@require_api_key
def xero_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # Generate structured data for Xero
        invoice_data = google_ai.generate_xero_invoice_data(prompt)
        if not invoice_data or 'contact_name' not in invoice_data:
            return jsonify({"error": _("Could not generate valid Xero invoice data from prompt")}), 400

        # Step 1: Create or get contact (Simplified: we use search or create)
        # For simplicity, we just try to create a contact
        contact_res = xero_service.create_contact(invoice_data['contact_name'])
        if 'error' in contact_res:
            return jsonify({"error": _("Xero Contact Error: %(error)s", error=contact_res['error'])}), 400

        contact_id = contact_res['contact']['contact_id']

        # Step 2: Create invoice
        invoice_res = xero_service.create_invoice(
            contact_id,
            invoice_data.get('amount', 0),
            invoice_data.get('description', 'AI Generated Invoice')
        )
        if 'error' in invoice_res:
            return jsonify({"error": _("Xero Invoice Error: %(error)s", error=invoice_res['error'])}), 400

        message = _("Successfully executed Xero action: Invoice created for %(contact)s. Details: %(details)s",
                    contact=invoice_data['contact_name'], details=str(invoice_res['invoice']))
        return jsonify({"status": "success", "message": message, "invoice": invoice_res['invoice']})

    message = google_ai.provide_xero_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/finance/quickbooks/assistance', methods=['POST'])
@require_api_key
def quickbooks_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # Generate structured data for QuickBooks
        invoice_data = google_ai.generate_quickbooks_invoice_data(prompt)
        if not invoice_data or 'customer_name' not in invoice_data:
            return jsonify({"error": _("Could not generate valid QuickBooks invoice data from prompt")}), 400

        # Step 1: Create or get customer
        customer_res = quickbooks_service.create_customer(invoice_data['customer_name'])
        if 'error' in customer_res:
            return jsonify({"error": _("QuickBooks Customer Error: %(error)s", error=customer_res['error'])}), 400

        customer_id = customer_res['customer']['Id']

        # Step 2: Create invoice
        invoice_res = quickbooks_service.create_invoice(
            customer_id,
            invoice_data.get('amount', 0),
            invoice_data.get('description', 'AI Generated Invoice')
        )
        if 'error' in invoice_res:
            return jsonify({"error": _("QuickBooks Invoice Error: %(error)s", error=invoice_res['error'])}), 400

        message = _("Successfully executed QuickBooks action: Invoice created for %(customer)s. Details: %(details)s",
                    customer=invoice_data['customer_name'], details=str(invoice_res['invoice']))
        return jsonify({"status": "success", "message": message, "invoice": invoice_res['invoice']})

    message = google_ai.provide_quickbooks_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/database/airtable/assistance', methods=['POST'])
@require_api_key
def airtable_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # Generate structured data for Airtable
        record_data = google_ai.generate_airtable_record_data(prompt)
        if not record_data or 'table_name' not in record_data:
            return jsonify({"error": _("Could not generate valid Airtable data from prompt")}), 400

        result = airtable_service.create_record(
            record_data['table_name'],
            record_data.get('fields', {})
        )

        if 'error' in result:
            return jsonify({"error": _("Airtable Execution Error: %(error)s", error=result['error'])}), 400

        message = _("Successfully executed Airtable action: Record created in table '%(table)s'.", table=record_data['table_name'])
        return jsonify({"status": "success", "message": message, "record": result['record']})

    message = google_ai.provide_airtable_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/notion/assistance', methods=['POST'])
@require_api_key
def notion_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # Generate structured data for Notion
        notion_data = google_ai.generate_notion_page_data(prompt)
        if not notion_data or 'title' not in notion_data:
            return jsonify({"error": _("Could not generate valid Notion data from prompt")}), 400

        parent_page_id = data.get('parent_page_id') or os.environ.get("NOTION_DEFAULT_PAGE_ID")
        if not parent_page_id:
             return jsonify({"error": _("Parent Page ID is required for Notion execution")}), 400

        result = notion_service.create_page(
            parent_page_id,
            notion_data['title'],
            notion_data.get('content_blocks')
        )

        if 'error' in result:
            return jsonify({"error": _("Notion Execution Error: %(error)s", error=result['error'])}), 400

        message = _("Successfully executed Notion action: Page '%(title)s' created.", title=notion_data['title'])
        return jsonify({"status": "success", "message": message, "page": result['page']})

    message = google_ai.provide_notion_assistance(prompt)
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


@app.route('/api/v1/offshore/assistance', methods=['POST'])
@require_api_key
def offshore_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_offshore_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/marketing/affiliate-mlm', methods=['POST'])
@require_api_key
def affiliate_mlm_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_affiliate_mlm_assistance(prompt)
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


@app.route('/api/v1/marketing/video', methods=['POST'])
@require_api_key
def marketing_video_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.generate_google_veo_video(prompt)
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


@app.route('/api/v1/gumloop/assistance', methods=['POST'])
@require_api_key
def gumloop_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    pipeline_id = data.get('pipeline_id')
    inputs = data.get('inputs', {})

    if not prompt and not execute:
        return jsonify({"error": _("Prompt or execute flag is required")}), 400

    if execute:
        if not pipeline_id:
            return jsonify({"error": _("Pipeline ID is required for execution")}), 400
        result = google_ai.run_gumloop_workflow(pipeline_id, inputs)
        return jsonify({"status": "success", "message": str(result)})

    message = google_ai.provide_gumloop_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/n8n/assistance', methods=['POST'])
@require_api_key
def n8n_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    webhook_url = data.get('webhook_url')
    payload = data.get('payload', {})

    if not prompt and not execute:
        return jsonify({"error": _("Prompt or execute flag is required")}), 400

    if execute:
        result = google_ai.trigger_n8n_webhook(webhook_url, payload)
        return jsonify({"status": "success", "message": str(result)})

    message = google_ai.provide_n8n_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/lamatic/assistance', methods=['POST'])
@require_api_key
def lamatic_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    workflow_id = data.get('workflow_id')

    if not prompt and not execute:
        return jsonify({"error": _("Prompt or execute flag is required")}), 400

    if execute:
        if not workflow_id:
            return jsonify({"error": _("Workflow ID is required for execution")}), 400
        result = google_ai.execute_lamatic_workflow(workflow_id, prompt)
        return jsonify({"status": "success", "message": str(result)})

    message = google_ai.provide_lamatic_assistance(prompt)
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

@app.route('/api/v1/blockchain/sponsoring', methods=['POST'])
@require_api_key
def blockchain_sponsoring_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_blockchain_sponsoring_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/zapier/assistance', methods=['POST'])
@require_api_key
def zapier_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_zapier_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/odoo/assistance', methods=['POST'])
@require_api_key
def odoo_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_odoo_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/sage/assistance', methods=['POST'])
@require_api_key
def sage_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_sage_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/fine-tuner/assistance', methods=['POST'])
@require_api_key
def fine_tuner_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_fine_tuning_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/rag-tuning/assistance', methods=['POST'])
@require_api_key
async def rag_tuning_assistance_endpoint():
    # Use current_user from require_api_key (it sets g.user)
    user = g.user
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    # Retrieve user documents for RAG context - only selecting needed fields
    user_files = File.query.with_entities(File.filename, File.content).filter_by(user_id=user.id, file_type='document').all()
    context_files = []
    for f in user_files:
        if f.content:
            context_files.append({
                "filename": f.filename,
                "content": f.content
            })

    # Run the blocking AI call in a thread to keep the event loop free
    message = await asyncio.to_thread(google_ai.provide_rag_tuning_assistance, prompt, context_files)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/router/assistance', methods=['POST'])
@require_api_key
def router_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_router_capacity_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/antigravity/agent', methods=['POST'])
@require_api_key
def antigravity_agent_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_antigravity_agent_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/gemini/spark', methods=['POST'])
@require_api_key
def gemini_spark_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_gemini_spark_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/sponsorship/open-collective', methods=['POST'])
@require_api_key
def open_collective_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_open_collective_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/sponsorship/patreon', methods=['POST'])
@require_api_key
def patreon_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_patreon_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/video/assistance', methods=['POST'])
@require_api_key
def video_production_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_video_production_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/deepmind/image', methods=['POST'])
@require_api_key
def deepmind_image_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    image_base64 = google_ai.generate_deepmind_image(prompt)
    if image_base64.startswith("Error"):
        return jsonify({"status": "error", "message": image_base64}), 500
    return jsonify({
        "status": "success",
        "message": "Image generated successfully using DeepMind Imagen.",
        "image_data": image_base64
    })


@app.route('/api/v1/deepmind/video', methods=['POST'])
@require_api_key
def deepmind_video_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.generate_deepmind_video_content(prompt)
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


@app.route('/api/v1/github-models/assistance', methods=['POST'])
@require_api_key
def github_models_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    model_name = data.get('model_name', 'gpt-4o')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_github_model_intelligence(prompt, model_name)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/copilot-chat/assistance', methods=['POST'])
@require_api_key
def copilot_chat_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_github_copilot_chat(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/copilot/coding', methods=['POST'])
@require_api_key
async def copilot_coding_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    # Use await asyncio.to_thread() to handle potential blocking call in thread
    message = await asyncio.to_thread(google_ai.provide_github_copilot_coding, prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/language/specialist', methods=['POST'])
@require_api_key
def language_specialist_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_language_specialist_assistance(prompt)
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

    g.user = new_user
    log_activity("register", f"User {username} registered")

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

    g.user = user
    log_activity("login", f"User {user.username} logged in")

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
        "subscription_plan": g.user.subscription_plan,
        "credits": g.user.credits,
        "earnings": g.user.earnings
    })

def is_safe_url(url):
    """Basic SSRF protection."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return False
        hostname = parsed.hostname
        if not hostname:
            return False
        # Allow internal calls for registered agents if explicitly allowed via environment variable
        if hostname in ['localhost', '127.0.0.1', '0.0.0.0']:
            return os.environ.get('ALLOW_INTERNAL_AGENTS') == 'true'
        # Block internal IP ranges (simple check)
        if hostname.startswith('192.168.') or hostname.startswith('10.') or hostname.startswith('172.'):
            return False
        # Block cloud metadata service
        if hostname == '169.254.169.254':
            return False
        return True
    except:
        return False

@app.route('/api/v1/store/agents', methods=['GET'])
def list_store_agents():
    category = request.args.get('category')
    query = Agent.query.filter_by(is_active=True)
    if category and category != 'All':
        query = query.filter_by(category=category)
    agents = query.all()
    # Add debug logging
    print(f"Found {len(agents)} agents in the store.")
    return jsonify([{
        "id": a.id,
        "developer_id": a.developer_id,
        "developer_name": a.developer.username if a.developer else "Unknown",
        "name": a.name,
        "description": a.description,
        "price_per_use": a.price_per_use,
        "category": a.category,
        "created_at": a.created_at.isoformat() if a.created_at else None
    } for a in agents])

@app.route('/api/v1/store/agents', methods=['POST'])
@require_api_key
def register_store_agent():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    endpoint_url = data.get('endpoint_url')
    price_per_use = data.get('price_per_use', 50)
    category = data.get('category', 'General')

    if not all([name, description, endpoint_url]):
        return jsonify({"error": _("Name, description, and endpoint_url are required")}), 400

    if not is_safe_url(endpoint_url):
        return jsonify({"error": _("Invalid or unsafe endpoint URL")}), 400

    new_agent = Agent(
        developer_id=g.user.id,
        name=name,
        description=description,
        endpoint_url=endpoint_url,
        price_per_use=price_per_use,
        category=category
    )
    db.session.add(new_agent)
    db.session.commit()
    return jsonify({"status": "success", "id": new_agent.id}), 201

@app.route('/api/v1/store/designs', methods=['GET'])
def list_store_designs():
    category = request.args.get('category')
    query = Design.query
    if category and category != 'All':
        query = query.filter_by(category=category)
    designs = query.all()
    return jsonify([{
        "id": d.id,
        "developer_id": d.developer_id,
        "developer_name": d.developer.username,
        "name": d.name,
        "description": d.description,
        "preview_url": d.preview_url,
        "price": d.price,
        "category": d.category,
        "created_at": d.created_at.isoformat()
    } for d in designs])

@app.route('/api/v1/store/designs', methods=['POST'])
@require_api_key
def register_store_design():
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    price = data.get('price', 500)
    category = data.get('category', 'Web')
    content = data.get('content')
    preview_url = data.get('preview_url')

    if not all([name, description]):
        return jsonify({"error": _("Name and description are required")}), 400

    new_design = Design(
        developer_id=g.user.id,
        name=name,
        description=description,
        price=price,
        category=category,
        content=content,
        preview_url=preview_url
    )
    db.session.add(new_design)
    db.session.commit()
    return jsonify({"status": "success", "id": new_design.id}), 201

@app.route('/api/v1/store/execute', methods=['POST'])
@require_api_key
async def execute_agent():
    data = request.get_json()
    agent_id = data.get('agent_id')
    prompt = data.get('prompt')

    if not agent_id:
        return jsonify({"error": _("Agent ID is required")}), 400

    agent = db.session.get(Agent, agent_id)
    if not agent or not agent.is_active:
        return jsonify({"error": _("Agent not found or inactive")}), 404

    if g.user.credits < agent.price_per_use:
        return jsonify({"error": _("Insufficient credits")}), 403

    # Call third-party agent FIRST
    try:
        async with httpx.AsyncClient() as client:
            # Note: We pass a temporary token or just let the agent know who the user is
            # In production, this would be a signed request
            headers = {"X-API-Key": g.user.api_key}
            response = await client.post(agent.endpoint_url, json={"prompt": prompt, "user_id": g.user.id}, headers=headers, timeout=30)
            response.raise_for_status()
            agent_result = response.json()
    except Exception as e:
        return jsonify({"error": _("Error executing third-party agent: %(error)s", error=str(e))}), 500

    # If successful, THEN deduct credits and pay developer
    try:
        log_activity("execute_agent", f"Executed agent {agent.name} (ID: {agent.id})")
        g.user.credits -= agent.price_per_use
        developer = db.session.get(User, agent.developer_id)
        if developer:
            earned_credits = int(agent.price_per_use * 0.8)
            developer.credits += earned_credits
            developer.earnings += float(earned_credits)

        # Log purchase
        purchase = Purchase(user_id=g.user.id, item_type='agent_execution', item_id=agent.id, amount=agent.price_per_use)
        db.session.add(purchase)
        db.session.commit()

        # Monetization Enhancement: Log to Notion if configured
        notion_db_id = os.environ.get("NOTION_MONETIZATION_DB_ID")
        if notion_db_id:
            try:
                notion_service.add_to_database(notion_db_id, {
                    "Item": {"title": [{"text": {"content": f"Agent: {agent.name}"}}]},
                    "Type": {"select": {"name": "Agent Execution"}},
                    "User": {"rich_text": [{"text": {"content": g.user.username}}]},
                    "Amount": {"number": agent.price_per_use},
                    "Date": {"date": {"start": time.strftime("%Y-%m-%d")}}
                })
            except:
                pass # Non-blocking

        return jsonify(agent_result)
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": _("Internal error during credit processing: %(error)s", error=str(e))}), 500

@app.route('/api/v1/store/purchase', methods=['POST'])
@require_api_key
def purchase_design():
    data = request.get_json()
    design_id = data.get('design_id')

    if not design_id:
        return jsonify({"error": _("Design ID is required")}), 400

    design = db.session.get(Design, design_id)
    if not design:
        return jsonify({"error": _("Design not found")}), 404

    if g.user.credits < design.price:
        return jsonify({"error": _("Insufficient credits")}), 403

    try:
        log_activity("purchase_design", f"Purchased design {design.name} (ID: {design.id})")
        # Deduct credits
        g.user.credits -= design.price
        # Pay developer (80%)
        developer = db.session.get(User, design.developer_id)
        if developer:
            earned_credits = int(design.price * 0.8)
            developer.credits += earned_credits
            developer.earnings += float(earned_credits)

        # Log purchase
        purchase = Purchase(user_id=g.user.id, item_type='design', item_id=design.id, amount=design.price)
        db.session.add(purchase)
        db.session.commit()

        # Monetization Enhancement: Log to Notion if configured
        notion_db_id = os.environ.get("NOTION_MONETIZATION_DB_ID")
        if notion_db_id:
            try:
                notion_service.add_to_database(notion_db_id, {
                    "Item": {"title": [{"text": {"content": f"Design: {design.name}"}}]},
                    "Type": {"select": {"name": "Design Purchase"}},
                    "User": {"rich_text": [{"text": {"content": g.user.username}}]},
                    "Amount": {"number": design.price},
                    "Date": {"date": {"start": time.strftime("%Y-%m-%d")}}
                })
            except:
                pass # Non-blocking

        return jsonify({
            "status": "success",
            "message": _("Design purchased successfully"),
            "content": design.content
        })
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": _("Internal error during purchase: %(error)s", error=str(e))}), 500

@app.route('/api/register', methods=['POST'])
@app.route('/api/v1/register', methods=['POST'])
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
@app.route('/api/v1/me', methods=['GET'])
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
            payment = db.session.get(Payment, int(payment_id))
            if payment:
                payment.status = 'succeeded'
                payment.meta_payment_id = payment_intent.id # Let's store the stripe payment intent id here
                db.session.commit()
    elif event['type'] == 'checkout.session.completed':
        session_obj = event['data']['object']
        user_id = session_obj.get('client_reference_id')
        customer_id = session_obj.get('customer')
        if user_id:
            user = db.session.get(User, int(user_id))
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
            payment = db.session.get(Payment, int(payment_id))
            if payment:
                payment.status = 'failed'
                db.session.commit()
    else:
        print('Unhandled event type {}'.format(event['type']))

    return jsonify(status='success')


@app.route('/api/v1/payment/paystack/initialize', methods=['POST'])
@require_api_key
def paystack_initialize_payment():
    data = request.get_json()
    amount = data.get('amount') # In major currency unit (e.g. GHS, NGN)
    currency = data.get('currency', 'NGN')
    callback_url = data.get('callback_url')

    if not amount:
        return jsonify({"error": _("Amount is required")}), 400

    try:
        amount_in_kobo = int(float(amount) * 100)
    except ValueError:
        return jsonify({"error": _("Invalid amount")}), 400

    # Create a payment record in our database
    new_payment = Payment(
        user_id=g.user.id,
        amount=amount_in_kobo,
        currency=currency,
        status='pending'
    )
    db.session.add(new_payment)
    db.session.commit()

    metadata = {
        "payment_id": new_payment.id,
        "user_id": g.user.id
    }

    response = paystack_service.initialize_transaction(
        email=g.user.username if '@' in g.user.username else f"{g.user.username}@yendoukoa.ai",
        amount=amount_in_kobo,
        callback_url=callback_url,
        metadata=metadata
    )

    if response.get('status'):
        new_payment.paystack_reference = response['data']['reference']
        db.session.commit()
        return jsonify(response)
    else:
        new_payment.status = 'failed'
        db.session.commit()
        return jsonify(response), 400


@app.route('/api/v1/payment/paystack/verify/<reference>', methods=['GET'])
@require_api_key
def paystack_verify_payment(reference):
    response = paystack_service.verify_transaction(reference)

    if response.get('status') and response.get('data') and response['data'].get('status') == 'success':
        payment = Payment.query.filter_by(paystack_reference=reference).first()
        if payment and payment.status != 'succeeded':
            payment.status = 'succeeded'
            db.session.commit()
            log_activity("paystack_payment_success", f"Payment {payment.id} succeeded")
            fulfill_payment(payment)
        elif payment and payment.status == 'succeeded':
            fulfill_payment(payment)

    return jsonify(response)


def fulfill_payment(payment):
    """Fulfills a payment by adding credits to the user's account."""
    if payment.status == 'succeeded':
        # Check if already fulfilled - we can use ActivityLog or another column
        # For now, we'll assume if status is 'succeeded', it's done or being done.
        # To avoid double fulfillment, we should use a more robust check.
        # Let's check if there's an activity log for this specific payment.
        existing_log = ActivityLog.query.filter_by(user_id=payment.user_id, action="credit_purchase", details=f"Payment ID: {payment.id}").first()
        if existing_log:
            return

        user = db.session.get(User, payment.user_id)
        if user:
            # 1 major unit = 10 credits. payment.amount is in kobo.
            credits_to_add = int(payment.amount / 10)
            user.credits += credits_to_add
            db.session.commit()
            log_activity("credit_purchase", f"Payment ID: {payment.id}", user_id=payment.user_id)


@app.route('/api/v1/payment/paystack/webhook', methods=['POST'])
def paystack_webhook():
    payload = request.get_json()
    sig_header = request.headers.get('x-paystack-signature')

    if not sig_header:
        return jsonify({"error": "No signature"}), 400

    secret = os.environ.get('PAYSTACK_SECRET_KEY', '')
    computed_hash = hmac.new(secret.encode('utf-8'), request.data, hashlib.sha512).hexdigest()

    if computed_hash != sig_header:
        return jsonify({"error": "Invalid signature"}), 400

    event = payload.get('event')
    data = payload.get('data')

    if event == 'charge.success':
        reference = data.get('reference')
        payment = Payment.query.filter_by(paystack_reference=reference).first()
        if payment and payment.status != 'succeeded':
            payment.status = 'succeeded'
            db.session.commit()
            fulfill_payment(payment)

    return jsonify(status='success'), 200


@app.route('/api/v1/payment/flutterwave/initialize', methods=['POST'])
@require_api_key
def flutterwave_initialize_payment():
    data = request.get_json()
    amount = data.get('amount')
    currency = data.get('currency', 'NGN')
    callback_url = data.get('callback_url')

    if not amount:
        return jsonify({"error": _("Amount is required")}), 400

    tx_ref = f"flw-{secrets.token_hex(8)}"

    # Create a payment record in our database
    new_payment = Payment(
        user_id=g.user.id,
        amount=int(float(amount) * 100), # Store in cents/kobo
        currency=currency,
        status='pending',
        flutterwave_tx_ref=tx_ref
    )
    db.session.add(new_payment)
    db.session.commit()

    response = flutterwave_service.initialize_transaction(
        email=g.user.username if '@' in g.user.username else f"{g.user.username}@yendoukoa.ai",
        amount=amount,
        tx_ref=tx_ref,
        currency=currency,
        callback_url=callback_url
    )

    if response.get('status') == 'success':
        return jsonify(response)
    else:
        new_payment.status = 'failed'
        db.session.commit()
        return jsonify(response), 400


@app.route('/api/v1/payment/flutterwave/verify/<int:transaction_id>', methods=['GET'])
@require_api_key
def flutterwave_verify_payment(transaction_id):
    response = flutterwave_service.verify_transaction(transaction_id)

    if response.get('status') == 'success' and response.get('data') and response['data'].get('status') == 'successful':
        tx_ref = response['data'].get('tx_ref')
        payment = Payment.query.filter_by(flutterwave_tx_ref=tx_ref).first()
        if payment and payment.status != 'succeeded':
            payment.status = 'succeeded'
            db.session.commit()
            log_activity("flutterwave_payment_success", f"Payment {payment.id} succeeded")
            fulfill_payment(payment)
        elif payment and payment.status == 'succeeded':
            fulfill_payment(payment)

    return jsonify(response)


@app.route('/api/v1/files/upload', methods=['POST'])
@require_api_key
async def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": _("No file part")}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": _("No selected file")}), 400

    upload_folder = 'uploads'
    if not os.path.exists(upload_folder):
        os.makedirs(upload_folder)

    safe_filename = secure_filename(file.filename)
    filename = secrets.token_hex(8) + "_" + safe_filename
    filepath = os.path.join(upload_folder, filename)
    file.save(filepath)

    new_file = File(
        user_id=g.user.id,
        filename=file.filename,
        file_type='upload',
        filepath=filepath
    )
    db.session.add(new_file)
    db.session.commit()

    log_activity("upload_file", f"Uploaded file: {file.filename}")

    return jsonify({
        "id": new_file.id,
        "filename": new_file.filename,
        "status": "success"
    }), 201

@app.route('/api/v1/files/create-doc', methods=['POST'])
@require_api_key
async def create_doc_file():
    data = request.get_json()
    filename = data.get('filename')
    content = data.get('content')
    file_type = data.get('file_type', 'document')

    if not all([filename, content]):
        return jsonify({"error": _("Filename and content are required")}), 400

    new_file = File(
        user_id=g.user.id,
        filename=filename,
        file_type=file_type,
        content=content
    )
    db.session.add(new_file)
    db.session.commit()

    return jsonify({
        "id": new_file.id,
        "filename": new_file.filename,
        "status": "success"
    }), 201

@app.route('/api/v1/files', methods=['GET'])
@require_api_key
async def list_files():
    files = File.query.filter_by(user_id=g.user.id).all()
    return jsonify([{
        "id": f.id,
        "filename": f.filename,
        "file_type": f.file_type,
        "created_at": f.created_at.isoformat() if f.created_at else None
    } for f in files])

@app.route('/api/v1/activity', methods=['GET'])
@require_api_key
async def list_activity():
    logs = ActivityLog.query.filter_by(user_id=g.user.id).order_by(ActivityLog.created_at.desc()).limit(50).all()
    return jsonify([{
        "id": l.id,
        "action": l.action,
        "details": l.details,
        "ip_address": l.ip_address,
        "created_at": l.created_at.isoformat() if l.created_at else None
    } for l in logs])

@app.route('/api/v1/files/<int:file_id>', methods=['GET'])
@require_api_key
async def get_file(file_id):
    file_record = File.query.filter_by(id=file_id, user_id=g.user.id).first()
    if not file_record:
        return jsonify({"error": _("File not found")}), 404

    if file_record.content:
        # If content exists, we can return it as JSON if requested or as a text file
        if request.args.get('download') == 'true':
            import io
            buf = io.BytesIO(file_record.content.encode('utf-8'))
            return send_file(buf, as_attachment=True, download_name=file_record.filename, mimetype='text/plain')
        return jsonify({
            "id": file_record.id,
            "filename": file_record.filename,
            "content": file_record.content,
            "file_type": file_record.file_type
        })
    elif file_record.filepath:
        return send_file(file_record.filepath, as_attachment=True, download_name=file_record.filename)

    return jsonify({"error": _("File data not available")}), 400

@app.route('/api/v1/files/<int:file_id>', methods=['DELETE'])
@require_api_key
async def delete_file(file_id):
    file_record = File.query.filter_by(id=file_id, user_id=g.user.id).first()
    if not file_record:
        return jsonify({"error": _("File not found")}), 404

    if file_record.filepath and os.path.exists(file_record.filepath):
        os.remove(file_record.filepath)

    db.session.delete(file_record)
    db.session.commit()

    return jsonify({"status": "success", "message": _("File deleted successfully")})

@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'SAMEORIGIN'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
    return response

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

@app.route('/api/v1/mailchimp/subscribe', methods=['POST'])
@require_api_key
def mailchimp_subscribe():
    data = request.get_json()
    email = data.get('email')
    if not email:
        return jsonify({"error": _("Email is required")}), 400
    result = mailchimp_service.subscribe_to_newsletter(email)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200

@app.route('/api/v1/mailchimp/campaigns', methods=['POST'])
@require_api_key
def mailchimp_create_campaign():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    # Use AI to generate campaign details
    campaign_info = google_ai.generate_email_campaign(prompt)

    result = mailchimp_service.create_campaign(
        subject_line=campaign_info.get('subject_line', 'New Campaign'),
        preview_text=campaign_info.get('preview_text', ''),
        title=campaign_info.get('title', 'AI Generated Campaign'),
        from_name=os.environ.get("MAILCHIMP_FROM_NAME", "Yendoukoa AI"),
        reply_to=os.environ.get("MAILCHIMP_REPLY_TO", "info@yendoukoa.ai")
    )

    if "error" in result:
        return jsonify(result), 500

    campaign_id = result['id']
    content_result = mailchimp_service.set_campaign_content(campaign_id, campaign_info.get('html_content', ''))

    if "error" in content_result:
        return jsonify(content_result), 500

    return jsonify({
        "status": "success",
        "campaign_id": campaign_id,
        "campaign_info": campaign_info
    }), 201

@app.route('/api/v1/mailchimp/reports', methods=['GET'])
@require_api_key
def mailchimp_reports():
    result = mailchimp_service.get_campaign_reports()
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200

@app.route('/api/v1/mailchimp/send', methods=['POST'])
@require_api_key
def mailchimp_send_campaign():
    data = request.get_json()
    campaign_id = data.get('campaign_id')
    if not campaign_id:
        return jsonify({"error": _("Campaign ID is required")}), 400
    result = mailchimp_service.send_campaign(campaign_id)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result), 200

@app.route('/api/v1/marketing/email-specialist', methods=['POST'])
@require_api_key
def email_marketing_specialist_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_email_marketing_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/voice/elevenlabs/voices', methods=['GET'])
@require_api_key
def elevenlabs_get_voices_endpoint():
    result = elevenlabs_service.get_voices()
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/api/v1/voice/elevenlabs', methods=['POST'])
@require_api_key
def elevenlabs_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    voice_id = data.get('voice_id', "21m00Tcm4TlvDq8ikWAM")

    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        result = elevenlabs_service.text_to_speech(prompt, voice_id)
        if "error" in result:
            return jsonify(result), 500

        # Log the generated file
        new_file = File(
            user_id=g.user.id,
            filename=result['filename'],
            file_type='audio',
            filepath=result['filepath']
        )
        db.session.add(new_file)
        db.session.commit()

        return jsonify({
            "status": "success",
            "message": result['message'],
            "file_id": new_file.id,
            "filename": new_file.filename
        })

    message = google_ai.provide_elevenlabs_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/market/tiktok/me', methods=['GET'])
@require_api_key
def tiktok_get_me_endpoint():
    result = tiktok_service.get_tiktok_user_info()
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/api/v1/market/tiktok', methods=['POST'])
@require_api_key
def tiktok_marketing_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    video_url = data.get('video_url')

    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        if not video_url:
            return jsonify({"error": _("Video URL is required for TikTok sharing")}), 400
        result = tiktok_service.share_to_tiktok(video_url, prompt)
        return jsonify(result)

    message = google_ai.provide_tiktok_marketing_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/mobile/whatsapp', methods=['POST'])
@require_api_key
def whatsapp_business_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    to_number = data.get('to_number')
    template_name = data.get('template_name')

    if not prompt and not template_name:
        return jsonify({"error": _("Prompt or template_name is required")}), 400

    if execute:
        if not to_number:
            return jsonify({"error": _("Recipient phone number is required")}), 400
        if template_name:
            result = whatsapp_service.send_whatsapp_template(to_number, template_name)
        else:
            result = whatsapp_service.send_whatsapp_message(to_number, prompt)
        return jsonify(result)

    message = google_ai.provide_whatsapp_business_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/finance/flutterwave', methods=['POST'])
@require_api_key
def flutterwave_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)

    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        payment_data = google_ai.generate_flutterwave_payment_data(prompt)
        # For execution, we'd typically initialize a payment and return the link
        tx_ref = f"flw-ai-{secrets.token_hex(8)}"
        response = flutterwave_service.initialize_transaction(
            email=g.user.username if '@' in g.user.username else f"{g.user.username}@yendoukoa.ai",
            amount=payment_data.get('amount', 1000),
            tx_ref=tx_ref,
            currency=payment_data.get('currency', 'NGN'),
            callback_url=request.host_url + 'dashboard'
        )
        return jsonify(response)

    message = google_ai.provide_flutterwave_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/mobile/twilio', methods=['POST'])
@require_api_key
def twilio_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    is_whatsapp = data.get('is_whatsapp', False)

    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        message_data = google_ai.generate_twilio_message_data(prompt)
        if not all([message_data.get('to_number'), message_data.get('message_body')]):
            return jsonify({"error": _("Could not extract recipient and body from prompt")}), 400

        if is_whatsapp:
            result = twilio_service.send_whatsapp_message(message_data['to_number'], message_data['message_body'])
        else:
            result = twilio_service.send_sms(message_data['to_number'], message_data['message_body'])

        return jsonify(result)

    message = google_ai.provide_twilio_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/media/cloudinary', methods=['POST'])
@require_api_key
def cloudinary_media_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    file_id = data.get('file_id')

    if not prompt and not file_id:
        return jsonify({"error": _("Prompt or file_id is required")}), 400

    if execute:
        if not file_id:
            return jsonify({"error": _("File ID is required for upload to Cloudinary")}), 400
        file_record = db.session.get(File, file_id)
        if not file_record or not file_record.filepath:
            return jsonify({"error": _("File not found or has no path")}), 404

        result = cloudinary_service.upload_media(file_record.filepath)
        return jsonify(result)

    message = google_ai.provide_cloudinary_media_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/video/runway/status/<task_id>', methods=['GET'])
@require_api_key
def runway_video_status_endpoint(task_id):
    result = runway_service.get_task_status(task_id)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/api/v1/video/runway', methods=['POST'])
@require_api_key
def runway_video_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)

    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        result = runway_service.generate_video(prompt)
        if "error" in result:
            return jsonify(result), 500
        return jsonify(result)

    message = google_ai.provide_runway_video_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/calendly/me', methods=['GET'])
@require_api_key
def calendly_get_me_endpoint():
    result = calendly_service.get_user_info()
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/api/v1/calendly/event_types', methods=['GET'])
@require_api_key
def calendly_list_event_types_endpoint():
    user_uri = request.args.get('user')
    result = calendly_service.list_event_types(user_uri)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/api/v1/calendly/events', methods=['GET'])
@require_api_key
def calendly_list_events_endpoint():
    user_uri = request.args.get('user')
    count = request.args.get('count', 10, type=int)
    result = calendly_service.list_scheduled_events(user_uri, count)
    if "error" in result:
        return jsonify(result), 500
    return jsonify(result)

@app.route('/api/v1/calendly', methods=['POST'])
@require_api_key
def calendly_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)

    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # For now, "execute" on Calendly just returns user info and event types as context
        user_info = calendly_service.get_user_info()
        event_types = calendly_service.list_event_types()

        context = f"Calendly User Info: {user_info}\nCalendly Event Types: {event_types}"
        message = google_ai.provide_calendly_assistance(f"Context: {context}\n\nUser Question: {prompt}")
        return jsonify({"status": "success", "message": message})

    message = google_ai.provide_calendly_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/business/excel', methods=['POST'])
@require_api_key
def business_excel_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)

    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        excel_data = google_ai.generate_excel_data(prompt)
        result = office_service.generate_excel(excel_data)
        if result['status'] == 'success':
            # Log the generated file
            new_file = File(
                user_id=g.user.id,
                filename=result['filename'],
                file_type='excel',
                filepath=result['filepath']
            )
            db.session.add(new_file)
            db.session.commit()
            return jsonify({"status": "success", "message": _("Excel file generated successfully."), "file_id": new_file.id, "filename": new_file.filename})
        return jsonify({"error": result.get('message')}), 500

    message = google_ai.provide_excel_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/business/word', methods=['POST'])
@require_api_key
def business_word_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)

    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        doc_info = google_ai.generate_word_content(prompt)
        result = office_service.generate_word(doc_info.get('paragraphs', []), doc_info.get('title', 'Document'))
        if result['status'] == 'success':
            new_file = File(
                user_id=g.user.id,
                filename=result['filename'],
                file_type='word',
                filepath=result['filepath']
            )
            db.session.add(new_file)
            db.session.commit()
            return jsonify({"status": "success", "message": _("Word document generated successfully."), "file_id": new_file.id, "filename": new_file.filename})
        return jsonify({"error": result.get('message')}), 500

    message = google_ai.provide_word_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/business/powerpoint', methods=['POST'])
@require_api_key
def business_powerpoint_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)

    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        pptx_info = google_ai.generate_pptx_data(prompt)
        result = office_service.generate_powerpoint(pptx_info.get('slides', []), pptx_info.get('title', 'Presentation'))
        if result['status'] == 'success':
            new_file = File(
                user_id=g.user.id,
                filename=result['filename'],
                file_type='powerpoint',
                filepath=result['filepath']
            )
            db.session.add(new_file)
            db.session.commit()
            return jsonify({"status": "success", "message": _("PowerPoint presentation generated successfully."), "file_id": new_file.id, "filename": new_file.filename})
        return jsonify({"error": result.get('message')}), 500

    message = google_ai.provide_powerpoint_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/gaming/monetization', methods=['POST'])
@require_api_key
def gaming_monetization_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_gaming_monetization_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/os/kernel', methods=['POST'])
@require_api_key
def os_kernel_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # Simulate kernel-level status check
        status = os_service.get_system_status()
        return jsonify({"status": "success", "message": f"Kernel Status: {json.dumps(status)}"})

    message = google_ai.provide_os_kernel_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/os/fs', methods=['POST'])
@require_api_key
def os_fs_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # Use AI to extract FS command (simplified)
        fs_cmd = google_ai.extract_json(google_ai.provide_os_fs_assistance(f"EXTRACT_JSON: {prompt}"))
        action = fs_cmd.get('action')
        path = fs_cmd.get('path')
        content = fs_cmd.get('content', "")

        if action == "write":
            res = os_service.fs.write_file(path, content)
        elif action == "read":
            res = os_service.fs.read_file(path)
        elif action == "list":
            res = str(os_service.fs.list_files(path or "/"))
        else:
            res = "Invalid FS action requested."

        return jsonify({"status": "success", "message": res})

    message = google_ai.provide_os_fs_assistance(prompt)
    return jsonify({"status": "success", "message": message})

@app.route('/api/v1/os/process', methods=['POST'])
@require_api_key
def os_process_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        proc_cmd = google_ai.extract_json(google_ai.provide_os_process_assistance(f"EXTRACT_JSON: {prompt}"))
        action = proc_cmd.get('action')
        name = proc_cmd.get('name')
        pid = proc_cmd.get('pid')

        if action == "spawn":
            res = f"Spawned with PID: {os_service.proc_mgr.spawn_process(name)}"
        elif action == "list":
            res = json.dumps(os_service.proc_mgr.list_processes())
        elif action == "kill":
            res = os_service.proc_mgr.kill_process(int(pid))
        else:
            res = "Invalid Process action requested."

        return jsonify({"status": "success", "message": res})

    message = google_ai.provide_os_process_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/os/dhcp', methods=['POST'])
@require_api_key
def os_dhcp_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        dhcp_cmd = google_ai.extract_json(google_ai.provide_os_dhcp_assistance(f"EXTRACT_JSON: {prompt}"))
        action = dhcp_cmd.get('action')
        mac = dhcp_cmd.get('mac')
        hostname = dhcp_cmd.get('hostname')
        requested_ip = dhcp_cmd.get('requested_ip')
        start_ip = dhcp_cmd.get('start_ip')
        end_ip = dhcp_cmd.get('end_ip')
        subnet_mask = dhcp_cmd.get('subnet_mask')
        gateway = dhcp_cmd.get('gateway')
        dns = dhcp_cmd.get('dns')
        lease_duration = dhcp_cmd.get('lease_duration')

        if action == "allocate":
            if not mac or not hostname:
                res = "Error: MAC address and hostname are required for lease allocation."
            else:
                try:
                    res = json.dumps(os_service.dhcp_server.allocate_lease(mac, hostname, requested_ip))
                except Exception as e:
                    res = str(e)
        elif action == "release":
            if not mac:
                res = "Error: MAC address is required for lease release."
            else:
                res = os_service.dhcp_server.release_lease(mac)
        elif action == "list":
            res = json.dumps(os_service.dhcp_server.list_leases())
        elif action == "get_config":
            res = json.dumps(os_service.dhcp_server.get_config())
        elif action == "configure":
            res = os_service.dhcp_server.configure(start_ip, end_ip, subnet_mask, gateway, dns, lease_duration)
        else:
            res = "Invalid DHCP action requested."

        return jsonify({"status": "success", "message": res})

    message = google_ai.provide_os_dhcp_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/nuclear/assistance', methods=['POST'])
@require_api_key
def nuclear_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_nuclear_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/emergent/assistance', methods=['POST'])
@require_api_key
def emergent_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    model_name = data.get('model_name', 'gpt-4o')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        message = google_ai.generate_emergent_completion(prompt, model_name)
    else:
        message = google_ai.provide_emergent_assistance(prompt)

    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/support/devrev', methods=['POST'])
@require_api_key
def devrev_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # Generate structured data for DevRev
        work_data = google_ai.generate_devrev_work_data(prompt)
        if not work_data or 'title' not in work_data:
            return jsonify({"error": _("Could not generate valid DevRev work data from prompt")}), 400

        applies_to_part = data.get('applies_to_part')
        result = devrev_service.create_work(
            work_data['title'],
            work_data.get('body', ''),
            work_data.get('type', 'ticket'),
            applies_to_part
        )

        if 'error' in result:
            return jsonify({"error": _("DevRev Execution Error: %(error)s", error=result['error'])}), 400

        message = _("Successfully executed DevRev action: %(type)s '%(title)s' created.",
                    type=work_data.get('type', 'ticket').capitalize(), title=work_data['title'])
        return jsonify({"status": "success", "message": message, "work": result['work']})

    message = google_ai.provide_devrev_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/ecommerce/shopline/assistance', methods=['POST'])
@require_api_key
def shopline_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # Generate structured data for Shopline
        product_data = google_ai.generate_shopline_product_data(prompt)
        if not product_data or 'title' not in product_data:
            return jsonify({"error": _("Could not generate valid Shopline product data from prompt")}), 400

        result = shopline_service.create_product(
            product_data['title'],
            product_data.get('body_html'),
            product_data.get('vendor'),
            product_data.get('product_type'),
            product_data.get('price')
        )

        if 'error' in result:
            return jsonify({"error": _("Shopline Execution Error: %(error)s", error=result['error'])}), 400

        message = _("Successfully executed Shopline action: Product '%(title)s' created.", title=product_data['title'])
        return jsonify({"status": "success", "message": message, "product": result['product']})

    message = google_ai.provide_shopline_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/support/zendesk', methods=['POST'])
@require_api_key
def zendesk_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        # Generate structured data for Zendesk
        ticket_data = google_ai.generate_zendesk_ticket_data(prompt)
        if not ticket_data or 'subject' not in ticket_data or 'comment_body' not in ticket_data:
            return jsonify({"error": _("Could not generate valid Zendesk ticket data from prompt")}), 400

        result = zendesk_service.create_ticket(
            ticket_data['subject'],
            ticket_data['comment_body'],
            ticket_data.get('requester_name'),
            ticket_data.get('requester_email')
        )

        if 'error' in result:
            return jsonify({"error": _("Zendesk Execution Error: %(error)s", error=result['error'])}), 400

        message = _("Successfully executed Zendesk action: Ticket '%(subject)s' created.", subject=ticket_data['subject'])
        return jsonify({"status": "success", "message": message, "ticket": result['ticket']})

    message = google_ai.provide_zendesk_assistance(prompt)
    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/perplexity/assistance', methods=['POST'])
@require_api_key
def perplexity_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    execute = data.get('execute', False)
    model_name = data.get('model_name', 'sonar-pro')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400

    if execute:
        message = google_ai.generate_perplexity_completion(prompt, model_name)
    else:
        message = google_ai.provide_perplexity_assistance(prompt)

    return jsonify({"status": "success", "message": message})


@app.route('/api/v1/psychoanalysis/assistance', methods=['POST'])
@require_api_key
def psychoanalysis_assistance_endpoint():
    data = request.get_json()
    prompt = data.get('prompt')
    if not prompt:
        return jsonify({"error": _("Prompt is required")}), 400
    message = google_ai.provide_psychoanalysis_assistance(prompt)
    return jsonify({"status": "success", "message": message})


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
        if 'credits' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN credits INTEGER DEFAULT 1000")
        if 'earnings' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN earnings FLOAT DEFAULT 0.0")
        if 'stripe_customer_id' not in columns:
            cursor.execute("ALTER TABLE user ADD COLUMN stripe_customer_id VARCHAR(120)")

        # Check for payment table
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='payment'")
        if cursor.fetchone():
            cursor.execute("PRAGMA table_info(payment)")
            payment_columns = [column[1] for column in cursor.fetchall()]
            if 'paystack_reference' not in payment_columns:
                cursor.execute("ALTER TABLE payment ADD COLUMN paystack_reference VARCHAR(120)")
            if 'flutterwave_tx_ref' not in payment_columns:
                cursor.execute("ALTER TABLE payment ADD COLUMN flutterwave_tx_ref VARCHAR(120)")

        # Create agent table if it doesn't exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agent'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE agent (
                    id INTEGER PRIMARY KEY,
                    developer_id INTEGER NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    description VARCHAR(500) NOT NULL,
                    endpoint_url VARCHAR(200) NOT NULL,
                    price_per_use INTEGER DEFAULT 50,
                    category VARCHAR(50) DEFAULT 'General',
                    is_active BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(developer_id) REFERENCES user(id)
                )
            """)

        # Create design table if it doesn't exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='design'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE design (
                    id INTEGER PRIMARY KEY,
                    developer_id INTEGER NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    description VARCHAR(500) NOT NULL,
                    preview_url VARCHAR(200),
                    price INTEGER DEFAULT 500,
                    category VARCHAR(50) DEFAULT 'Web',
                    content TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(developer_id) REFERENCES user(id)
                )
            """)

        # Create purchase table if it doesn't exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='purchase'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE purchase (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    item_type VARCHAR(20) NOT NULL,
                    item_id INTEGER NOT NULL,
                    amount INTEGER NOT NULL,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES user(id)
                )
            """)

        # Create file table if it doesn't exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='file'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE file (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    filename VARCHAR(200) NOT NULL,
                    file_type VARCHAR(50) NOT NULL,
                    content TEXT,
                    filepath VARCHAR(500),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES user(id)
                )
            """)

        # Create activity_log table if it doesn't exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='activity_log'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE activity_log (
                    id INTEGER PRIMARY KEY,
                    user_id INTEGER,
                    action VARCHAR(100) NOT NULL,
                    details VARCHAR(500),
                    ip_address VARCHAR(45),
                    user_agent VARCHAR(200),
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES user(id)
                )
            """)

        # Create training_data table if it doesn't exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='training_data'")
        if not cursor.fetchone():
            cursor.execute("""
                CREATE TABLE training_data (
                    id INTEGER PRIMARY KEY,
                    prompt TEXT NOT NULL,
                    completion TEXT NOT NULL,
                    category VARCHAR(50) DEFAULT 'General',
                    is_public BOOLEAN DEFAULT 1,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
                )
            """)

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

    if not TrainingData.query.first():
        sample_data = [
            TrainingData(prompt="How do I harden a Linux kernel?", completion="To harden a Linux kernel, you should enable features like KSPP, use specialized security modules (SELinux/AppArmor), and apply patches like Grsecurity if possible...", category="Security"),
            TrainingData(prompt="Write a simple smart contract in Solidity.", completion="pragma solidity ^0.8.0;\n\ncontract SimpleStorage {\n    uint256 public data;\n    function set(uint256 _data) public { data = _data; }\n}", category="Blockchain"),
            TrainingData(prompt="Translate 'Hello World' to Fon.", completion="In Fon (Togo/Benin), 'Hello World' can be translated as 'Kùabo xɛ lɔ'.", category="Language")
        ]
        db.session.bulk_save_objects(sample_data)
        db.session.commit()

    print("Database initialized.")
