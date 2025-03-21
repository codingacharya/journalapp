from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
import uuid

db = SQLAlchemy()

# User Roles
ROLES = {'admin': 'Admin', 'author': 'Author', 'reviewer': 'Reviewer'}

# User Model
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='author')
    articles = db.relationship('Article', backref='author', lazy=True)

# Journal Article Model
class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), nullable=False)
    abstract = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    doi = db.Column(db.String(100), unique=True, default=lambda: str(uuid.uuid4()))
    status = db.Column(db.String(50), nullable=False, default='Pending')  # Pending, Approved, Rejected

    def generate_citation(self):
        return f"{self.author.username}, '{self.title}', DOI: {self.doi}"
