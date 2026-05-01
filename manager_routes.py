from flask import Blueprint
from models import User
from utils import token_required, role_required, get_html_template

manager_bp = Blueprint('manager', __name__)

@manager_bp.route('/manager')
@token_required
@role_required('Manager')
def manager_page(user):
    # Fetch ONLY normal users from database
    normal_users = User.query.filter_by(role='User').all()
    
    # Generate Simplified Table HTML
    table_html = "<table><tr><th>Name</th><th>Account Type</th></tr>"
    for u in normal_users:
        table_html += f"<tr><td>{u.name}</td><td>{u.role}</td></tr>"
    table_html += "</table>"
    
    return get_html_template(
        "Manager Zone", 
        f"Welcome Manager <b>{user.name}</b>. You have access to view standard users only.", 
        "#f59e0b", 
        table_html
    )