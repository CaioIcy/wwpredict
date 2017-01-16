from role import Role
import argparse
import logging

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

def is_balanced(roles):
    nPlayers = len(roles)
    varianceAllowed = (nPlayers / 4) + 1

    logging.info("Roles:")
    for role in roles:
        logging.info("-> " + str(role) + " (" + str(role.strength(roles)) + ")")
    logging.info("")

    vgRoles = [role for role in roles if (role not in Role.non_vg_roles())]
    vgStrength = 0
    logging.info("Village roles:")
    for role in vgRoles:
        roleStrength = role.strength(roles)
        logging.info("-> " + str(role) + " (" + str(roleStrength) + ")")
        vgStrength += roleStrength
    logging.info("**** Village strength is: " + str(vgStrength) + " ****\n")

    nonVgRoles = [role for role in roles if (role in Role.non_vg_roles())]
    nonVgStrength = 0
    logging.info("Non-village roles:")
    for role in nonVgRoles:
        roleStrength = role.strength(roles)
        logging.info("-> " + str(role) + " (" + str(roleStrength) + ")")
        nonVgStrength += roleStrength
    logging.info("**** Non-village strength is: " + str(nonVgStrength) + " ****\n")

    totalStrength = abs(vgStrength - nonVgStrength)
    logging.info("Strength is: " + str(totalStrength))

    balanced = (totalStrength <= varianceAllowed)
    if(not balanced):
        logging.info("[FAIL] Outisde allowed variance (" + str(totalStrength) + " > " + str(varianceAllowed) + "):\n " + str(roles))
    return balanced



def project_truth(lie_roles):
    print("Projecting for these roles: " + str(lie_roles))
    possible_fakers = set()
    possibilities_per_faker = set()
    for i, role in enumerate(lie_roles):
        curr = lie_roles[:]
        for possible_role in Role.wolf_roles_2():
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
    dumps = [
        {'correct_roles': [Role.ClumsyGuy, Role.AlphaWolf, Role.Doppelganger, Role.Mason, Role.Mason],
         'lies': [(Role.AlphaWolf, Role.Mason)]},
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
            lie_roles = [lie[1] if role == lie[0] else role for role in dump['correct_roles']]

        if(is_balanced(lie_roles)):
            print("Already balanced...")
            continue
        project_truth(lie_roles)
        raise

if __name__ == '__main__':
    main()
