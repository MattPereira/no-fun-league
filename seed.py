from models import db, User, Pick, Roster, Manager, Post
from app import app
import requests

LEAGUE_ID = 723677559673409536

# Create all tables

db.drop_all()
db.create_all()

# # Input all the users. Special attention to provide correct user_id
matt = User.register(sleeper_id='724424250483650560', first_name='Matt',
                     last_name='Pereira', email="ramchips99@gmail.com", password='eclipse21')

brad = User.register(sleeper_id='470093099188613120', first_name='Brad',
                     last_name='Johnson', email="bJohnson@gmail.com", password='eclipse21')

jake = User.register(sleeper_id='723670786174451712', first_name='Jake',
                     last_name='Dame', email="jakeD@gmail.com", password='eclipse21')

lemon = User.register(sleeper_id='723692755766849536', first_name='Chris',
                      last_name='Hall', email="cHall@gmail.com", password='eclipse21')

mikey = User.register(sleeper_id='725910594263265280', first_name='Mikey',
                      last_name='unknown', email="mikey@gmail.com", password='eclipse21')

michael = User.register(sleeper_id='723694715693821952', first_name='Michael',
                        last_name='Meyer', email="mmeyer@gmail.com", password='eclipse21')

chris = User.register(sleeper_id='725808119531286528', first_name='Chris',
                      last_name='Thomas', email="cThomas@gmail.com", password='eclipse21')

kaelin = User.register(sleeper_id='469946665449549824', first_name='Kaelin',
                       last_name='Ragan', email="kRagan@gmail.com", password='eclipse21')

brett = User.register(sleeper_id='725777513267126272', first_name='Brett',
                      last_name='Psomething', email="brettP@gmail.com", password='eclipse21')

grant = User.register(sleeper_id='469964078912106496', first_name='Grant',
                      last_name='idk', email="grant@gmail.com", password='eclipse21')


db.session.add_all([matt, brad, lemon, jake, mikey,
                   michael, chris, kaelin, brett, grant])
db.session.commit()

###### Add some posts for testing ########
p1 = Post(user_id=1, title="Welcome to the managers", content="Greetings No Fun League managers! Welcome to our new site. Initially, I am hoping we will be able to use this site to manage our voting process for new rule proposals. Eventually, many useful features may be added since a few of our league managers are/ will eventually become professional software engineers. Thanks.")

p2 = Post(user_id=2, title="Test post from another user",
          content="We are testing posting functionality here")
db.session.add_all([p1, p2])
db.session.commit()


# ADDS ALL THE MANAGERS INFO
managers_info = requests.get(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users").json()

for manager in managers_info:
    m = Manager(user_id=manager['user_id'], display_name=manager['display_name'],
                avatar_id=manager['avatar'], team_name=manager['metadata']['team_name'])
    db.session.add(m)
    db.session.commit()


# ADDS ALL THE ROSTERS DATA FOR LEAGUE
rosters_data = requests.get(
    "https://api.sleeper.app/v1/league/723677559673409536/rosters").json()


for roster in rosters_data:
    r = Roster(id=roster['roster_id'], owner_id=roster['owner_id'], wins=roster['settings']['wins'], losses=roster['settings']
               ['losses'], ppts=roster['settings']['ppts'], fpts=roster['settings']['fpts'], fpts_against=roster['settings']['fpts_against'], streak=roster['metadata']['streak'], record=roster['metadata']['record'], players=roster['players'])

    db.session.add(r)
    db.session.commit()


# ADDS ALL THE DRAFT DATA FOR SPECIFIC 2021 DRAFT
draft_data = requests.get(
    'https://api.sleeper.app/v1/draft/723677560327737344/picks').json()

for pick in draft_data:
    p = Pick(roster_id=pick['roster_id'], draft_id=pick['draft_id'], picked_by=pick['picked_by'],
             first_name=pick['metadata']['first_name'], last_name=pick['metadata']['last_name'], position=pick['metadata']['position'], team=pick['metadata']['team'], amount=pick['metadata']['amount'])
    db.session.add(p)
    db.session.commit()
