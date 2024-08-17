from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy_serializer import SerializerMixin
import cloudinary.uploader
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
    password = db.Column(db.String(128), nullable=False)
    house_number = db.Column(db.String(50))
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.id'), nullable=False)
    profile_image_url = db.Column(db.String(255))  # URL for profile picture

    neighborhood = db.relationship('Neighborhood', back_populates='residents')
    activities = db.relationship('Activity', back_populates='resident', foreign_keys='Activity.resident_id')
    def __repr__(self):
        return f"<Resident {self.name} (ID: {self.id}, Email: {self.email})>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'house_number': self.house_number,
            'neighborhood_id': self.neighborhood_id,
            'profile_image_url': self.profile_image_url
        }

class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(255))  # URL for profile picture
    neighborhood_id = db.Column(db.Integer, db.ForeignKey('neighborhoods.id'), nullable=False)
    profile_image_url = db.Column(db.String(255))  # URL for profile picture

    neighborhood = db.relationship('Neighborhood', back_populates='admins')

    def __repr__(self):
        return f"<Admin {self.name} (ID: {self.id}, Email: {self.email})>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'url': self.url,
            'profile_image_url': self.profile_image_url
        }

class SuperAdmin(db.Model, SerializerMixin):
    __tablename__ = 'superadmins'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    url = db.Column(db.String(255))  # URL for profile picture
    profile_image_url = db.Column(db.String(255))  # URL for profile picture

    def __repr__(self):
        return f"<SuperAdmin {self.name} (ID: {self.id}, Email: {self.email})>"

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'url': self.url,
            'profile_image_url': self.profile_image_url
        }

class News(db.Model, SerializerMixin):
    __tablename__ = 'news'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    image_url = db.Column(db.String(255))  # URL for news image

    def __repr__(self):
        return f"<News {self.title} (ID: {self.id}, Created: {self.date_created})>"

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'image_url': self.image_url
        }

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'location': self.location,
            'image_url': self.image_url
        }

class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'
    id = db.Column(db.Integer, primary_key=True)
    resident_id = db.Column(db.Integer, db.ForeignKey('residents.id'))
    event_id = db.Column(db.Integer)
    news_id = db.Column(db.Integer, db.ForeignKey('news.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('residents.id'))

    resident = db.relationship('Resident', back_populates='activities', foreign_keys=[resident_id])
    user = db.relationship('Resident', foreign_keys=[user_id])

    def __repr__(self):
        return f"<Activity (ID: {self.id}, Resident ID: {self.resident_id}, Event ID: {self.event_id})>"

    def to_dict(self):
        return {
            'id': self.id,
            'resident_id': self.resident_id,
            'event_id': self.event_id,
            'news_id': self.news_id,
            'user_id': self.user_id
        }

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
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subject': self.subject,
            'description': self.description,
            'date_submitted': self.date_submitted
        }
    
class Event(db.Model, SerializerMixin):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.String(255))  # URL for event image

    def __repr__(self):
        return f"<Event {self.name} (ID: {self.id}, Date: {self.date})>"

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'date': self.date,
            'image_url': self.image_url
        }
    