from faker import Faker
from app import app
from models import db, SuperAdmin, Admin, Resident, Neighborhood, Activity, News, Contact
import cloudinary.uploader

with app.app_context():
    fake = Faker()

    # Delete all records/rows in the tables

    db.session.query(SuperAdmin).delete()
    db.session.query(Admin).delete()
    db.session.query(Resident).delete()
    db.session.query(Neighborhood).delete()
    db.session.query(Activity).delete()
    db.session.query(News).delete()
    db.session.commit()

   
    # Empty lists for each table

    superadmins = []
    admins = []
    residents = []
    neighborhoods = []
    activities = []
    news = []

def seed_residents(num=10):
    for _ in range(num):
        resident = Resident(
            name=fake.name(),
            email=fake.email(),
            house_number=fake.building_number(),
            neighborhood_id=fake.random_int(min=1, max=5),
            profile_image_url=fake.image_url()
        )
        resident.set_password(fake.password())
        db.session.add(resident)
    db.session.commit()

def seed_admins(num=5):
    for _ in range(num):
        admin = Admin(
            name=fake.name(),
            email=fake.email(),
            neighborhood_id=fake.random_int(min=1, max=5),
            profile_image_url=fake.image_url()
        )
        admin.set_password(fake.password())
        db.session.add(admin)
    db.session.commit()

def seed_superadmins(num=2):
    for _ in range(num):
        superadmin = SuperAdmin(
            name=fake.name(),
            email=fake.email(),
            profile_image_url=fake.image_url()
        )
        superadmin.set_password(fake.password())
        db.session.add(superadmin)
    db.session.commit()

def seed_news(num=10):
    for _ in range(num):
        news = News(
            title=fake.sentence(nb_words=5),
            description=fake.text(),
            image_url=fake.image_url()
        )
        db.session.add(news)
    db.session.commit()

def seed_neighborhoods(num=5):
    for _ in range(num):
        neighborhood = Neighborhood(
            name=fake.word(),
            location=fake.address(),
            image_url=fake.image_url()
        )
        db.session.add(neighborhood)
    db.session.commit()

def seed_contacts(num=10):
    for _ in range(num):
        contact = Contact(
            name=fake.name(),
            email=fake.email(),
            subject=fake.sentence(nb_words=3),
            description=fake.text()
        )
        db.session.add(contact)
    db.session.commit()

if __name__ == '__main__':
    from app import app
    with app.app_context():
        db.create_all()
        seed_residents()
        seed_admins()
        seed_superadmins()
        seed_news()
        seed_neighborhoods()
        seed_contacts()
        print("Database seeded successfully.")

    