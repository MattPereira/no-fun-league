from models import db, User, Pick, Roster, Member
from app import app
import requests

LEAGUE_ID = 723677559673409536

# Create all tables

db.drop_all()
db.create_all()

# # Input all the users. Special attention to provide correct user_id
matt = User.register(id='724424250483650560', first_name='Matt',
                     last_name='Pereira', email="ramchips99@gmail.com", password='eclipse21')

brad = User.register(id='470093099188613120', first_name='Brad',
                     last_name='Johnson', email="bJohnson@gmail.com", password='eclipse21')

jake = User.register(id='723670786174451712', first_name='Jake',
                     last_name='Dame', email="jakeD@gmail.com", password='eclipse21')

lemon = User.register(id='723692755766849536', first_name='Chris',
                      last_name='Hall', email="cHall@gmail.com", password='eclipse21')

mikey = User.register(id='725910594263265280', first_name='Mikey',
                      last_name='unknown', email="mikey@gmail.com", password='eclipse21')

michael = User.register(id='723694715693821952', first_name='Michael',
                        last_name='Meyer', email="mmeyer@gmail.com", password='eclipse21')

chris = User.register(id='725808119531286528', first_name='Chris',
                      last_name='Thomas', email="cThomas@gmail.com", password='eclipse21')

kaelin = User.register(id='469946665449549824', first_name='Kaelin',
                       last_name='Ragan', email="kRagan@gmail.com", password='eclipse21')

brett = User.register(id='725777513267126272', first_name='Brett',
                      last_name='Psomething', email="brettP@gmail.com", password='eclipse21')

grant = User.register(id='469964078912106496', first_name='Grant',
                      last_name='idk', email="grant@gmail.com", password='eclipse21')


db.session.add_all([matt, brad, lemon, jake, mikey,
                   michael, chris, kaelin, brett, grant])
db.session.commit()


# ADDS ALL THE MEMBERS INFO
member_info = requests.get(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users").json()

for member in member_info:
    m = Member(user_id=member['user_id'], display_name=member['display_name'],
               avatar_id=member['avatar'], team_name=member['metadata']['team_name'])
    db.session.add(m)
    db.session.commit()


# ADDS ALL THE ROSTERS DATA FOR LEAGUE
rosters_data = requests.get(
    "https://api.sleeper.app/v1/league/723677559673409536/rosters").json()


for roster in rosters_data:
    r = Roster(id=roster['roster_id'], owner_id=roster['owner_id'], wins=roster['settings']['wins'], losses=roster['settings']
               ['losses'], fpts=roster['settings']['fpts'], fpts_against=roster['settings']['fpts_against'], streak=roster['metadata']['streak'], record=roster['metadata']['record'])

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
