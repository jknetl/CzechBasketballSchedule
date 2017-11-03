from time import strptime


class Competition(object):
    """
    A competition represents a league.
    """

    def __init__(self, **kwargs):
        """
        Note, there are required parameters which must be passed through kwargs
        :param kwargs:
        """
        # competition name
        self.id = kwargs.get("compid")
        self.name = kwargs.get("cname")

        # category name (mens, U19, ...)
        self.cat_id = kwargs.get("catid")
        self.cat_name = kwargs.get("catname")

        # season
        self.season_id = kwargs.get("sid")
        self.season_name = kwargs.get()

        # is this women competition
        self.is_woman = kwargs.get("female") == '1'

        # Not required (usually matches competition)
        # self.cat_group_id = kwargs.get("cgid")
        # self.cat_group_name = kwargs.get("cgname")

    def __str__(self):
        return "Division: {} - {} ".format(self.id, self.name)


class Phase(object):
    """
    A phase represents a part of a competition (e.g. standard part, play-off, ...)
    """

    def __init__(self, **kwargs):
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.phase_type_name = kwargs.get("typename")
        self.phase_type_id = kwargs.get("IDphaseType")
        self.competition_id = kwargs.get("IDcompetition")

    def __str__(self):
        return "Phase: {} - {} ".format(self.id, self.name)


class Person(object):
    def __init__(self, id, firstname, lastname):
        self.id = id
        self.firstname = firstname
        self.lastname = lastname


class Address(object):
    def __init__(self, street, city, zipcode):
        self.street = street
        self.city = city
        self.zipcode = zipcode


class Arena(Address):
    def __init__(self, arena, street, city, zipcode, lat, lon):
        super(Arena, self).__init__(street, city, zipcode)
        self.arena = arena
        self.lat = lat
        self.lon = lon


class Team(object):
    def __init__(self, **kwargs):
        self.id = kwargs.get("IDteam")
        self.name = kwargs.get("name")
        self.name_short = kwargs.get("short_name")
        self.is_female = kwargs.get("is_male") == "0"
        self.web = kwargs.get("www")
        self.email = kwargs.get("email")
        self.address = Address(kwargs.get("street"), kwargs.get("city"), kwargs.get("psc"))
        self.phones = []

        if kwargs.get("phone_1") != None:
            self.phones.append(kwargs.get("phone_1"))
        if kwargs.get("phone_2") != None:
            self.phones.append(kwargs.get("phone_2"))

        self.category_id = kwargs.get("IDcategory")
        self.category_name = kwargs("catname")
        self.club_id = kwargs.get("IDclub")
        self.club_name = kwargs.get("clubname")

        # The team object also contains info about games and Contact person
        # but it has no usage right now


class Game(object):
    """A game represent a match between two teams."""

    def __init__(self, **kwargs):
        self.id = kwargs.get("IDgame")
        self.phase_id = kwargs.get("IDphase")
        self.round = kwargs.get("round")
        self.competition_id = kwargs.get("IDcompetition")
        self.game_number = kwargs.get("num")

        self.date_time = None
        date = kwargs.get("gdate")
        time = kwargs.get("gtime")

        if date != None and time != None:
            time_string = "{} {}".format(date, time)
            self.date_time = strptime(time_string, "%Y-%m-%d %H-%M-%S")

        self.score_home = kwargs.get("score_home")
        self.score_guest = kwargs.get("score_guest")
        self.score_quarters = kwargs.get("score_quarter")

        self.live_url = kwargs.get("url_live")
        self.ct4 = kwargs.get("ct4") == "1"
        self.tvcom_url = kwargs.get("videoIFrame")

        self.team_home = kwargs.get("taidteam")
        self.team_home_group_by = kwargs.get("tagroupby")

        self.team_guest = kwargs.get("tbidteam")
        self.team_guest_group_by = kwargs.get("tbgroupby")

        # json contains also names of the teams, but these can be fetched from teams
        self.arena = Arena(kwargs.get("place"), kwargs.get("street"), kwargs.get("city"), kwargs.get("zipcode"),
                           kwargs.get("lat"), kwargs.get("lon"))

        self.commisar = None
        if kwargs.get("commisarid") != None:
            self.commisar = Person(kwargs.get("commisarid"), kwargs.get("commisarn1"), kwargs.get("commisarn2"))

        self.referees = []

        if kwargs.get("u1id") != None:
            referee = Person(kwargs.get("u1id"), kwargs.get("u1n1"), kwargs.get("u1n2"))
            self.referees.append(referee)
        if kwargs.get("u2id") != None:
            referee = Person(kwargs.get("u2id"), kwargs.get("u2n1"), kwargs.get("u2n2"))
            self.referees.append(referee)
        if kwargs.get("u1id") != None:
            referee = Person(kwargs.get("u3id"), kwargs.get("u3n1"), kwargs.get("u3n2"))
            self.referees.append(referee)

            # a game json contains also player statistics
