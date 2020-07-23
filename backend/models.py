from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

'''
Question

'''


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    category_id = db.Column(
        db.ForeignKey("categories.id"),
        nullable=False
    )

    question = db.Column(
        db.String,
        nullable=False
    )

    answer = db.Column(
        db.String,
        nullable=False
    )

    difficulty = db.Column(
        db.Integer,
        nullable=False
    )

    def __init__(self, question, answer, category_id, difficulty):
        self.question = question
        self.answer = answer
        self.category_id = category_id
        self.difficulty = difficulty

    def add(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'question': self.question,
            'answer': self.answer,
            'category': self.category.format(),
            'difficulty': self.difficulty
        }


'''
Category

'''


class Category(db.Model):
    __tablename__ = 'categories'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    type = db.Column(
        db.String,
        nullable=False
    )

    questions = db.relationship(
        "Question",
        lazy="dynamic",
        backref="category"
    )

    def __init__(self, type):
        self.type = type

    def format(self):
        return {
            'id': self.id,
            'type': self.type
        }
