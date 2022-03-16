def get_roster(league_data, user_id):

    for owner in league_data:
        if owner['owner_id'] == user_id:
            return owner

    return 'not found'
