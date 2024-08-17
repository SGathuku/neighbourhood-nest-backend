from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from sqlalchemy_serializer import SerializerMixin
# from sqlalchemy.orm import validates
from datetime import datetime
import re

metadata = MetaData()

db = SQLAlchemy(metadata=metadata)


class Resident(db.Model, SerializerMixin):
    __tablename__ = 'residents'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    house_number = db.Column(db.String(50))
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.id'), nullable=False)
    profile_image_url = db.Column(db.String(255))  # URL for profile picture

    neighborhood = db.relationship('Neighborhood', back_populates='residents')
    activities = db.relationship('Activity', back_populates='resident')

    def __repr__(self):
        return f"<Resident {self.name} (ID: {self.id}, Email: {self.email})>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(255))  # URL for profile picture
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.id'), nullable=False)
    profile_image_url = db.Column(db.String(255))  # URL for profile picture

    neighborhood = db.relationship('Neighborhood', back_populates='admins')

    def __repr__(self):
        return f"<Admin {self.name} (ID: {self.id}, Email: {self.email})>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class SuperAdmin(db.Model, SerializerMixin):
    __tablename__ = 'superadmins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(255))  # URL for profile picture
    profile_image_url = db.Column(db.String(255))  # URL for profile picture

    def __repr__(self):
        return f"<SuperAdmin {self.name} (ID: {self.id}, Email: {self.email})>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class News(db.Model, SerializerMixin):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(255))  # URL for news image

    def __repr__(self):
        return f"<News {self.title} (ID: {self.id}, Created: {self.date_created})>"

class Neighborhood(db.Model, SerializerMixin):
    __tablename__ = 'neighborhoods'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    image_url = db.Column(db.String(255))  # URL for neighborhood image

    residents = db.relationship('Resident', back_populates='neighborhood')
    admins = db.relationship('Admin', back_populates='neighborhood')

    def __repr__(self):
        return f"<Neighborhood {self.name} (ID: {self.id}, Location: {self.location})>"

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.id'))
    event_id = db.Column(db.Integer)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('residents.id'))

    resident = db.relationship('Resident', foreign_keys=[resident_id], back_populates='activities')
    user = db.relationship('Resident', foreign_keys=[user_id])

    def __repr__(self):
        return f"<Activity (ID: {self.id}, Resident ID: {self.resident_id}, Event ID: {self.event_id})>"

class Contact(db.Model, SerializerMixin):
    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_submitted = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Contact {self.subject} (ID: {self.id}, Email: {self.email})>"