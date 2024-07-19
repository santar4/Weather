from app import app
from app.models import *


def mock_data():
    p1 = User(nickname='Max', email='mav@gmail.com', password= 'Zxcghoul' )

    db.session.add_all([p1])
    db.session.commit()
    print("mock data added")


with app.app_context():
    db.create_all()

    print("database created")
    mock_data()
