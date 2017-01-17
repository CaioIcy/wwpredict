from nose.tools import *
import werewolf as ww
from role import Role


'''
The minimum number of players should be 5.
'''
def test_is_valid_number_of_players():
    roles = []
    for i in range(0, 5):
        assert_false(ww.is_valid(roles, True, True, True))
        roles.append(Role.Villager)

'''
Should not have Cultist or Cultist Hunter when not allowed or less than 11
players.
'''
def test_is_valid_cultists():
    roles_with_cultists_10 = [Role.Cultist, Role.CultistHunter, Role.Villager,
                   Role.Villager, Role.Villager, Role.Villager, Role.Villager,
                   Role.Villager, Role.Villager, Role.Villager]
    assert_equals(len(roles_with_cultists_10), 10)
    assert_false(ww.is_valid(roles_with_cultists_10, True, True, True))

    roles_with_cultists_11 = [Role.Cultist, Role.CultistHunter, Role.Villager,
                   Role.Villager, Role.Villager, Role.Villager, Role.Villager,
                   Role.Villager, Role.Villager, Role.Villager, Role.Villager]
    assert_equals(len(roles_with_cultists_11), 11)
    assert_false(ww.is_valid(roles_with_cultists_11, False, True, True))

'''
Should not have Tanner when not allowed.
'''
def test_is_valid_tanner():
    assert_false(ww.is_valid([Role.Tanner, Role.Villager, Role.Villager,
                             Role.Villager, Role.Wolf], True, False, True))
    assert_true(ww.is_valid([Role.Tanner, Role.Villager, Role.Villager,
                             Role.Villager, Role.Wolf], True, True, True))

'''
Should not have Fool when not allowed.
'''
def test_is_valid_fool():
    assert_false(ww.is_valid([Role.Fool, Role.Villager, Role.Villager,
                             Role.Villager, Role.Wolf], True, True, False))
    assert_true(ww.is_valid([Role.Fool, Role.Villager, Role.Villager,
                             Role.Villager, Role.Wolf], True, True, True))

'''
Should not have Sorcerer or Traitor without a wolf.
'''
def test_is_valid_sorcerer_traitor_without_wolves():
    assert_false(ww.is_valid([Role.Sorcerer, Role.Villager, Role.Villager,
                             Role.Villager, Role.SerialKiller], True, True, True))
    assert_false(ww.is_valid([Role.Traitor, Role.Villager, Role.Villager,
                             Role.Villager, Role.SerialKiller], True, True, True))
    assert_true(ww.is_valid([Role.Sorcerer, Role.Villager, Role.Villager,
                             Role.Villager, Role.Wolf], True, True, True))
    assert_true(ww.is_valid([Role.Traitor, Role.Villager, Role.Villager,
                             Role.Villager, Role.Wolf], True, True, True))

'''
Should not have Apprentice Seer without a Seer.
'''
def test_is_valid_apprentice_seer_without_seer():
    assert_false(ww.is_valid([Role.ApprenticeSeer, Role.Wolf, Role.Villager,
                             Role.Villager, Role.Villager], True, True, True))
    assert_true(ww.is_valid([Role.ApprenticeSeer, Role.Wolf, Role.Seer,
                             Role.Villager, Role.Villager], True, True, True))

'''
Should not have a Cultist without a Cultist Hunter.
'''
def test_is_valid_cultist_without_cultist_hunter():
    roles_without_cultist_hunter = [Role.Cultist, Role.Wolf, Role.Villager,
               Role.Villager, Role.Villager, Role.Villager, Role.Villager,
               Role.Villager, Role.Villager, Role.Villager, Role.Villager]
    roles_with_cultist_hunter = [Role.Cultist, Role.CultistHunter, Role.Wolf,
               Role.Villager, Role.Villager, Role.Villager, Role.Villager,
               Role.Villager, Role.Villager, Role.Villager, Role.Villager]

    assert_false(ww.is_valid(roles_without_cultist_hunter, True, True, True))
    assert_true(ww.is_valid(roles_with_cultist_hunter, True, True, True))

'''
Should have at least one enemy.
'''
def test_is_valid_at_least_one_enemy():
    villagers_10 = [Role.CultistHunter, Role.Villager, Role.Villager, Role.Villager,
                   Role.Villager, Role.Villager, Role.Villager, Role.Villager,
                   Role.Villager, Role.Villager]
    assert_false(ww.is_valid(villagers_10 + [Role.Villager], True, True, True))
    for enemy in Role.enemies():
        assert_true(ww.is_valid(villagers_10 + [enemy], True, True, True))

'''
Real cases should be valid.
'''
def test_is_valid_real_cases():
    assert_true(ww.is_valid([Role.ClumsyGuy, Role.AlphaWolf, Role.Doppelganger, Role.Mason, Role.Mason], True, True, True))
    assert_true(ww.is_valid([Role.ClumsyGuy, Role.WolfCub, Role.Mayor, Role.Cupid, Role.Drunk, Role.Prince], True, True, True))
    assert_true(ww.is_valid([Role.ClumsyGuy, Role.Doppelganger, Role.Beholder, Role.SerialKiller, Role.Hunter, Role.Blacksmith], True, True, True))
    assert_true(ww.is_valid([Role.Prince, Role.Sorcerer, Role.Harlot, Role.Drunk, Role.WildChild, Role.WolfCub, Role.Cursed], True, True, True))
    assert_true(ww.is_valid([Role.Drunk, Role.Tanner, Role.Mason, Role.Villager, Role.Hunter, Role.AlphaWolf, Role.Gunner], True, True, True))
    assert_true(ww.is_valid([Role.Prince, Role.Villager, Role.Villager, Role.AlphaWolf, Role.GuardianAngel, Role.Fool, Role.Tanner, Role.Doppelganger], True, True, True))
    assert_true(ww.is_valid([Role.Villager, Role.Mayor, Role.Villager, Role.Seer, Role.Cultist, Role.WolfCub, Role.ApprenticeSeer, Role.Cupid, Role.Prince, Role.Villager, Role.CultistHunter], True, True, True))
