import abc


class Skill(object):
    def __init__(self, damage_coef, skill_target, need_anger=0, normal_attack=True, debuff=None):
        self.__damage_coef = damage_coef
        self.__skill_target = skill_target
        self.__need_anger = need_anger
        self.__normal_attack = normal_attack
        self.__debuff = debuff
        self.__damage = 0

    @property
    def damage(self):
        return self.__damage

    @damage.setter
    def damage(self, base_damage):
        self.__damage = base_damage * self.__damage_coef

    @property
    def anger(self):
        return self.__need_anger

    def attack_enemy(self, enemy_team, me_state, src_hero_prop):
        targets = self.__skill_target.get_target(enemy_team, me_state)
        for target in targets:
            target.is_attacked(self.__damage, self.__debuff, src_hero_prop)

        if self.__normal_attack:
            return -40

        return self.__need_anger

    def __repr__(self):
        return '<Skill: Damage({}) SkillTarget({}) NeedAnger({})'.format(self.__damage, self.__skill_target,
                                                                         self.__need_anger)


class SkillTarget(object):
    @abc.abstractmethod
    def get_target(self, enemy_team, me_state):
        pass


class NormalAttackTarget(SkillTarget):
    def __search_alive_hero_idx(self, team, idx, left, right):
        if not team[idx].dead:
            return idx

        lefter_delta = -1
        righter_delta = 1
        lefter = righter = 0

        while lefter >= left or righter < right:
            lefter = idx + lefter_delta
            if lefter >= left:
                lefter_delta -= 1
                if not team[lefter].dead:
                    return lefter

            righter = idx + righter_delta
            if righter < right:
                righter_delta += 1
                if not team[righter].dead:
                    return righter

    def get_target(self, enemy_team, me_state):
        enemy_numbers = len(enemy_team)
        base = enemy_numbers // 2
        me_state %= base

        if enemy_team.front_all_dead():
            # enemy_idx = me_state + base
            enemy_idx = self.__search_alive_hero_idx(enemy_team, me_state + base, base, enemy_numbers)
        else:
            # enemy_idx = me_state
            enemy_idx = self.__search_alive_hero_idx(enemy_team, me_state, 0, base)

        return [enemy_team[enemy_idx]]

    def __repr__(self):
        return 'NormalTarget'


class AllTarget(SkillTarget):
    def get_target(self, enemy_team, me_state):
        return enemy_team

    def __repr__(self):
        return 'AllTarget'


class WeakestTarget(SkillTarget):
    def get_target(self, enemy_team, me_state):
        weakest_hero = enemy_team[0]
        for hero in enemy_team:
            if (not hero.dead and hero.life < weakest_hero.life) or weakest_hero.life < 0:
                weakest_hero = hero

        return [weakest_hero]

    def __repr__(self):
        return 'WeakestTarget'


class FrontTarget(SkillTarget):
    def get_target(self, enemy_team, me_state):
        begin, end = 0, 0
        enemy_numbers = len(enemy_team)
        if enemy_team.front_all_dead():
            begin, end = enemy_numbers // 2, enemy_numbers
        else:
            begin, end = 0, enemy_numbers // 2

        return [enemy_team[i] for i in range(begin, end)]

    def __repr__(self):
        return 'FrontTarget'


class SkillTemplate(object):
    @staticmethod
    def gen_tank_skills():
        return [Skill(1, NormalAttackTarget()), Skill(1.7, FrontTarget(), 100, normal_attack=False)]

    @staticmethod
    def gen_killer_skills():
        return [Skill(1, NormalAttackTarget()), Skill(3, WeakestTarget(), 100, normal_attack=False)]

    @staticmethod
    def gen_master_skills():
        return [Skill(1, FrontTarget()), Skill(2.5, AllTarget(), 100, normal_attack=False)]

    @staticmethod
    def gen_healer_skills():
        return [Skill(1, WeakestTarget()), Skill(1.2, AllTarget(), 100, normal_attack=False)]
