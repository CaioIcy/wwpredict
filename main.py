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

    player_count = 5
    allow_cult = True
    allow_tanner = True
    allow_fool = True
    players = {
        'certain': [Role.Mason, Role.Mason],
        'uncertain': [Role.ClumsyGuy, Role.Detective, Role.Doppelganger]
    }

    ww.project_truth(player_count, allow_cult, allow_tanner, allow_fool, players)


if __name__ == '__main__':
    main()
