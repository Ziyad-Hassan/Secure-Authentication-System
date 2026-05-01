from flask import Blueprint
from models import User
from utils import token_required, role_required, get_html_template

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/admin')
@token_required
@role_required('Admin')
def admin_page(user):
    # Fetch ALL users from database
    all_users = User.query.all()
    total_users = len(all_users)
    
    # Generate Table HTML
    table_html = "<table><tr><th>ID</th><th>Name</th><th>Email/Username</th><th>Role</th></tr>"
    for u in all_users:
        table_html += f"<tr><td>{u.id}</td><td>{u.name}</td><td>{u.email_or_username}</td><td><b>{u.role}</b></td></tr>"
    table_html += "</table>"
    
    return get_html_template(
        "Admin Control Panel", 
        f"Welcome Admin <b>{user.name}</b>. System has a total of <b>{total_users}</b> registered users.", 
        "#ef4444", 
        table_html
    )