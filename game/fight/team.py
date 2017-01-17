import collections


class GameTeam(list):
    def __init__(self, *args, **kwargs):
        super(GameTeam, self).__init__(*args)
        self._cur_hero_idx = 0
        self.__desc = kwargs.get('desc')

    def angry(self):
        # NOTE: cache the angry hero
        for hero in self:
            if not hero.dead and hero.angry():
                return True
        return False

    @property
    def dead(self):
        for hero in self:
            if not hero.dead:
                return False
        return True

    def __forward_hero_idx(self):
        self._cur_hero_idx += 1
        if self._cur_hero_idx >= len(self):
            self._cur_hero_idx = 0

    @property
    def cur_hero(self):
        if len(self) >= 1:
            return self[self._cur_hero_idx]
        return None

    def attack(self, enemy_teams):
        enemy_team = enemy_teams[0]

        for hero in self:
            # release anger
            if hero.angry():
                return hero.attack(enemy_team, self._cur_hero_idx)

        cur_hero = self.cur_hero
        if cur_hero:
            cur_hero.attack(enemy_team, self._cur_hero_idx)
            self.__forward_hero_idx()

    def front_all_dead(self):
        for i in range(len(self) // 2):
            if not self[i].dead:
                return False

        return True

    def __repr__(self):
        return '<Team {}>'.format(self.__desc)

    def full_str(self):
        return 'Team {}: '.format(self.__desc) + '\n'.join([str(i) for i in self])


class TeamStateCache(object):
    def __init__(self, teams):
        self.__teams = teams

    def add_dead_team(self, team):
        self.__teams.remove(team)

    def game_over(self):
        count = 0
        for team in self.__teams[:]:
            if not team.dead:
                count += 1
            else:
                self.__teams.remove(team)

        return count <= 1

    def get_winner(self):
        return self.__teams[0] if self.__teams and len(self.__teams) == 1 else None


class TeamSelector(collections.Iterator):
    """
    Choose next team to take action
    """

    def __init__(self, teams, release_at_once=True):
        self._teams = teams
        self._release_at_once = release_at_once
        # self._cur_team = teams[0]
        self._angry_team_idx = 0
        self._cur_team_idx = 0
        self._team_size = len(teams)
        self._team_state_cache = TeamStateCache(teams)

    def __next__(self):
        # alive_team_count = self._team_size
        for i in range(self._team_size):
            # any team is angry?
            team = self._teams[self._angry_team_idx]
            if team.angry():
                if not self._release_at_once:
                    self._angry_team_idx = self._circle_add(self._angry_team_idx)
                return team

            self._angry_team_idx = self._circle_add(self._angry_team_idx)
        else:
            if self._team_state_cache.game_over():
                raise StopIteration()

            self._angry_team_idx = 0

            for i in range(self._team_size):
                cur_team = self._teams[self._cur_team_idx]
                self._forward_team()
                if cur_team.dead:
                    self._team_state_cache.add_dead_team(cur_team)
                    continue

                return cur_team

    def _forward_team(self):
        self._cur_team_idx = self._circle_add(self._cur_team_idx)

    def _circle_add(self, idx):
        idx += 1
        if idx >= self._team_size:
            idx = 0
        return idx

    def get_winner(self):
        return self._team_state_cache.get_winner()
