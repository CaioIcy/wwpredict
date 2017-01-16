from role import Role


def is_balanced(roles):
    variance_allowed = (len(roles) / 4) + 1

    village_roles = [role for role in roles if (role not in
                     Role.non_villagers())]
    village_strength = 0
    for role in village_roles:
        village_strength += role.strength(roles)

    non_village_roles = [role for role in roles if (role in
                         Role.non_villagers())]
    non_village_strength = 0
    for role in non_village_roles:
        non_village_strength += role.strength(roles)

    final_strength = abs(village_strength - non_village_strength)
    return (final_strength <= variance_allowed)


def project_truth(lie_roles):
    print("Projecting for these roles: " + str(lie_roles))
    possible_fakers = set()
    possibilities_per_faker = set()
    for i, role in enumerate(lie_roles):
        curr = lie_roles[:]
        for possible_role in Role.wolves_2():
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
