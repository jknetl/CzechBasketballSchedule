from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from googleapiclient.errors import HttpError
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from cbf.model import Game

import datetime


try:
    import argparse

    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

EVENT_ID_PREFIX = 'cbf'

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/calendar'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'cbf'
CREDENTIALS_STORAGE_FILE_NAME = 'CzechBasketballSchedule.json'


def _get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   CREDENTIALS_STORAGE_FILE_NAME)

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        file = ".." + os.sep + CLIENT_SECRET_FILE
        flow = client.flow_from_clientsecrets(file, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else:  # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials


def authorize():
    credentials = _get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('calendar', 'v3', http=http)
    return service


def to_google_event(game):
    """

    :param game:
    :type game: Game
    :return:
    :type dict
    """

    # determine date
    if game.date_time == None:
        return None # if game has no date assigned then it is not an event for calendar

    if game.date_time.hour == 0:
        start = {'date': to_google_date_format(game.date_time.date())}
        end = {'date': to_google_date_format(game.date_time.date())}
    else:
        start = {'dateTime' : to_google_date_format(game.date_time)}
        end = {'dateTime': to_google_date_format(game.date_time + datetime.timedelta(hours = 2))}



    event = {
        'id' : generate_game_id(game),
        'summary': "{} - {}".format(game.team_home_name, game.team_guest_name),
        #'location': game.arena,
        'description':  "Event automatically parsed by CzechBasketballSchedule",
        'start' : start,
        'end' : end
    }

    return event

def to_google_date_format(dt):
    d = dt #type:datetime.datetime
    return d.isoformat()


def generate_game_id(game):
    return (EVENT_ID_PREFIX
            + "cid" + game.competition_id
            + "phid" + game.phase_id
            + "id" + game.id)


def create_event(service, game):
    event = to_google_event(game)
    try:
        response = service.events().insert(calendarId='primary', body=event).execute()
    except HttpError as err:
        if err.resp.status == 409: # duplicate id
            response = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()

    print(response.get('htmlLink'))

