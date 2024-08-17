from flask import request, jsonify
from flask_restful import Resource
from models import SuperAdmin, Admin, Resident, News, Event, Neighborhood, Contact, Activity, db
from datetime import datetime
from flask import Flask
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

#Setting configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///neighborhood.db'
db.init_app(app)

class UserLoginResource(Resource):
    def post(self):
        data = request.json
        email = data.get('email')
        # Logic to check if email exists in Resident, Admin, or SuperAdmin table and authenticate
        # Return appropriate response
        return jsonify({"message": "User logged in successfully"})


class SuperAdminAdminResource(Resource):
    def get(self, super_admin_id):
        super_admin = SuperAdmin.query.get_or_404(super_admin_id)
        admins = Admin.query.all()
        return jsonify([admin.to_dict() for admin in admins])

    def post(self, super_admin_id):
        super_admin = SuperAdmin.query.get_or_404(super_admin_id)
        data = request.json
        new_admin = Admin(
            name=data['name'],
            email=data['email'],
            url=data['url'],
            neighborhood_id=data['neighborhood_id']
        )
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
        new_neighborhood = Neighborhood(
            name=data['name'],
            location=data['location'],
            image_url=data['image_url']
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
 


class AdminResidentsResource(Resource):
    def get(self, admin_id):
        admin = Admin.query.get_or_404(admin_id)
        residents = Resident.query.filter_by(neighborhood_id=admin.neighborhood_id).all()
        return jsonify([resident.to_dict() for resident in residents])

    def post(self, admin_id):
        admin = Admin.query.get_or_404(admin_id)
        data = request.json
        new_resident = Resident(
            name=data['name'],
            email=data['email'],
            house_number=data['house_number'],
            neighborhood_id=admin.neighborhood_id
        )
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
        new_news = News(
            title=data['title'],
            description=data['description'],
            neighborhood_id=admin.neighborhood_id,
            date_created=datetime.utcnow()
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


class AdminEventsResource(Resource):
    def get(self, admin_id):
        admin = Admin.query.get_or_404(admin_id)
        events = Event.query.filter_by(neighborhood_id=admin.neighborhood_id).all()
        return jsonify([event.to_dict() for event in events])

    def post(self, admin_id):
        admin = Admin.query.get_or_404(admin_id)
        data = request.json
        new_event = Event(
            title=data['title'],
            description=data['description'],
            neighborhood_id=admin.neighborhood_id,
            date_created=datetime.utcnow()
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201

class AdminEventResource(Resource):
    def put(self, admin_id, event_id):
        admin = Admin.query.get_or_404(admin_id)
        event = Event.query.get_or_404(event_id)
        data = request.json
        event.title = data['title']
        event.description = data['description']
        db.session.commit()
        return jsonify(event.to_dict())

    def delete(self, admin_id, event_id):
        admin = Admin.query.get_or_404(admin_id)
        event = Event.query.get_or_404(event_id)
        if event.neighborhood_id != admin.neighborhood_id:
            return {"error": "Unauthorized"}, 403
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted"}


class ResidentEventsResource(Resource):
    def get(self, resident_id):
        resident = Resident.query.get_or_404(resident_id)
        events = Event.query.filter_by(neighborhood_id=resident.neighborhood_id).all()
        return jsonify([event.to_dict() for event in events])

    def post(self, resident_id):
        resident = Resident.query.get_or_404(resident_id)
        data = request.json
        new_event = Event(
            title=data['title'],
            description=data['description'],
            neighborhood_id=resident.neighborhood_id,
            date_created=datetime.utcnow()
        )
        db.session.add(new_event)
        db.session.commit()
        return jsonify(new_event.to_dict()), 201

    def delete(self, resident_id, event_id):
        resident = Resident.query.get_or_404(resident_id)
        event = Event.query.get_or_404(event_id)
        if event.neighborhood_id != resident.neighborhood_id:
            return {"error": "Unauthorized"}, 403
        db.session.delete(event)
        db.session.commit()
        return {"message": "Event deleted"}


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
        new_news = News(
            title=data['title'],
            description=data['description'],
            date_created=datetime.utcnow()
        )
        db.session.add(new_news)
        db.session.commit()
        return jsonify(new_news.to_dict()), 201

class ContactResource(Resource):
    def post(self):
        data = request.json
        new_contact = Contact(
            name=data['name'],
            email=data['email'],
            subject=data['subject'],
            description=data['description']
        )
        db.session.add(new_contact)
        db.session.commit()
        return jsonify(new_contact.to_dict()), 201

class SuperAdminContactResource(Resource):
    def get(self, super_admin_id):
        super_admin = SuperAdmin.query.get_or_404(super_admin_id)
        contacts = Contact.query.all()
        return jsonify([contact.to_dict() for contact in contacts])

class ActivityResource(Resource):
    def get(self):
        activities = Activity.query.all()
        return jsonify([activity.to_dict() for activity in activities])

# Admin routes
api.add_resource(AdminResidentsResource, '/admin/<int:admin_id>/residents')
api.add_resource(AdminResidentResource, '/admin/<int:admin_id>/residents/<int:resident_id>')
api.add_resource(AdminNewsResource, '/admin/<int:admin_id>/news/<int:news_id>')

# SuperAdmin routes
api.add_resource(SuperAdminAdminResource, '/superadmin/<int:super_admin_id>/admins')
api.add_resource(SuperAdminNeighborhoodResource, '/superadmin/<int:super_admin_id>/neighborhoods')

# News routes
api.add_resource(NewsResource, '/news/<int:news_id>')
api.add_resource(NewsListResource, '/news')

# User routes
api.add_resource(UserLoginResource, '/login')

# Admin routes
api.add_resource(AdminEventsResource, '/admin/<int:admin_id>/events')
api.add_resource(AdminEventResource, '/admin/<int:admin_id>/events/<int:event_id>')

# Resident routes
api.add_resource(ResidentEventsResource, '/resident/<int:resident_id>/events')

# Contact routes
api.add_resource(ContactResource, '/contact')
api.add_resource(SuperAdminContactResource, '/superadmin/<int:super_admin_id>/contacts')

# Activity routes
api.add_resource(ActivityResource, '/activities')

if __name__ == '__main__':
    app.run(debug=True)