from datetime import date
import requests

from cbf.model import Competition, Phase, Game, Team


class Dao(object):
    """DAO class servers for obtaining model data from CBF REST endpoints"""

    API_URL = 'http://www.cbf.cz/xml/api/'

    COMPETITIONS_ENDPOINT = API_URL + 'divs.php'
    PHASES_ENDPOINT = API_URL + 'phases.php'
    TABLE_ENDPOINT = API_URL + 'table.php'
    PHASE_GAMES_ENDPOINT = API_URL + 'games.php'
    GAME_ENDPOINT = API_URL + 'game.php'
    TEAMS_ENDPOINT = API_URL + 'team.php'
    PLAYERS_ENDPOINT = API_URL + 'teamplayers.php'

    def __init__(self, year = -1):

        if year == -1:
            year = date.today().strftime("%Y")
        self.params = {'json' : 1, 'season' : year}

    def list_competitions(self, female = 0):
        params = self.params.copy()
        params['female'] = female
        r = requests.get(Dao.COMPETITIONS_ENDPOINT, params)
        json_data = r.json()

        competitions = []

        for comp in json_data:
            c = Competition(**comp)
            competitions.append(c)

        return competitions

    def list_phases(self, competition):
        params = self.params.copy()
        params['competition'] = competition.id

        r = requests.get(Dao.PHASES_ENDPOINT, params)
        json_data = r.json()

        phases = []

        for phase in json_data:
            p = Phase(**phase)
            phases.append(p)

        return phases

    def list_games(self, phase):
        params = self.params.copy()
        params['phase'] = phase.id

        r = requests.get(Dao.PHASE_GAMES_ENDPOINT, params)
        json_data = r.json()

        games = []

        for game in json_data:
            g = Game(**game)
            games.append(g)

        return games

    def list_teams(self, phase):
        params = self.params.copy()
        params['phase'] = phase.id

        r = requests.get(Dao.TABLE_ENDPOINT, params)
        json_data = r.json()

        # this could be either paralelized or data could be obtained just from the table
        # in case of performance issues.
        teams = []
        for row in json_data:
            t = self.get_team(row['tid'], row['cid'])
            teams.append(t)
        return teams

    def get_team(self, team_id, competition_id):
        params = self.params.copy()
        params['id'] = team_id
        params['competition'] = competition_id

        r = requests.get(Dao.TEAMS_ENDPOINT, params)
        if r.status_code != requests.codes.ok:
            return None

        json_data = r.json()

        team_info = json_data['info'][0]
        team = Team(**team_info)

        return team
