from enum import Enum, unique


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
