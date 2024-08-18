from flask import Flask, make_response, request, jsonify
from flask_restful import Api, Resource
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
import cloudinary.uploader
from datetime import datetime
from models import db, SuperAdmin, Admin, Resident, Neighborhood, News, Contact, Event
from flask_migrate import Migrate
from flask_cors import CORS

import cloudinary
import cloudinary.uploader
import cloudinary.api

# Initialize the app and extensions
app = Flask(__name__)
api = Api(app)

# Configure app
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neighborhood.db'
app.config['JWT_SECRET_KEY'] = '#1@2##' 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False # Change this to a random secret key

db.init_app(app)
jwt = JWTManager(app)
migrate = Migrate(app, db)

CORS(app) # Allow requests from all origins

cloudinary.config(
    cloud_name='dypwsrolf',
    api_key='339349293184484',
    api_secret='zcplKelqPs1MV4wfptQaPXAYgq4'
)

# Authentication endpoint
class LoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        password = data.get('password')

        if not email or not password:
            return {"error": "Email and password required"}, 400

        user = SuperAdmin.query.filter_by(email=email).first() or \
               Admin.query.filter_by(email=email).first() or \
               Resident.query.filter_by(email=email).first()

        if not user or not user.check_password(password):
            return {"error": "Invalid credentials"}, 401

        access_token = create_access_token(identity={'id': user.id, 'type': user.__class__.__name__, 'role': user.role.name})
        return jsonify(access_token=access_token, role=user.role.name)

# Example: Protecting admin routes
class AdminResidentsResource(Resource):
    @jwt_required()
    def get(self, admin_id):
        identity = get_jwt_identity()
        if identity['type'] != 'Admin':
            return {"error": "Unauthorized"}, 403

        admin = Admin.query.get_or_404(admin_id)
        residents = Resident.query.filter_by(neighborhood_id=admin.neighborhood_id).all()
        return jsonify([resident.to_dict() for resident in residents])

    @jwt_required()
    def post(self, admin_id):
        identity = get_jwt_identity()
        if identity['type'] != 'Admin':
            return {"error": "Unauthorized"}, 403

        admin = Admin.query.get_or_404(admin_id)
        data = request.json
        profile_image = request.files.get('profile_image')

        profile_image_url = None
        if profile_image:
            upload_result = cloudinary.uploader.upload(profile_image)
            profile_image_url = upload_result['url']

        new_resident = Resident(
            name=data['name'],
            email=data['email'],
            house_number=data['house_number'],
            neighborhood_id=admin.neighborhood_id,
            profile_image_url=profile_image_url,
            role_id=data['role_id']
        )
        new_resident.set_password(data['password'])

        db.session.add(new_resident)
        db.session.commit()
        return jsonify(new_resident.to_dict()), 201

class AdminResidentResource(Resource):
    def delete(self, admin_id, resident_id):
        admin = Admin.query.get_or_404(admin_id)
        resident = Resident.query.get_or_404(resident_id)
        if resident.neighborhood_id != admin.neighborhood_id:
            return {"error": "Unauthorized"}, 403
        db.session.delete(resident)
        db.session.commit()
        return {"message": "Resident deleted"}

class AdminNewsResource(Resource):
    def post(self, admin_id):
        admin = Admin.query.get_or_404(admin_id)
        data = request.json
        image = request.files.get('image')

        image_url = None
        if image:
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result['url']

        new_news = News(
            title=data['title'],
            description=data['description'],
            neighborhood_id=admin.neighborhood_id,
            date_created=datetime.utcnow(),
            image_url=image_url
        )
        db.session.add(new_news)
        db.session.commit()
        return jsonify(new_news.to_dict()), 201

    def delete(self, admin_id, news_id):
        admin = Admin.query.get_or_404(admin_id)
        news = News.query.get_or_404(news_id)
        if news.neighborhood_id != admin.neighborhood_id:
            return {"error": "Unauthorized"}, 403
        db.session.delete(news)
        db.session.commit()
        return {"message": "News deleted"}

