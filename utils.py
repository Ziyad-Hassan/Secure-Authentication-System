from flask import request, current_app
import jwt
from functools import wraps
from models import User

def get_html_template(title, message, color="#3b82f6", extra_html=""):
    return f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{title}</title>
        <style>
            body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #0f172a; color: #f8fafc; display: flex; justify-content: center; align-items: center; min-height: 100vh; margin: 0; padding: 20px; }}
            .card {{ background: #1e293b; padding: 40px; border-radius: 20px; box-shadow: 0 15px 35px rgba(0,0,0,0.5); max-width: 650px; width: 100%; border-top: 5px solid {color}; text-align: center; border: 1px solid #334155; border-top: 5px solid {color}; }}
            h1 {{ color: #f8fafc; margin-top: 0; font-size: 26px; }}
            p {{ color: #94a3b8; font-size: 16px; line-height: 1.6; margin-bottom: 25px; }}
            .btn {{ display: inline-block; padding: 12px 25px; background: {color}; color: white; text-decoration: none; border-radius: 10px; font-weight: 600; transition: background 0.3s, transform 0.2s; box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3); }}
            .btn:hover {{ opacity: 0.9; transform: translateY(-2px); }}
            
            /* Dark Theme Table */
            table {{ width: 100%; border-collapse: collapse; margin-bottom: 25px; text-align: left; font-size: 14px; background: #0f172a; border-radius: 10px; overflow: hidden; }}
            th, td {{ padding: 12px 15px; border-bottom: 1px solid #334155; }}
            th {{ background-color: #020617; color: #cbd5e1; font-weight: 700; text-transform: uppercase; font-size: 12px; letter-spacing: 1px; }}
            tr:hover {{ background-color: #1e293b; }}
            td {{ color: #e2e8f0; }}
        </style>
    </head>
    <body>
        <div class="card">
            <h1>{title}</h1>
            <p>{message}</p>
            {extra_html}
            <br>
            <a href="/dashboard" class="btn">Back to Dashboard</a>
        </div>
    </body>
    </html>
    """

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.cookies.get('token')
        if not token:
            return get_html_template("401 Unauthorized", "Please <a href='/login' style='color:#60a5fa;'>login</a> first.", "#ef4444"), 401
        try:
            data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=['HS256'])
            user = User.query.get(data['user_id'])
        except:
            return get_html_template("401 Session Expired", "Please <a href='/login' style='color:#60a5fa;'>login again</a>.", "#ef4444"), 401
        return f(user, *args, **kwargs)
    return decorated

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated(user, *args, **kwargs):
            if user.role != role:
                return get_html_template("403 Forbidden", f"Blocked! Access restricted to <b style='color:#ef4444;'>{role}</b> only.<br>You are logged in as <b>{user.role}</b>.", "#ef4444"), 403
            return f(user, *args, **kwargs)
        return decorated
    return decorator