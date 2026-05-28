from flask import Blueprint, request, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from urllib.parse import urlparse
import httpx
import asyncio

# Note: We assume 'db' and 'User' will be available via the app context or passed in.
# For simplicity in this refactor, we will import them from app.py but carefully.

marketplace_bp = Blueprint('marketplace', __name__)

def get_db():
    from app import db
    return db

def get_user_model():
    from app import User
    return User

import ipaddress
import socket

def is_safe_url(url):
    """Enhanced SSRF protection for developer-provided endpoints."""
    try:
        parsed = urlparse(url)
        if parsed.scheme not in ['http', 'https']:
            return False

        hostname = parsed.hostname.lower()
        if not hostname:
            return False

        # Block literal IP addresses that are private/internal
        try:
            ip = ipaddress.ip_address(hostname)
            if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast:
                return False
        except ValueError:
            # Not an IP literal, resolve DNS
            try:
                # Note: In a production env, use a custom resolver to prevent DNS rebinding
                ip_addr = socket.gethostbyname(hostname)
                ip = ipaddress.ip_address(ip_addr)
                if ip.is_private or ip.is_loopback or ip.is_link_local or ip.is_multicast:
                    return False
            except:
                return False

        # Explicit block list for known sensitive hostnames
        if hostname in ['localhost', 'metadata.google.internal', '169.254.169.254']:
            return False

        return True
    except:
        return False

# Models (moved from app.py to here)
from database import db

class Agent(db.Model):
    __bind_key__ = None # Use default
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    api_endpoint = db.Column(db.String(200), nullable=False)
    api_key = db.Column(db.String(120), nullable=True)
    price = db.Column(db.Integer, default=50)
    icon = db.Column(db.String(50), default='Bot')
    is_approved = db.Column(db.Boolean, default=False)
    # developer relationship will be handled via backref in User or defined here

    def to_dict(self):
        from app import User
        dev = User.query.get(self.developer_id)
        return {
            "id": self.id,
            "name": self.name,
            "category": self.category,
            "description": self.description,
            "price": self.price,
            "icon": self.icon,
            "developer": dev.username if dev else "Unknown"
        }

class Design(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    developer_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    preview_url = db.Column(db.String(200), nullable=True)
    file_url = db.Column(db.String(200), nullable=True)
    price = db.Column(db.Integer, default=100)
    is_approved = db.Column(db.Boolean, default=False)

    def to_dict(self):
        from app import User
        dev = User.query.get(self.developer_id)
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "preview_url": self.preview_url,
            "developer": dev.username if dev else "Unknown"
        }

# Routes
from app import require_api_key, _

@marketplace_bp.route('/agents', methods=['POST'])
@require_api_key
def create_agent():
    from app import db
    data = request.get_json()
    name = data.get('name')
    category = data.get('category')
    description = data.get('description')
    api_endpoint = data.get('api_endpoint')
    api_key = data.get('api_key')
    price = data.get('price', 50)
    icon = data.get('icon', 'Bot')

    if not all([name, category, description, api_endpoint]):
        return jsonify({"error": _("Missing required fields")}), 400

    new_agent = Agent(
        developer_id=g.user.id,
        name=name,
        category=category,
        description=description,
        api_endpoint=api_endpoint,
        api_key=api_key,
        price=price,
        icon=icon,
        is_approved=True # Auto-approving for demo purposes
    )
    db.session.add(new_agent)
    db.session.commit()
    return jsonify({"status": "success", "agent": {"id": new_agent.id, "name": new_agent.name}})

@marketplace_bp.route('/agents', methods=['GET'])
def list_agents():
    agents = Agent.query.filter_by(is_approved=True).all()
    return jsonify([a.to_dict() for a in agents])

@marketplace_bp.route('/agents/<int:agent_id>/execute', methods=['POST'])
@require_api_key
async def execute_agent(agent_id):
    from app import db, User
    agent = Agent.query.get_or_404(agent_id)
    if not agent.is_approved:
         return jsonify({"error": _("Agent not approved")}), 403

    if not is_safe_url(agent.api_endpoint):
        return jsonify({"error": _("Invalid or unsafe API endpoint")}), 400

    if g.user.credits < agent.price:
        return jsonify({"error": _("Insufficient credits")}), 402

    data = request.get_json()
    prompt = data.get('prompt')

    try:
        headers = {}
        if agent.api_key:
            headers['Authorization'] = f'Bearer {agent.api_key}'
            headers['X-API-Key'] = agent.api_key

        async with httpx.AsyncClient() as client:
            response = await client.post(agent.api_endpoint, json={"prompt": prompt}, headers=headers, timeout=60)
            response.raise_for_status()
            agent_response = response.json()

            g.user.credits -= agent.price
            developer = User.query.get(agent.developer_id)
            developer.earnings += int(agent.price * 0.8)
            db.session.commit()

            return jsonify({
                "status": "success",
                "message": agent_response.get('message') or agent_response.get('response') or str(agent_response)
            })
    except Exception as e:
        return jsonify({"error": f"Agent Execution Error: {str(e)}"}), 500

@marketplace_bp.route('/designs', methods=['POST'])
@require_api_key
def create_design():
    from app import db
    data = request.get_json()
    name = data.get('name')
    description = data.get('description')
    preview_url = data.get('preview_url')
    file_url = data.get('file_url')
    price = data.get('price', 100)

    if not all([name, description, file_url]):
        return jsonify({"error": _("Missing required fields")}), 400

    new_design = Design(
        developer_id=g.user.id,
        name=name,
        description=description,
        preview_url=preview_url,
        file_url=file_url,
        price=price,
        is_approved=True # Auto-approving for demo purposes
    )
    db.session.add(new_design)
    db.session.commit()
    return jsonify({"status": "success", "design": {"id": new_design.id, "name": new_design.name}})

@marketplace_bp.route('/designs', methods=['GET'])
def list_designs():
    designs = Design.query.filter_by(is_approved=True).all()
    return jsonify([d.to_dict() for d in designs])

@marketplace_bp.route('/designs/<int:design_id>/purchase', methods=['POST'])
@require_api_key
def purchase_design(design_id):
    from app import db, User
    design = Design.query.get_or_404(design_id)
    if not design.is_approved:
         return jsonify({"error": _("Design not approved")}), 403

    if g.user.credits < design.price:
        return jsonify({"error": _("Insufficient credits")}), 402

    g.user.credits -= design.price
    developer = User.query.get(design.developer_id)
    developer.earnings += int(design.price * 0.8)
    db.session.commit()

    return jsonify({
        "status": "success",
        "message": _("Design purchased successfully"),
        "file_url": design.file_url
    })
