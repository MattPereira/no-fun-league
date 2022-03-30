from models import db, User, Pick, Roster, Manager, Post, Proposal, ProposalVotes, Player
from app import app
import requests
import json

LEAGUE_ID = 723677559673409536

DRAFT_ID = 723677560327737344


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

# ADD ALL THE ROSTERS DATA FOR LEAGUE

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

# ADD ALL THE DRAFT DATA FOR SPECIFIC 2021 DRAFT

draft_data = requests.get(
    f'https://api.sleeper.app/v1/draft/{DRAFT_ID}/picks').json()

for pick in draft_data:
    p = Pick(roster_id=pick['roster_id'], player_id=pick['metadata']['player_id'], picked_by=pick['picked_by'],
             first_name=pick['metadata']['first_name'], last_name=pick['metadata']['last_name'], position=pick['metadata']['position'], team=pick['metadata']['team'], amount=pick['metadata']['amount'])
    db.session.add(p)
    db.session.commit()


# Input myself first so I can display an initial blog post and create the first poll
matt = User.register(sleeper_id='724424250483650560', first_name='Matt',
                     last_name='Pereira', email="ramchips99@gmail.com", password='eclipse21')


db.session.add(matt)
db.session.commit()


# Create first blog post welcoming the managers
post = Post(user_id=1, title="Welcome to the Managers",
            para_1="Allow me to introduce everyone to the official No Fun League website. To begin, you can create your user account by registering. You must choose your sleeper account name from the select input, and then provide a name, email, and password. You will then be automatically logged in and redirected to your manager profile page where you are free to customize the content to your liking. Next, you may want to peruse the roster pages or take a gander at the results of the 2021 draft.",
            para_2="Another feature I would like to highlight is the polls page where you can propose amendments to the No Fun League constitution. After submitting, all members of the league who are registered and logged in will have the ability to vote on your proposition. Please note that, unlike a blog post, the contents of a rule change proposal cannot be edited or deleted.",
            para_3="Since the site is still very much a work in progress, please do not hesitate to reach out if you encounter any bugs or would like to suggest ideas for some new features.")

db.session.add(post)
db.session.commit()

# Create the first few rule change proposals
prop1 = Proposal(user_id=1, ammendment="Reinstate kickers as a legitimate fantasy position",
                 argument="Kickers are fantasy players too. They should not be discrimated against. The game of fantasy football should be celebrated in its entirety!")

prop2 = Proposal(user_id=1, ammendment="Change QB2 starting roster position to a super flex where any position may be started",
                 argument="This rule change is a pivotal step in allowing for the league to expand from 10 managers to 12. More managers means more prize money. Also, it feels real bad when you dont have a second QB to start on your roster. ")
db.session.add_all([prop1, prop2])
db.session.commit()


########## Add some votes on the propposals ##############
v1 = ProposalVotes(proposal_id=1, user_id=1, agree=True)
v2 = ProposalVotes(proposal_id=2, user_id=1, agree=True)

db.session.add_all([v1, v2])
db.session.commit()


### ADDS ALL THE PLAYERS WHO HAVE AN ID ON SOME ROSTER TO PLAYER TABLE ####
## ONLY ALLOWED TO CALL PLAYERS REQ FROM SLEEPER API ONCE PER DAY ##
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
