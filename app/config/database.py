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

class UserQueryHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    query = db.Column(db.String(500), nullable=False)
    response = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    user = db.relationship('User', backref=db.backref('query_history', lazy=True))

    def __repr__(self):
        return f'<UserQueryHistory {self.query}>'

class NeuralNetworkSettings(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(255), nullable=False)
    api_key = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f'<NeuralNetworkSettings {self.model}>'

class VectorizedKnowledgeBase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    content = db.Column(db.Text, nullable=False)
    vector = db.Column(db.ARRAY(db.Float), nullable=False)  # Векторное представление

    def __repr__(self):
        return f'<VectorizedKnowledgeBase {self.title}>'