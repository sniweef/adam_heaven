import logging
import random
from game.fight.skill import SkillTemplate


class HeroProp(object):
    def __init__(self, critical_chance, hit_rate, dodge_rate, attack):
        self.critical_chance = critical_chance
        self.hit_rate = hit_rate
        self.dodge_rate = dodge_rate
        self.attack = attack


class Hero(object):
    def __init__(self, skills, life, prop=HeroProp(0, 1, 0, 100), team=None):
        assert len(skills) > 1
        self.__skills = skills
        self.__anger = 50
        self.__life = life
        self.__cur_life = life
        self.__team = team
        self.__prop = prop
        self.__debuff = None
        self.__setup__skills()

    def __setup__skills(self):
        for skill in self.__skills:
            skill.damage = self.__prop.attack

    @property
    def team(self):
        return self.__team

    @team.setter
    def team(self, team):
        self.__team = team

    @property
    def dead(self):
        return self.__cur_life <= 0

    @property
    def life(self):
        return self.__cur_life

    def angry(self):
        return self.__cur_life > 0 and self.__anger >= self.__skills[1].anger

    def attack(self, enemy_team, me_state):
        if self.dead:
            return

        target_team = enemy_team
        if self.__prop.attack < 0:
            # mean this hero is a healer
            if self.__team is None:
                raise RuntimeError('Must set team property of this Hero {}!'.format(self))
            target_team = self.__team

        if self.angry():
            logging.info('Hero {} begin attack because of his anger!'.format(self))
            self.__anger -= self.__skills[1].attack_enemy(target_team, me_state, self.__prop)
            return

        for skill in self.__skills:
            if not target_team.dead and self.__anger > skill.anger:
                logging.info('Hero(idx:{}) {} begin attack(Skill: {})!'.format(me_state, self, skill))
                self.__anger -= skill.attack_enemy(target_team, me_state, self.__prop)

    def is_attacked(self, damage, debuff, src_hero_prop):
        self.__debuff = debuff

        hit = (random.random() < (src_hero_prop.hit_rate - self.__prop.dodge_rate))
        if damage > 0 and not hit:
            logging.warning('Hero {} skip the attack!'.format(self))
            return False

        critical_damage = False
        damage *= (random.random() / 5 - 0.1 + 1)  # generate random damage (-10% ~ 10%)
        if random.random() < src_hero_prop.critical_chance:
            # logging.warning('{} is attacked by critical damage(Base damage is {})'.format(self, damage))
            damage *= 1.5
            critical_damage = True

        damage = int(damage)
        self.__cur_life -= int(damage)
        self.__anger += 15

        if critical_damage:
            logging.warning('Hero is attacked by critical damage {}(Base damage: {})! Current status is {}'
                            .format(damage, damage // 1.5, self))
        else:
            logging.info('Hero is attacked by damage {}! Current status is {}.'.format(damage, self))

        return True

    def __repr__(self):
        return '<Life({}) Anger({}) Skills({})>'.format(self.__cur_life, self.__anger, self.__skills)


class HeroTemplate(object):
    @staticmethod
    def gen_tanker(idx=1):
        return Hero(SkillTemplate.gen_tank_skills(), 4000 + 1000 * idx, prop=HeroProp(0.05, 0.9, 0.1, 400))

    @staticmethod
    def gen_killer(idx=1):
        return Hero(SkillTemplate.gen_killer_skills(), 2000 + 1000 * idx, prop=HeroProp(0.2, 1, 0.1, 900))

    @staticmethod
    def gen_master(idx=1):
        return Hero(SkillTemplate.gen_master_skills(), 3000 + 1000 * idx, prop=HeroProp(0.1, 1, 0.1, 200))

    @staticmethod
    def gen_healer(idx=1, team=None):
        return Hero(SkillTemplate.gen_healer_skills(), 3000 + 1000 * idx, prop=HeroProp(0.1, 1, 0.1, -300), team=team)
