from flask import Blueprint, render_template
from utils import token_required, role_required, get_html_template

user_bp = Blueprint('user_routes', __name__)

# Dashboard Route (Frontend)
@user_bp.route('/dashboard')
def dashboard_view(): 
    return render_template('dashboard.html')

# Personal Profile Route (Data from DB via JWT)
@user_bp.route('/profile')
@token_required
def profile(user):
    # Generate Profile Card HTML
    profile_html = f"""
    <div style='background: #f8fafc; padding: 20px; border-radius: 15px; border: 1px solid #e2e8f0; text-align: left; display: inline-block; width: 80%;'>
        <p style='margin-bottom: 10px;'><b>Full Name:</b> {user.name}</p>
        <p style='margin-bottom: 10px;'><b>Username:</b> {user.email_or_username}</p>
        <p style='margin-bottom: 10px;'><b>System Role:</b> {user.role}</p>
        <p style='margin-bottom: 0;'><b>Database ID:</b> #{user.id}</p>
    </div>
    """
    return get_html_template(
        "Personal Profile", 
        "Your secure personal data fetched directly from the database.", 
        "#3b82f6", 
        profile_html
    )

# Restricted User Zone
@user_bp.route('/user')
@token_required
@role_required('User')
def user_page(user):
    return get_html_template(
        "User Zone", 
        f"Authorized access granted. This is a restricted area for users.", 
        "#64748b"
    )