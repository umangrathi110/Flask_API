# sample data
from app import app
from models import db, User, Contact
import random

def sample_data():
    with app.app_context():
        user = User(name='abc def', phone='2345687654', email='abcdef@example.com', password='Abcdef@123')
        db.session.add(user)
        db.session.commit()

        contacts = [Contact(name=f'Contact {i}', phone=f'{random.randint(1000000000, 9999999999)}', owner=user) for i in range(10)]
        db.session.add_all(contacts)
        db.session.commit()

if __name__ == "__main__":
    sample_data()
