from enum import Enum


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


def getStrength(role, allRoles):
    wolfRoles = [Role.WolfCub, Role.WolfCub, Role.AlphaWolf]
    nonConvertibleRoles = [Role.Seer, Role.GuardianAngel, Role.Detective,
                           Role.Cursed, Role.Harlot, Role.Hunter,
                           Role.Doppelganger, Role.Wolf, Role.AlphaWolf,
                           Role.WolfCub, Role.SerialKiller]
    if(role == Role.Villager):
        return 1
    elif(role == Role.Drunk):
        return 3
    elif(role == Role.Harlot):
        return 6
    elif(role == Role.Seer):
        return 7
    elif(role == Role.Traitor):
        return 0
    elif(role == Role.GuardianAngel):
        return 7
    elif(role == Role.Detective):
        return 6
    elif(role == Role.Wolf):
        return 10
    elif(role == Role.Gunner):
        return 6
    elif(role == Role.Fool):
        return 3
    elif(role == Role.WildChild):
        return 1
    elif(role == Role.ApprenticeSeer):
        return 6
    elif(role == Role.Doppelganger):
        return 2
    elif(role == Role.Cupid):
        return 2
    elif(role == Role.Hunter):
        return 6
    elif(role == Role.SerialKiller):
        return 15
    elif(role == Role.Sorcerer):
        return 2
    elif(role == Role.AlphaWolf):
        return 12
    elif(role == Role.WolfCub):
        return 12
    elif(role == Role.Blacksmith):
        return 5
    elif(role == Role.ClumsyGuy):
        return -1
    elif(role == Role.Mayor):
        return 4
    elif(role == Role.Prince):
        return 3

    elif(role == Role.Cursed):
        return 666  # 1 - allRoles.Count(x => wolfRoles.Contains(x)) / 2
    elif(role == Role.Cultist):
        return 666  # 10 + allRoles.Count(x => !nonConvertibleRoles.Contains(x))
    elif(role == Role.CultistHunter):
        return 666  # allRoles.Count(x => x == Role.Cultist) == 0 ? 1 : 7
    elif(role == Role.Mason):
        return 666  # allRoles.Count(x => x == Role.Mason) <= 1 ? 1 : allRoles.Count(x => x == Role.Mason) + 3
    elif(role == Role.Beholder):
        return 2 + (4 if Role.Seer in allRoles else 0)
    elif(role == Role.Tanner):
        return 666  # allRoles.Count / 2
    else:
        raise RuntimeError


def main():
    print("Init.\n")
    nvgroles = [Role.Cultist, Role.SerialKiller, Role.Tanner, Role.Wolf,
                Role.AlphaWolf, Role.Sorcerer, Role.WolfCub]
    nPlayers = 6
    varianceAllowed = (nPlayers / 4) + 1

    roles = [Role.ClumsyGuy, Role.Doppelganger, Role.Beholder,
             Role.SerialKiller, Role.Hunter, Role.Blacksmith]
    print("Roles:")
    for role in roles:
        print("-> " + str(role) + " (" + str(getStrength(role, roles)) + ")")
    print("")

    vgRoles = [r for r in roles if (r not in nvgroles)]
    vgStrength = 0
    print("Village roles:")
    for role in vgRoles:
        roleStrength = getStrength(role, roles)
        print("-> " + str(role) + " (" + str(roleStrength) + ")")
        vgStrength += roleStrength
    print("**** Village strength is: " + str(vgStrength) + " ****\n")

    nonVgRoles = [r for r in roles if (r in nvgroles)]
    nonVgStrength = 0
    print("Non-village roles:")
    for role in nonVgRoles:
        roleStrength = getStrength(role, roles)
        print("-> " + str(role) + " (" + str(roleStrength) + ")")
        nonVgStrength += roleStrength
    print("**** Non-village strength is: " + str(nonVgStrength) + " ****\n")

    totalStrength = abs(vgStrength - nonVgStrength)
    print("Strength is: " + str(totalStrength))
    if(totalStrength < varianceAllowed):
        print("Inside allowed variance (" + str(varianceAllowed) + ")")

    print("\nDone.")


if __name__ == '__main__':
    main()
