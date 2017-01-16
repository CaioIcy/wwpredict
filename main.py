from enum import Enum, unique


doDebug = False


@unique
class Role(Enum):
    Villager = 1
    Drunk = 2
    Harlot = 3
    Seer = 4
    Traitor = 5
    GuardianAngel = 6
    Detective = 7
    Wolf = 8
    Cursed = 9
    Gunner = 10
    Tanner = 11
    Fool = 12
    WildChild = 13
    Beholder = 14
    ApprenticeSeer = 15
    Cultist = 16
    CultistHunter = 17
    Mason = 18
    Doppelganger = 19
    Cupid = 20
    Hunter = 21
    SerialKiller = 22
    Sorcerer = 23
    AlphaWolf = 24
    WolfCub = 25
    Blacksmith = 26
    ClumsyGuy = 27
    Mayor = 28
    Prince = 29
    # MaybeSeer      = 30


    def __repr__(self):
        return str(self)


    def strength(self, allRoles):
        if(self == Role.Villager):
            return 1
        elif(self == Role.Drunk):
            return 3
        elif(self == Role.Harlot):
            return 6
        elif(self == Role.Seer):
            return 7
        elif(self == Role.Traitor):
            return 0
        elif(self == Role.GuardianAngel):
            return 7
        elif(self == Role.Detective):
            return 6
        elif(self == Role.Wolf):
            return 10
        elif(self == Role.Gunner):
            return 6
        elif(self == Role.Fool):
            return 3
        elif(self == Role.WildChild):
            return 1
        elif(self == Role.ApprenticeSeer):
            return 6
        elif(self == Role.Doppelganger):
            return 2
        elif(self == Role.Cupid):
            return 2
        elif(self == Role.Hunter):
            return 6
        elif(self == Role.SerialKiller):
            return 15
        elif(self == Role.Sorcerer):
            return 2
        elif(self == Role.AlphaWolf):
            return 12
        elif(self == Role.WolfCub):
            return 12
        elif(self == Role.Blacksmith):
            return 5
        elif(self == Role.ClumsyGuy):
            return -1
        elif(self == Role.Mayor):
            return 4
        elif(self == Role.Prince):
            return 3
        elif(self == Role.Cursed):
            # 1 - allRoles.Count(x => wolfRoles.Contains(x)) / 2
            return 1 - (len([role for role in allRoles if role in Role.wolf_roles()]) / 2)
        elif(self == Role.Cultist):
            # 10 + allRoles.Count(x => !nonConvertibleRoles.Contains(x))
            return 10 + len([role for role in allRoles if role not in Role.non_convertible_roles()])
        elif(self == Role.CultistHunter):
            # allRoles.Count(x => x == Role.Cultist) == 0 ? 1 : 7
            return 7 if Role.Cultist in allRoles else 1
        elif(self == Role.Mason):
            # allRoles.Count(x => x == Role.Mason) <= 1 ? 1 : allRoles.Count(x => x == Role.Mason) + 3
            return allRoles.count(Role.Mason) + 3 if allRoles.count(Role.Mason) > 1 else 1
        elif(self == Role.Beholder):
            # 2 + (allRoles.Any(x => x == IRole.Seer) ? 4 : 0)
            return 2 + (4 if Role.Seer in allRoles else 0)
        elif(self == Role.Tanner):
            # allRoles.Count / 2
            return len(allRoles) / 2
        else:
            raise RuntimeError

    @staticmethod
    def non_vg_roles():
        return [Role.Cultist, Role.SerialKiller, Role.Tanner, Role.Wolf,
                Role.AlphaWolf, Role.Sorcerer, Role.WolfCub]

    @staticmethod
    def wolf_roles():
        return [Role.WolfCub, Role.WolfCub, Role.AlphaWolf]

    # The original wolf roles in their code has 2 WolfCubs and leaves Wolf out.
    @staticmethod
    def wolf_roles_2():
        return [Role.Wolf, Role.WolfCub, Role.AlphaWolf]

    @staticmethod
    def non_convertible_roles():
        return [Role.Seer, Role.GuardianAngel, Role.Detective, Role.Cursed,
                Role.Harlot, Role.Hunter, Role.Doppelganger, Role.Wolf,
                Role.AlphaWolf, Role.WolfCub, Role.SerialKiller]


def debug(msg):
    if(doDebug):
        print(msg)

def is_balanced(roles):
    nPlayers = len(roles)
    varianceAllowed = (nPlayers / 4) + 1

    debug("Roles:")
    for role in roles:
        debug("-> " + str(role) + " (" + str(role.strength(roles)) + ")")
    debug("")

    vgRoles = [role for role in roles if (role not in Role.non_vg_roles())]
    vgStrength = 0
    debug("Village roles:")
    for role in vgRoles:
        roleStrength = role.strength(roles)
        debug("-> " + str(role) + " (" + str(roleStrength) + ")")
        vgStrength += roleStrength
    debug("**** Village strength is: " + str(vgStrength) + " ****\n")

    nonVgRoles = [role for role in roles if (role in Role.non_vg_roles())]
    nonVgStrength = 0
    debug("Non-village roles:")
    for role in nonVgRoles:
        roleStrength = role.strength(roles)
        debug("-> " + str(role) + " (" + str(roleStrength) + ")")
        nonVgStrength += roleStrength
    debug("**** Non-village strength is: " + str(nonVgStrength) + " ****\n")

    totalStrength = abs(vgStrength - nonVgStrength)
    debug("Strength is: " + str(totalStrength))

    balanced = (totalStrength <= varianceAllowed)
    if(not balanced):
        debug("[FAIL] Outisde allowed variance (" + str(totalStrength) + " > " + str(varianceAllowed) + "):\n " + str(roles))
    return balanced



def project_truth(dump):
    lie_roles = dump['correct_roles']
    for lie in dump['lies']:
        lie_roles = [lie[1] if role == lie[0] else role for role in dump['correct_roles']]

    if(is_balanced(lie_roles)):
        print("Already balanced...")
        return

    print("Projecting for these roles: " + str(lie_roles))
    possible_liars = set()
    possibilities = set()
    for i, role in enumerate(lie_roles):
        curr = lie_roles[:]
        for possible_role in Role.wolf_roles_2():
            curr[i] = possible_role
            balanced = is_balanced(curr)
            if(balanced):
                possible_liars.add(role)
                possibilities.add((role, possible_role))

    print("These are the possible liars:")
    for role in possible_liars:
        print("-> " + str(role) + ";")
        for p in possibilities:
            if role == p[0]:
                print("    => " + str(p[1]))
    print("\n")

def main():
    dumps = [
        {'correct_roles': [Role.ClumsyGuy, Role.AlphaWolf, Role.Doppelganger, Role.Mason, Role.Mason],
         'lies': [(Role.AlphaWolf, Role.Villager)]},
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
        project_truth(dump)

if __name__ == '__main__':
    main()
