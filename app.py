from flask import Flask, render_template
from models import db
from auth import auth_bp
from admin_routes import admin_bp
from manager_routes import manager_bp
from user_routes import user_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secure-alexandria-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///secure_auth.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

# Register all Blueprints
app.register_blueprint(auth_bp, url_prefix='/api')
app.register_blueprint(admin_bp)
app.register_blueprint(manager_bp)
app.register_blueprint(user_bp)

# Main Authentication Routes
@app.route('/login')
def login_view(): return render_template('login.html')

@app.route('/')
@app.route('/register')
def register_view(): return render_template('register.html')

with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)