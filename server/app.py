from flask import request, jsonify
from flask_restful import Resource
from models import SuperAdmin, Admin, Resident, News, Event, Neighborhood, db

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
