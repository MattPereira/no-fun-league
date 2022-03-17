from models import db, User
from app import app

# Create all tables

db.drop_all()
db.create_all()


matt = User.register(user_id='724424250483650560', first_name='Matt',
                     last_name='Pereira', email="ramchips99@gmail.com", password='eclipse21')

brad = User.register(user_id='470093099188613120', first_name='Brad',
                     last_name='Johnson', email="bJohnson@gmail.com", password='eclipse21')

jake = User.register(user_id='723670786174451712', first_name='Jake',
                     last_name='Dame', email="jakeD@gmail.com", password='eclipse21')

lemon = User.register(user_id='723692755766849536', first_name='Chris',
                      last_name='Hall', email="cHall@gmail.com", password='eclipse21')

mikey = User.register(user_id='725910594263265280', first_name='Mikey',
                      last_name='idk', email="mikey@gmail.com", password='eclipse21')

michael = User.register(user_id='723694715693821952', first_name='Michael',
                        last_name='Meyer', email="mmeyer@gmail.com", password='eclipse21')

chris = User.register(user_id='725808119531286528', first_name='Chris',
                      last_name='Thomas', email="cThomas@gmail.com", password='eclipse21')

kaelin = User.register(user_id='469946665449549824', first_name='Kaelin',
                       last_name='Ragan', email="kRagan@gmail.com", password='eclipse21')

brett = User.register(user_id='725777513267126272', first_name='Brett',
                      last_name='Psomething', email="brettP@gmail.com", password='eclipse21')

grant = User.register(user_id='469964078912106496', first_name='Grant',
                      last_name='idk', email="grant@gmail.com", password='eclipse21')


db.session.add_all([matt, brad, lemon, jake, mikey,
                   michael, chris, kaelin, brett, grant])
db.session.commit()
