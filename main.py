from role import Role
import argparse
import logging


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


def main():
    parser = argparse.ArgumentParser(description='Predict Werewolf games.')
    parser.add_argument('--log', dest='log_level', help='log help msg')
    args = parser.parse_args()

    if args.log_level:
        numeric_level = getattr(logging, args.log_level.upper(), None)
        if not isinstance(numeric_level, int):
            raise ValueError('Invalid log level: %s' % args.log_level)
        logging.basicConfig(level=numeric_level,
                            format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')
    else:
        logging.basicConfig(format='%(asctime)s %(levelname)-8s %(message)s',
                            datefmt='%Y/%m/%d %H:%M:%S')

    dumps = [
        {'correct_roles': [Role.ClumsyGuy, Role.AlphaWolf, Role.Doppelganger, Role.Mason, Role.Mason],
         'lies': [(Role.AlphaWolf, Role.Mason)]},
        {'correct_roles': [Role.ClumsyGuy, Role.WolfCub, Role.Mayor, Role.Cupid, Role.Drunk, Role.Prince],
         'lies': [(Role.WolfCub, Role.Mason)]},
        {'correct_roles': [Role.ClumsyGuy, Role.Doppelganger, Role.Beholder, Role.SerialKiller, Role.Hunter, Role.Blacksmith],
         'lies': [(Role.SerialKiller, Role.Villager)]},
        {'correct_roles': [Role.Prince, Role.Sorcerer, Role.Harlot, Role.Drunk, Role.WildChild, Role.WolfCub, Role.Cursed],
         'lies': [(Role.WolfCub, Role.Villager)]},
        {'correct_roles': [Role.Drunk, Role.Tanner, Role.Mason, Role.Villager, Role.Hunter, Role.AlphaWolf, Role.Gunner],
         'lies': [(Role.AlphaWolf, Role.Villager)]},
        {'correct_roles': [Role.Prince, Role.Villager, Role.Villager, Role.AlphaWolf, Role.GuardianAngel, Role.Fool, Role.Tanner, Role.Doppelganger],
         'lies': [(Role.AlphaWolf, Role.Villager)]},
        {'correct_roles': [Role.Villager, Role.Mayor, Role.Villager, Role.Seer, Role.Cultist, Role.WolfCub, Role.ApprenticeSeer, Role.Cupid, Role.Prince, Role.Villager, Role.CultistHunter],
         'lies': [(Role.WolfCub, Role.Villager)]}
    ]

    for i, dump in enumerate(dumps):
        balanced = is_balanced(dump['correct_roles'])
        if(balanced):
            print(str(i+1) + ") [OK] Inside allowed variance")
        else:
            print(str(i+1) + ") [FAIL] Outisde allowed variance")

    for dump in dumps:
        lie_roles = dump['correct_roles']
        for lie in dump['lies']:
            lie_roles = [lie[1] if role == lie[0] else role for role in
                         dump['correct_roles']]

        if(is_balanced(lie_roles)):
            print("Already balanced...")
            continue
        project_truth(lie_roles)
        raise


if __name__ == '__main__':
    main()
