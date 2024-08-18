from faker import Faker
from datetime import datetime
from app import app
from models import db, Role, Resident, Admin, SuperAdmin, News, Neighborhood, Activity, Contact, Event
from werkzeug.security import generate_password_hash

def seed_all():
    with app.app_context():
        fake = Faker()

    # Delete all records/rows in the tables

    db.session.query(SuperAdmin).delete()
    db.session.query(Admin).delete()
    db.session.query(Resident).delete()
    db.session.query(Neighborhood).delete()
    db.session.query(Activity).delete()
    db.session.query(News).delete()
    db.session.query(Contact).delete()
    db.session.query(Event).delete()
    db.session.commit()

   
    # Empty lists for each table

    superadmins = []
    admins = []
    residents = []
    neighborhoods = []
    activities = []
    news = []
    contacts = []
    events = []

def seed_roles():
    roles = [
        {'name': 'Resident', 'description': 'Regular resident'},
        {'name': 'Admin', 'description': 'Admin of a neighborhood'},
        {'name': 'SuperAdmin', 'description': 'Super administrator with all permissions'},
    ]
    
    for role in roles:
        r = Role(name=role['name'], description=role['description'])
        db.session.add(r)
    db.session.commit()

def seed_neighborhoods():
    neighborhoods = [
        {'name': 'Green Valley', 'location': 'North Side'},
        {'name': 'Sunny Meadows', 'location': 'West End'},
        {'name': 'Ocean View', 'location': 'South Coast'},
    ]
    
    for neighborhood in neighborhoods:
        n = Neighborhood(name=neighborhood['name'], location=neighborhood['location'])
        db.session.add(n)
    db.session.commit()

def seed_residents():
    residents = [
        {'name': 'Sean Marquez', 'email': 'sean@example.com', 'password': 'password123', 'house_number': '451', 'neighborhood_id': 1, 'role_name': 'Resident', 'profile_image_url': 'https://placekitten.com/446/323'},
        {'name': 'Jane Doe', 'email': 'jane@example.com', 'password': 'password123', 'house_number': '12A', 'neighborhood_id': 2, 'role_name': 'Resident', 'profile_image_url': 'https://placekitten.com/445/322'},
    ]
    
    for resident in residents:
        role = Role.query.filter_by(name=resident['role_name']).first()
        r = Resident(
            name=resident['name'],
            email=resident['email'],
            password_hash=generate_password_hash(resident['password']),
            house_number=resident['house_number'],
            neighborhood_id=resident['neighborhood_id'],
            role_id=role.id,
            profile_image_url=resident['profile_image_url']
        )
        db.session.add(r)
    db.session.commit()

def seed_admins():
    admins = [
        {'name': 'Admin One', 'email': 'admin1@example.com', 'password': 'admin123', 'neighborhood_id': 1, 'role_name': 'Admin', 'profile_image_url': 'https://placekitten.com/450/320'},
    ]
    
    for admin in admins:
        role = Role.query.filter_by(name=admin['role_name']).first()
        a = Admin(
            name=admin['name'],
            email=admin['email'],
            password_hash=generate_password_hash(admin['password']),
            neighborhood_id=admin['neighborhood_id'],
            role_id=role.id,
            profile_image_url=admin['profile_image_url']
        )
        db.session.add(a)
    db.session.commit()

def seed_superadmins():
    superadmins = [
        {'name': 'Super Admin', 'email': 'superadmin@example.com', 'password': 'superadmin123', 'role_name': 'SuperAdmin', 'profile_image_url': 'https://placekitten.com/449/319'},
    ]
    
    for superadmin in superadmins:
        role = Role.query.filter_by(name=superadmin['role_name']).first()
        s = SuperAdmin(
            name=superadmin['name'],
            email=superadmin['email'],
            password_hash=generate_password_hash(superadmin['password']),
            role_id=role.id,
            profile_image_url=superadmin['profile_image_url']
        )
        db.session.add(s)
    db.session.commit()

def seed_news():
    news_items = [
        {'title': 'New Park Opening', 'description': 'A new park is opening in Green Valley.', 'image_url': 'https://placekitten.com/400/300'},
    ]
    
    for news in news_items:
        n = News(
            title=news['title'],
            description=news['description'],
            image_url=news['image_url']
        )
        db.session.add(n)
    db.session.commit()

def seed_events():
    events = [
        {'name': 'Community BBQ', 'description': 'Join us for a community BBQ.', 'date': datetime(2024, 9, 5), 'image_url': 'https://placekitten.com/401/301'},
    ]
    
    for event in events:
        e = Event(
            name=event['name'],
            description=event['description'],
            date=event['date'],
            image_url=event['image_url']
        )
        db.session.add(e)
    db.session.commit()

def seed_contacts():
    contacts = [
        {'name': 'John Smith', 'email': 'johnsmith@example.com', 'subject': 'Inquiry', 'description': 'I have a question about the neighborhood.'},
    ]
    
    for contact in contacts:
        c = Contact(
            name=contact['name'],
            email=contact['email'],
            subject=contact['subject'],
            description=contact['description']
        )
        db.session.add(c)
    db.session.commit()

def seed_all():
    seed_roles()
    seed_neighborhoods()
    seed_residents()
    seed_admins()
    seed_superadmins()
    seed_news()
    seed_events()
    seed_contacts()

if __name__ == '__main__':
    db.create_all()
    seed_all()