# encoding:utf-8
import logging
from game.fight.team import GameTeam, TeamSelector
from game.fight.hero import HeroTemplate


class FightingGame(object):
    def __init__(self):
        self.__teams = []

    def add_teams(self, *args):
        assert len(args) >= 2
        self.__teams.extend(args)

    def start(self):
        selector = TeamSelector(self.__teams)
        for team in selector:
            logging.info('<Team {}> begin attack!'.format(team))
            enemy_teams = self.__teams[:]
            enemy_teams.remove(team)
            team.attack(enemy_teams)

            logging.info('====== After attack ======')
            for t in self.__teams:
                logging.info(t.full_str())
            logging.info('====== End ======')

        logging.warning('Game over! Winner is {}'.format(selector.get_winner()))

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(filename)s(Line %(lineno)s): '
                                                   '%(message)s')
    we_team = GameTeam([HeroTemplate.gen_tanker() for i in range(5)], desc='We')
    we_team.append(HeroTemplate.gen_healer(team=we_team))
    # enemy_team = GameTeam([HeroTemplate.gen_master() for i in range(6)], desc='Enemy')
    enemy_team = GameTeam([HeroTemplate.gen_master() for i in range(3)] + [HeroTemplate.gen_killer() for i in range(3)],
                          desc='Enemy')

    game = FightingGame()
    # game.start()
    game.add_teams(we_team, enemy_team)
    game.start()
