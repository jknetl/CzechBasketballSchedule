import unittest

from cbf.dao import Dao


class EndpointsTest(unittest.TestCase):

    def setUp(self):
        self.dao = Dao(2017)

    def test_list_methods(self):
        #test competitions
        competitions = self.dao.list_competitions(0)
        kooperativa_competitions = list(filter(lambda x: "kooperativa" in x.name.lower(), competitions))
        self.assertEqual(len(kooperativa_competitions), 1)

        #test phases
        kooperativa_competition = kooperativa_competitions[0]
        phases = self.dao.list_phases(kooperativa_competition)
        basic_phases = list(filter(lambda x: "základní" in x.name.lower(), phases))
        self.assertEqual(len(basic_phases), 1)

        #test_teams
        basic_phase = basic_phases[0]
        teams = self.dao.list_teams(basic_phase)
        nymburk_teams = list(filter(lambda x: "nymburk" in x.name.lower(), teams))
        self.assertEqual(len(nymburk_teams), 1)

        #test_games
        nymburk_team = nymburk_teams[0]
        games = self.dao.list_games(basic_phase)
        nymburk_games = list(filter(lambda game: game.team_home_id == nymburk_team.id, games))
        self.assertTrue(len(nymburk_games) > 0)



if __name__ == '__main__':
    unittest.main()


