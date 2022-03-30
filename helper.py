def player_averages(players):
    p_ages = [int(p.age) for p in players if p.age != None]

    avg_age = sum(p_ages) // len(p_ages)

    p_height = [int(p.height) for p in players if p.height != None]

    avg_height = round(sum(p_height) / len(p_height) / 12, 2)

    return {'avg_age': avg_age, 'avg_height': avg_height}
