from app.create_app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(500), nullable=False)
    role = db.Column(db.String(10), nullable=False)

    def __repr__(self):
        return f'<User {self.email}>'

class KnowledgeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<KnowledgeBase {self.title}>'