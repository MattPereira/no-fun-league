from models import db, User, Pick, Roster, Manager, Post, Proposal, ProposalVotes, Player
from app import app
import requests
import json

LEAGUE_ID = 723677559673409536

DRAFT_ID = 723677560327737344

# Create all tables


#### how to handle creation of tables in deployment??? ####
db.drop_all()
db.create_all()


# ADDS ALL THE MANAGERS INFO
managers_info = requests.get(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users").json()

for manager in managers_info:
    m = Manager(sleeper_id=manager['user_id'], display_name=manager['display_name'],
                avatar_id=manager['avatar'], team_name=manager['metadata']['team_name'])
    db.session.add(m)
    db.session.commit()

# # Input all the users. Special attention to provide correct user_id
# matt = User.register(sleeper_id='724424250483650560', first_name='Matt',
#                      last_name='Pereira', email="ramchips99@gmail.com", password='eclipse21')

# brad = User.register(sleeper_id='470093099188613120', first_name='Brad',
#                      last_name='Johnson', email="bJohnson@gmail.com", password='eclipse21')

# jake = User.register(sleeper_id='723670786174451712', first_name='Jake',
#                      last_name='Dame', email="jakeD@gmail.com", password='eclipse21')

# lemon = User.register(sleeper_id='723692755766849536', first_name='Chris',
#                       last_name='Hall', email="cHall@gmail.com", password='eclipse21')

# mikey = User.register(sleeper_id='725910594263265280', first_name='Mikey',
#                       last_name='unknown', email="mikey@gmail.com", password='eclipse21')

# michael = User.register(sleeper_id='723694715693821952', first_name='Michael',
#                         last_name='Meyer', email="mmeyer@gmail.com", password='eclipse21')

# chris = User.register(sleeper_id='725808119531286528', first_name='Chris',
#                       last_name='Thomas', email="cThomas@gmail.com", password='eclipse21')

# kaelin = User.register(sleeper_id='469946665449549824', first_name='Kaelin',
#                        last_name='Ragan', email="kRagan@gmail.com", password='eclipse21')

# brett = User.register(sleeper_id='725777513267126272', first_name='Brett',
#                       last_name='Psomething', email="brettP@gmail.com", password='eclipse21')

# grant = User.register(sleeper_id='469964078912106496', first_name='Grant',
#                       last_name='idk', email="grant@gmail.com", password='eclipse21')


# db.session.add_all([matt, brad, lemon, jake])
# db.session.commit()


######## Add some rule proposals for testing ############
# prop1 = Proposal(user_id=4, ammendment="Reinstate kickers as a real fantasy position",
#                  argument="Kickers are fantasy player too. They should not be discrimated against. They should be celebrated!")

# prop2 = Proposal(user_id=2, ammendment="Change QB2 starting roster position to a super flex instead",
#                  argument="This rule change will allow for the league to expand from 10 managers to 12. More managers means more prize money. Also, it feels bad when you dont have a second QB to start on your roster. ")
# db.session.add_all([prop1, prop2])
# db.session.commit()


########## Add some votes on the propposals ##############
# v1 = ProposalVotes(proposal_id=1, user_id=1, agree=True)
# v2 = ProposalVotes(proposal_id=1, user_id=2, agree=True)
# v3 = ProposalVotes(proposal_id=1, user_id=3, agree=True)
# v4 = ProposalVotes(proposal_id=1, user_id=4, agree=True)
# v5 = ProposalVotes(proposal_id=1, user_id=5, agree=False)
# v6 = ProposalVotes(proposal_id=1, user_id=6, agree=False)
# v7 = ProposalVotes(proposal_id=2, user_id=1, agree=False)
# v8 = ProposalVotes(proposal_id=2, user_id=2, agree=False)
# v9 = ProposalVotes(proposal_id=2, user_id=3, agree=False)
# v10 = ProposalVotes(proposal_id=2, user_id=4, agree=True)
# v11 = ProposalVotes(proposal_id=1, user_id=7, agree=True)
# v12 = ProposalVotes(proposal_id=1, user_id=8, agree=True)
# v13 = ProposalVotes(proposal_id=1, user_id=9, agree=True)
# db.session.add_all([v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13])
# db.session.commit()


# ADDS ALL THE ROSTERS DATA FOR LEAGUE

rosters_data = requests.get(
    f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters").json()


for roster in rosters_data:
    r = Roster(
        id=roster['roster_id'],
        owner_id=roster['owner_id'],
        wins=roster['settings']['wins'],
        losses=roster['settings']['losses'],
        ppts=roster['settings']['ppts'],
        fpts=roster['settings']['fpts'],
        fpts_against=roster['settings']['fpts_against'],
        streak=roster['metadata']['streak'],
        record=roster['metadata']['record'],
        player_ids=roster['players'])

    db.session.add(r)
    db.session.commit()

# ADDS ALL THE DRAFT DATA FOR SPECIFIC 2021 DRAFT

draft_data = requests.get(
    f'https://api.sleeper.app/v1/draft/{DRAFT_ID}/picks').json()

for pick in draft_data:
    p = Pick(roster_id=pick['roster_id'], player_id=pick['metadata']['player_id'], picked_by=pick['picked_by'],
             first_name=pick['metadata']['first_name'], last_name=pick['metadata']['last_name'], position=pick['metadata']['position'], team=pick['metadata']['team'], amount=pick['metadata']['amount'])
    db.session.add(p)
    db.session.commit()


### ADDS ALL THE PLAYERS WHO HAVE AN ID ON SOME ROSTER TO PLAYER TABLE ####
## ONLY ALLOWED TO CALL PLAYERS REQ ONCE PER DAY ##
# players = requests.get("https://api.sleeper.app/v1/players/nfl") #
f = open('players.json', 'r')

players = json.loads(f.read())

rosters = Roster.query.all()

# TARGET ONLY THE PLAYERS THAT ARE PRESENT IN OUR LEAGUE #
all_p_ids = []
for roster in rosters:
    for id in roster.player_ids:
        all_p_ids.append(id)

for player in players.values():
    if player['player_id'] in all_p_ids:
        p = Player(id=player.get('player_id'), last_name=player.get('last_name'), full_name=player.get('full_name'),
                   position=player.get('position'), team=player.get('team'), age=player.get('age'), height=player.get('height'))

        db.session.add(p)
        db.session.commit()
