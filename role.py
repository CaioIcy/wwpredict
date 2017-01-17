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

    def __repr__(self):
        return str(self)

    def strength(self, ingame_roles):
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
            wolves = [role for role in ingame_roles if role in Role.wolves_2()]
            return 1 - (len(wolves) / 2)
        elif(self == Role.Cultist):
            convertibles = [role for role in ingame_roles if role not in
                            Role.non_convertibles()]
            return 10 + len(convertibles)
        elif(self == Role.CultistHunter):
            return 7 if Role.Cultist in ingame_roles else 1
        elif(self == Role.Mason):
            mason_count = ingame_roles.count(Role.Mason)
            return mason_count + 3 if mason_count > 1 else 1
        elif(self == Role.Beholder):
            return 2 + (4 if Role.Seer in ingame_roles else 0)
        elif(self == Role.Tanner):
            return len(ingame_roles) / 2
        else:
            raise RuntimeError

    @staticmethod
    def non_villagers():
        return [Role.Cultist, Role.SerialKiller, Role.Tanner, Role.Wolf,
                Role.AlphaWolf, Role.Sorcerer, Role.WolfCub]

    @staticmethod
    def wolves():
        return [Role.Wolf, Role.WolfCub, Role.AlphaWolf]

    # The original wolf roles in their code has 2 WolfCubs and leaves Wolf out.
    @staticmethod
    def wolves_2():
        return [Role.WolfCub, Role.WolfCub, Role.AlphaWolf]

    @staticmethod
    def non_convertibles():
        return [Role.Seer, Role.GuardianAngel, Role.Detective, Role.Cursed,
                Role.Harlot, Role.Hunter, Role.Doppelganger, Role.Wolf,
                Role.AlphaWolf, Role.WolfCub, Role.SerialKiller]

    @staticmethod
    def enemies():
        return [Role.Wolf, Role.WolfCub, Role.AlphaWolf, Role.SerialKiller,
                Role.Cultist]

    @staticmethod
    def all():
        return [Role.Villager, Role.Drunk, Role.Harlot, Role.Seer, Role.Traitor,
                Role.GuardianAngel, Role.Detective, Role.Wolf, Role.Cursed,
                Role.Gunner, Role.Tanner, Role.Fool, Role.WildChild,
                Role.Beholder, Role.ApprenticeSeer, Role.Cultist,
                Role.CultistHunter, Role.Mason, Role.Doppelganger, Role.Cupid,
                Role.Hunter, Role.SerialKiller, Role.Sorcerer, Role.AlphaWolf,
                Role.WolfCub, Role.Blacksmith, Role.ClumsyGuy, Role.Mayor,
                Role.Prince]
