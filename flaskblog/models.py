from flaskblog import db, login_manger
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Date


@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model,  UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(20), nullable=False)
    image_file = db.Column(db.String(20), nullable=False,
                           default='default.jpg')
    post = db.relationship('Post', backref='author', lazy=True)
    questions = db.relationship(
        'Questions', backref='questions_author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}','{self.date_posted}')"


class Questionstype(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    type = db.Column(db.String(300), nullable=False)

    questions = db.relationship(
        'Questions', backref='questions_type', lazy=True)

    def __repr__(self):
        return f"QuestionsType('{self.id}','{self.type}')"


class Questionspaper(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_paper_title = db.Column(db.String(300), nullable=False)
    question_size = db.Column(db.Integer, nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)

    questions = db.relationship(
        'Questions', backref='questions_paper', lazy=True)

    def __repr__(self):
        return f"QuestionsPaper('{self.question_paper}','{self.question_id}','{self.date_created}')"


class Questions(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_title = db.Column(db.String(300), nullable=False)
    correct_answer = db.Column(db.String(300), nullable=False)
    date_created = db.Column(
        db.DateTime, nullable=False, default=datetime.utcnow)
    question_paper_id = db.Column(db.Integer, db.ForeignKey(
        'questionspaper.id'), nullable=False)
    question_type = db.Column(db.Integer, db.ForeignKey(
        'questionstype.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Questions('{self.id}','{self.question_title}','{self.correct_answer}', '{self.question_type}')"