# Example: SuperAdmins managing news
class SuperAdminNewsResource(Resource):
    @jwt_required()
    def get(self, superadmin_id):
        identity = get_jwt_identity()
        if identity['type'] != 'SuperAdmin':
            return {"error": "Unauthorized"}, 403

        superadmin = SuperAdmin.query.get_or_404(superadmin_id)
        news = News.query.all()
        return jsonify([news_item.to_dict() for news_item in news])

    @jwt_required()
    def post(self, superadmin_id):
        identity = get_jwt_identity()
        if identity['type'] != 'SuperAdmin':
            return {"error": "Unauthorized"}, 403

        superadmin = SuperAdmin.query.get_or_404(superadmin_id)
        data = request.json
        news_item = News(
            title=data['title'],
            content=data['content'],
            created_at=datetime.utcnow()
        )
        db.session.add(news_item)
        db.session.commit()
        return jsonify(news_item.to_dict()), 201

class SuperAdminNeighborhoodResource(Resource):
    def post(self, super_admin_id):
        super_admin = SuperAdmin.query.get_or_404(super_admin_id)
        data = request.json
        image = request.files.get('image')

        image_url = None
        if image:
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result['url']

        new_neighborhood = Neighborhood(
            name=data['name'],
            location=data['location'],
            image_url=image_url
        )
        db.session.add(new_neighborhood)
        db.session.commit()
        return jsonify(new_neighborhood.to_dict()), 201

    def delete(self, super_admin_id, neighborhood_id):
        super_admin = SuperAdmin.query.get_or_404(super_admin_id)
        neighborhood = Neighborhood.query.get_or_404(neighborhood_id)
        db.session.delete(neighborhood)
        db.session.commit()
        return {"message": "Neighborhood deleted"}

# Example: Resident managing their profile
class ResidentProfileResource(Resource):
    @jwt_required()
    def get(self):
        identity = get_jwt_identity()
        if identity['type'] != 'Resident':
            return {"error": "Unauthorized"}, 403

        resident = Resident.query.get_or_404(identity['id'])
        return jsonify(resident.to_dict())

    @jwt_required()
    def put(self):
        identity = get_jwt_identity()
        if identity['type'] != 'Resident':
            return {"error": "Unauthorized"}, 403

        resident = Resident.query.get_or_404(identity['id'])
        data = request.json
        resident.name = data.get('name', resident.name)
        resident.house_number = data.get('house_number', resident.house_number)
        db.session.commit()
        return jsonify(resident.to_dict())



class NewsResource(Resource):
    def get(self, news_id):
        news = News.query.get_or_404(news_id)
        return jsonify(news.to_dict())

    def put(self, news_id):
        news = News.query.get_or_404(news_id)
        data = request.json
        news.title = data['title']
        news.description = data['description']
        db.session.commit()
        return jsonify(news.to_dict())

    def delete(self, news_id):
        news = News.query.get_or_404(news_id)
        db.session.delete(news)
        db.session.commit()
        return {"message": "News deleted"}

class NewsListResource(Resource):
    def get(self):
        news_list = News.query.all()
        return jsonify([news.to_dict() for news in news_list])

    def post(self):
        data = request.json
        image = request.files.get('image')

        image_url = None
        if image:
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result['url']

        new_news = News(
            title=data['title'],
            description=data['description'],
            date_created=datetime.utcnow(),
            image_url=image_url
        )
        db.session.add(new_news)
        db.session.commit()
        return jsonify(new_news.to_dict()), 201

class EventResource(Resource):
    def get(self, event_id):
        event = Event.query.get_or_404(event_id)
        return jsonify(event.to_dict())

    def post(self):
        data = request.json
        image = request.files.get('image')

        image_url = None
        if image:
            upload_result = cloudinary.uploader.upload(image)
            image_url = upload_result['url']

        new_event = Event(
            title=data['title'],
            description=data['description'],
            date_created=datetime.utcnow(),
            image_url=image_url
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201

    def delete(self, event_id):
        event = Event.query.get_or_404(event_id)
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted"}

# Add resources to the API
api.add_resource(LoginResource, '/api/login')
api.add_resource(AdminResidentsResource, '/api/admin/<int:admin_id>/residents')
api.add_resource(AdminResidentResource, '/api/admin/<int:admin_id>/residents/<int:resident_id>')
api.add_resource(AdminNewsResource, '/api/admin/<int:admin_id>/news')
api.add_resource(SuperAdminNewsResource, '/api/superadmin/<int:superadmin_id>/news')
api.add_resource(ResidentProfileResource, '/api/resident/profile')
api.add_resource(NewsResource, '/api/news/<int:news_id>')
api.add_resource(NewsListResource, '/api/news')
api.add_resource(EventResource, '/api/events/<int:event_id>')

if __name__ == '__main__':
    app.run(debug=True)
