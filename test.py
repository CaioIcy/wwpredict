from role import Role
import werewolf as ww
import argparse
import logging


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
         'lies': [(Role.SerialKiller, Role.Fool)]},
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
        balanced = ww.is_balanced(dump['correct_roles'])
        if(balanced):
            print(str(i+1) + ") [OK] Inside allowed variance")
        else:
            print(str(i+1) + ") [FAIL] Outisde allowed variance")

    for dump in dumps:
        lie_roles = dump['correct_roles']
        for lie in dump['lies']:
            lie_roles = [lie[1] if role == lie[0] else role for role in
                         dump['correct_roles']]

        if(ww.is_balanced(lie_roles)):
            print("Already balanced...")
            continue
        ww.project_truth(lie_roles)
        # raise


if __name__ == '__main__':
    main()
