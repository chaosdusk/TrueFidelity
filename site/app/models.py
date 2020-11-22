from app import db, login
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean, default=False)
    # TODO: Might need to specify cascade delete if plan to enable user deletion
    labels = db.relationship('Label', backref='labeler', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Label(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # Index on timestamp might not be that useful
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    image_id = db.Column(db.Integer, db.ForeignKey('image.id'))
    is_correct = db.Column(db.Boolean, nullable=False)
    measurement = db.Column(db.Integer) # Chose Integer > Float or Numeric since no need for decimals

    def __repr__(self):
        return '<Label {}>'.format(self.timestamp)

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    batch_id = db.Column(db.Integer, db.ForeignKey('batch.id'))
    dose_reduction = db.Column(db.Float)
    reconstruction = db.Column(db.Float)
    attenuation = db.Column(db.String(128))
    lesion_size_mm = db.Column(db.Float)
    size_measurement = db.Column(db.Integer)
    filename = db.Column(db.String(64))
    labels = db.relationship('Label', backref='image', lazy='dynamic')

    def __repr__(self):
        return '<Image, id: {} dose: {} size: {}>'.format(self.id, self.dose_reduction, self.lesion_size_mm)

class Batch(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    description = db.Column(db.String(512))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

    images = db.relationship('Image', backref='batch', lazy='dynamic')

    def __repr__(self):
        return '<Batch: {}'.format(self.name)