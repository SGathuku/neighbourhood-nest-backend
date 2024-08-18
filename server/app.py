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

        access_token = create_access_token(identity={'id': user.id, 'type': user.__class__.__name__})
        return jsonify(access_token=access_token)

class AdminResidentsResource(Resource):
    def get(self, admin_id):
        admin = Admin.query.get_or_404(admin_id)
        residents = Resident.query.filter_by(neighborhood_id=admin.neighborhood_id).all()
        return jsonify([resident.to_dict() for resident in residents])

    def post(self, admin_id):
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
            profile_image_url=profile_image_url
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

class SuperAdminAdminResource(Resource):
    def get(self, super_admin_id):
        super_admin = SuperAdmin.query.get_or_404(super_admin_id)
        admins = Admin.query.all()
        return jsonify([admin.to_dict() for admin in admins])

    def post(self, super_admin_id):
        super_admin = SuperAdmin.query.get_or_404(super_admin_id)
        data = request.json
        profile_image = request.files.get('profile_image')

        profile_image_url = None
        if profile_image:
            upload_result = cloudinary.uploader.upload(profile_image)
            profile_image_url = upload_result['url']

        new_admin = Admin(
            name=data['name'],
            email=data['email'],
            url=data['url'],
            neighborhood_id=data['neighborhood_id'],
            profile_image_url=profile_image_url
        )
        new_admin.set_password(data['password'])

        db.session.add(new_admin)
        db.session.commit()
        return jsonify(new_admin.to_dict()), 201

    def delete(self, super_admin_id, admin_id):
        super_admin = SuperAdmin.query.get_or_404(super_admin_id)
        admin = Admin.query.get_or_404(admin_id)
        db.session.delete(admin)
        db.session.commit()
        return {"message": "Admin deleted"}

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
            neighborhood_id=data['neighborhood_id'],
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

class ContactResource(Resource):
    def post(self):
        data = request.json
        new_contact = Contact(
            name=data['name'],
            email=data['email'],
            message=data['message']
        )
        db.session.add(new_contact)
        db.session.commit()
        return {"message": "Contact message submitted"}, 201

    def get(self):
        contacts = Contact.query.all()
        return jsonify([contact.to_dict() for contact in contacts])

# Add resources to the API
api.add_resource(LoginResource, '/login')
api.add_resource(AdminResidentsResource, '/admin/<int:admin_id>/residents')
api.add_resource(AdminResidentResource, '/admin/<int:admin_id>/residents/<int:resident_id>')
api.add_resource(AdminNewsResource, '/admin/<int:admin_id>/news')
api.add_resource(SuperAdminAdminResource, '/superadmin/<int:super_admin_id>/admins')
api.add_resource(SuperAdminNeighborhoodResource, '/superadmin/<int:super_admin_id>/neighborhoods')
api.add_resource(NewsResource, '/news/<int:news_id>')
api.add_resource(NewsListResource, '/news')
api.add_resource(EventResource, '/events/<int:event_id>')
api.add_resource(ContactResource, '/contacts')

if __name__ == '__main__':
    app.run(debug=True)