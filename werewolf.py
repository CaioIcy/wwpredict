from role import Role


def get_allowed_variance(player_count):
    return (player_count / 4) + 1


def is_valid(roles, allow_cult, allow_tanner, allow_fool):
    num_players = len(roles)

    if num_players < 5:
        return False

    if (not allow_cult or num_players < 11) and (Role.Cultist in roles or
       Role.CultistHunter in roles):
        return False

    if not allow_tanner and Role.Tanner in roles:
        return False

    if not allow_fool and Role.Fool in roles:
        return False

    if (Role.Sorcerer in roles or Role.Traitor in roles) and not any(
       wolf in roles for wolf in Role.wolves()):
        return False

    if Role.ApprenticeSeer in roles and Role.Seer not in roles:
        return False

    if Role.Cultist in roles and Role.CultistHunter not in roles:
        return False

    if not any(enemy in roles for enemy in Role.enemies()):
        return False

    return True


def get_village_strength(roles):
    village_strength = 0
    village_roles = [role for role in roles if (role not in
                     Role.non_villagers())]
    for role in village_roles:
        village_strength += role.strength(roles)
    return village_strength


def get_non_village_strength(roles):
    non_village_strength = 0
    non_village_roles = [role for role in roles if (role in
                         Role.non_villagers())]
    for role in non_village_roles:
        non_village_strength += role.strength(roles)
    return non_village_strength

def is_balanced(roles):
    village_strength = get_village_strength(roles)
    non_village_strength = get_non_village_strength(roles)
    final_strength = abs(village_strength - non_village_strength)
    return (final_strength <= get_allowed_variance(len(roles)))


def project_truth(players, config):
    assert(config['player_count'] == len(players['certain']) + len(players['uncertain']))
    print("Certain players: " + str(players['certain']))
    print("Uncertain players: " + str(players['uncertain']) + "\n")

    print("Safe:")
    for player in players['certain']:
        print("-> " + str(player))
    print("")

    if len(players['uncertain']) == 0:
        print("No uncertainty to be projected, game is over.")
        return
    elif len(players['uncertain']) == 1:
        print("No uncertainty to be projected.")
        print("Enemy is " + str(players['uncertain']))
        return

    fakers = {}
    for i, role in enumerate(players['uncertain']):
        current_projection = players['uncertain'][:]
        for possible_role in Role.non_villagers():
            current_projection[i] = possible_role
            valid = is_valid(current_projection + players['certain'],
                             config['allow_cult'], config['allow_tanner'],
                             config['allow_fool'])
            balanced = config['chaos'] or is_balanced(current_projection + players['certain'])
            if(valid and balanced):
                if role not in fakers:
                    fakers[role] = set()
                fakers[role].add(possible_role)

    probably_safe_players = [x for x in players['uncertain'] if x not in fakers.keys()]
    print("Probably safe:")
    for psp in probably_safe_players:
        print("-> " + str(psp) + ";")
    print("")

    print("Possibly fake:")
    for faker, possibilities in fakers.items():
        print("-> " + str(faker) + ";")
        for p in possibilities:
            print("    => " + str(p))
    print("")
