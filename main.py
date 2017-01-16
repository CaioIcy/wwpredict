from enum import Enum


doDebug = False


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


def debug(msg):
    if(doDebug):
        print(msg)


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
        # 1 - allRoles.Count(x => wolfRoles.Contains(x)) / 2
        return 1 - (len([role for role in allRoles if role in wolfRoles]) / 2)
    elif(role == Role.Cultist):
        # 10 + allRoles.Count(x => !nonConvertibleRoles.Contains(x))
        return 10 + len([role for role in allRoles if role not in nonConvertibleRoles])
    elif(role == Role.CultistHunter):
        # allRoles.Count(x => x == Role.Cultist) == 0 ? 1 : 7
        return 7 if Role.Cultist in allRoles else 1
    elif(role == Role.Mason):
        # allRoles.Count(x => x == Role.Mason) <= 1 ? 1 : allRoles.Count(x => x == Role.Mason) + 3
        return allRoles.count(Role.Mason) + 3 if allRoles.count(Role.Mason) > 1 else 1
    elif(role == Role.Beholder):
        # 2 + (allRoles.Any(x => x == IRole.Seer) ? 4 : 0)
        return 2 + (4 if Role.Seer in allRoles else 0)
    elif(role == Role.Tanner):
        # allRoles.Count / 2
        return len(allRoles) / 2
    else:
        raise RuntimeError


def report(roles):
    debug("Init.\n")
    nvgroles = [Role.Cultist, Role.SerialKiller, Role.Tanner, Role.Wolf,
                Role.AlphaWolf, Role.Sorcerer, Role.WolfCub]
    nPlayers = len(roles)
    varianceAllowed = (nPlayers / 4) + 1

    debug("Roles:")
    for role in roles:
        debug("-> " + str(role) + " (" + str(getStrength(role, roles)) + ")")
    debug("")

    vgRoles = [r for r in roles if (r not in nvgroles)]
    vgStrength = 0
    debug("Village roles:")
    for role in vgRoles:
        roleStrength = getStrength(role, roles)
        debug("-> " + str(role) + " (" + str(roleStrength) + ")")
        vgStrength += roleStrength
    debug("**** Village strength is: " + str(vgStrength) + " ****\n")

    nonVgRoles = [r for r in roles if (r in nvgroles)]
    nonVgStrength = 0
    debug("Non-village roles:")
    for role in nonVgRoles:
        roleStrength = getStrength(role, roles)
        debug("-> " + str(role) + " (" + str(roleStrength) + ")")
        nonVgStrength += roleStrength
    debug("**** Non-village strength is: " + str(nonVgStrength) + " ****\n")

    totalStrength = abs(vgStrength - nonVgStrength)
    debug("Strength is: " + str(totalStrength))

    balanced = (totalStrength <= varianceAllowed)
    if(balanced):
        print("[OK] Inside allowed variance (" + str(totalStrength) + " <= " + str(varianceAllowed) + ")")
    else:
        print("[FAIL] Outisde allowed variance (" + str(totalStrength) + " > " + str(varianceAllowed) + "):\n " + str(roles))

    debug("\nDone.")

def main():
    report([Role.ClumsyGuy, Role.AlphaWolf, Role.Doppelganger, Role.Mason, Role.Mason])  # 5
    report([Role.ClumsyGuy, Role.Doppelganger, Role.Beholder, Role.SerialKiller, Role.Hunter, Role.Blacksmith])  # 6
    report([Role.Prince, Role.Sorcerer, Role.Harlot, Role.Drunk, Role.WildChild, Role.WolfCub, Role.Cursed])  # 7
    report([Role.Drunk, Role.Tanner, Role.Mason, Role.Villager, Role.Hunter, Role.AlphaWolf, Role.Gunner])  # 7
    report([Role.Prince, Role.Villager, Role.Villager, Role.AlphaWolf, Role.GuardianAngel, Role.Fool, Role.Tanner, Role.Doppelganger])  # 8
    report([Role.Villager, Role.Mayor, Role.Villager, Role.Seer, Role.Cultist, Role.WolfCub, Role.ApprenticeSeer, Role.Cupid, Role.Prince, Role.Villager, Role.CultistHunter])  # 11

if __name__ == '__main__':
    main()
