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


def project_truth(lie_roles):
    print("Projecting for these roles: " + str(lie_roles))
    possible_fakers = set()
    possibilities_per_faker = set()
    for i, role in enumerate(lie_roles):
        curr = lie_roles[:]
        for possible_role in Role.wolves():
            curr[i] = possible_role
            balanced = is_balanced(curr)
            if(balanced):
                possible_fakers.add(role)
                possibilities_per_faker.add((role, possible_role))

    if not possible_fakers:
        print("No possible fakers with the given roles.")
        raise

    print("These are the possible fakers:")
    for role in possible_fakers:
        print("-> " + str(role) + ";")
        for p in possibilities_per_faker:
            if role == p[0]:
                print("    => " + str(p[1]))
    print("\n")
