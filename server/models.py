from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Camper(db.Model):
    __tablename__ = 'campers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    signups = db.relationship('Signup', backref='camper', cascade="all, delete-orphan")

    def __init__(self, name=None, age=None):
        if not name:
            raise ValueError("Camper must have a name")
        if age is None or not (8 <= age <= 18):
            raise ValueError("Age must be between 8 and 18")
        self.name = name
        self.age = age

    def to_dict(self, include_signups=False):
        data = {
            'id': self.id,
            'name': self.name,
            'age': self.age
        }
        if include_signups:
            data['signups'] = [s.to_dict(include_activity=True) for s in self.signups]
        return data


class Activity(db.Model):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    difficulty = db.Column(db.Integer, nullable=False)
    signups = db.relationship('Signup', backref='activity', cascade="all, delete-orphan")

    def __init__(self, name=None, difficulty=None):
        if not name:
            raise ValueError("Activity must have a name")
        try:
            difficulty = int(difficulty)
        except:
            raise ValueError("Difficulty must be an integer between 1 and 10")
        if not (1 <= difficulty <= 10):
            raise ValueError("Difficulty must be an integer between 1 and 10")
        self.name = name
        self.difficulty = difficulty

    def to_dict(self, include_signups=False):
        data = {
            'id': self.id,
            'name': self.name,
            'difficulty': self.difficulty
        }
        if include_signups:
            data['signups'] = [s.to_dict(include_camper=True) for s in self.signups]
        return data


class Signup(db.Model):
    __tablename__ = 'signups'
    id = db.Column(db.Integer, primary_key=True)
    time = db.Column(db.Integer, nullable=False)
    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'), nullable=False)
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'), nullable=False)

    def __init__(self, time=None, camper_id=None, activity_id=None):
        if time is None or not isinstance(time, int) or not (0 <= time <= 23):
            raise ValueError("Time must be an integer between 0 and 23")
        if camper_id is None:
            raise ValueError("camper_id is required")
        if activity_id is None:
            raise ValueError("activity_id is required")
        self.time = time
        self.camper_id = camper_id
        self.activity_id = activity_id

    def to_dict(self, include_camper=False, include_activity=False):
        data = {
            'id': self.id,
            'time': self.time,
            'camper_id': self.camper_id,
            'activity_id': self.activity_id
        }
        if include_camper and self.camper:
            data['camper'] = self.camper.to_dict()
        if include_activity and self.activity:
            data['activity'] = self.activity.to_dict()
        return data
