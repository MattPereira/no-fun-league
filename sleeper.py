from models import db, User, Pick, Roster, Manager, Post, Proposal, ProposalVotes, Player

import requests
import json

LEAGUE_ID = 723677559673409536

DRAFT_ID = 723677560327737344


def update_picks():
    draft_data = requests.get(
        f'https://api.sleeper.app/v1/draft/{DRAFT_ID}/picks').json()

    picks = Pick.query.all()

    pick_ids = [p.player_id for p in picks]

    for pick in draft_data:
        if pick['player_id'] in pick_ids:
            p = Pick.query.filter(Pick.player_id == pick['player_id'])
            p.team = pick['metadata']['team']
            p.amount = pick['metadata']['amount']
            db.session.commit()

        else:
            p = Pick(roster_id=pick['roster_id'], player_id=pick['metadata']['player_id'], picked_by=pick['picked_by'],
                     first_name=pick['metadata']['first_name'], last_name=pick['metadata']['last_name'], position=pick['metadata']['position'], team=pick['metadata']['team'], amount=pick['metadata']['amount'])
            db.session.add(p)
            db.session.commit()


def update_managers():
    managers_info = requests.get(
        f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/users").json()

    managers = Manager.query.all()

    man_ids = [m.sleeper_id for m in managers]

    # Sleeper api 'user_id' is what i call 'sleeper_id' in local db
    for manager in managers_info:
        # Check if manager is already in local db
        if manager['user_id'] in man_ids:
            m = Manager.query.filter(Manager.sleeper_id == manager['user_id'])
            m.display_name = manager['display_name']
            m.avatar_id = manager['avatar']
            m.team_name = manager['metadata']['team_name']
            db.session.commit()
        # Add manager if not in local db
        else:
            m = Manager(sleeper_id=manager['user_id'], display_name=manager['display_name'],
                        avatar_id=manager['avatar'], team_name=manager['metadata']['team_name'])
            db.session.add(m)
            db.session.commit()


def update_rosters():
    rosters_data = requests.get(
        f"https://api.sleeper.app/v1/league/{LEAGUE_ID}/rosters").json()

    rosters = Roster.query.all()

    owner_ids = [r.owner_id for r in rosters]

    for roster in rosters_data:
        # If the roster already exists in local db, update the info using sleeper api
        if roster['owner_id'] in owner_ids:
            r = Roster.query.filter(Roster.owner_id == roster['owner_id'])
            r.wins = roster['settings']['wins']
            r.losses = roster['settings']['losses']
            r.ppts = roster['settings']['ppts']
            r.fpts = roster['settings']['fpts']
            r.fpts_against = roster['settings']['fpts_against']
            r.streak = roster['metadata']['streak']
            r.record = roster['metadata']['record']
            r.player_ids = roster['players']
            db.session.commit()
        # If roster does not exist in local db, add it
        else:
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


def update_players():
    ### ONLY ALLOWED TO CALL PLAYERS ONCE PER DAY ###
    ### SUB THIS LINE IN BEFORE PRODUCTION ###
    # players = requests.get("https://api.sleeper.app/v1/players/nfl") #
    f = open('players.json', 'r')
    players = json.loads(f.read())

    ### SAVE ONLY PLAYERS PRESENT IN OUR LEAGUE TO LOCAL DB ###
    rosters = Roster.query.all()
    # GRAB ALL THE PLAYER IDS FROM EVERY ROSTER THAT IS IN LOCAL DB #
    all_p_ids = []
    for roster in rosters:
        for id in roster.player_ids:
            all_p_ids.append(id)

    ### GRAB ALL THE PLAYER IDS THAT EXIST IN LOCAL DB TO AVOID UNIQUE CONSTRAINT ERROR ###
    db_players = Player.query.all()
    db_p_ids = [p.id for p in db_players]

    for player in players.values():
        if player['player_id'] in all_p_ids:
            if player['player_id'] in db_p_ids:
                p = Player.query.filter(Player.id == player['player_id'])
                p.full_name = player.get('full_name')
                p.position = player.get('position')
                p.team = player.get('team')
                p.age = player.get('age')
                p.height = player.get('height')
                p.last_name = player.get('last_name')
                db.session.commit()

            else:
                p = Player(id=player.get('player_id'), last_name=player.get('last_name'), full_name=player.get('full_name'),
                           position=player.get('position'), team=player.get('team'), age=player.get('age'), height=player.get('height'))

                db.session.add(p)
                db.session.commit()
