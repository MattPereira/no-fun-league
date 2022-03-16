from models import db, User
from app import app

# Create all tables

db.drop_all()
db.create_all()


matt = User.register(username='ramchips', pwd='eclipse21',
                     first_name='Matt', last_name='Pereira', email="ramchips99@gmail.com")

brad = User.register(username='baretank', pwd='eclipse21',
                     first_name='Brad', last_name='Johnson', email="bjohnson@gmail.com")


lemon = User.register(username='Lemonnn', pwd='eclipse21',
                      first_name='Chris', last_name='Hall', email="lemon@gmail.com")

jake = User.register(username='Truffles29', pwd='eclipse21',
                     first_name='Jake', last_name='unknown', email="jake@gmail.com")


db.session.add_all([matt, brad, lemon, jake])
db.session.commit()
