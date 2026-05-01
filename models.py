from flask_sqlalchemy import SQLAlchemy

# Initialize the database extension
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    # User can register with email or username as per the assignment requirements
    email_or_username = db.Column(db.String(100), unique=True, nullable=False)
    hashed_password = db.Column(db.String(255), nullable=False)
    # Roles can be Admin, Manager, or User
    role = db.Column(db.String(20), nullable=False, default='User')
    # Stores the 2FA secret key for each user
    two_factor_secret = db.Column(db.String(32), nullable=True) 

    def __repr__(self):
        return f"<User {self.email_or_username} - Role: {self.role}>"
