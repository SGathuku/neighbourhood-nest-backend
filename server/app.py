from flask import request, jsonify
from flask_restful import Resource
from models import Admin, Resident, News, Event, db

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
