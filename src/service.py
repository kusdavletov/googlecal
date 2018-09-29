from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
from src.constants import *
import os
import datetime
import random


def _connect(first=False):
    if first:
        dir_path = os.path.dirname(os.path.realpath(__file__))
        os.system('cd {}/auth && python3 get_token.py'.format(dir_path))
    else:
        global service
        dir_path = os.path.dirname(os.path.realpath(__file__))
        store = file.Storage(dir_path + '/auth/token.json')
        creds = store.get()
        if not creds or creds.invalid:
            flow = client.flow_from_clientsecrets(dir_path + '/auth/credentials.json', SCOPES)
            creds = tools.run_flow(flow, store)
        service = build('calendar', 'v3', http=creds.authorize(Http()))


def _format(day, time):
    day = str(day)
    time = str(time)
    today = datetime.datetime.today()
    if len(day) < 1:
        raise ValueError('Preferable format for date is dd.mm.yyyy')
    elif len(day) <= 2:
        day += '.' + str(today.month) + '.' + str(today.year)
    elif len(day) <= 5:
        day += '.' + str(today.year)
    if len(time) < 1:
        ValueError('Preferable format for time is hh:mm')
    elif len(time) <= 2:
        time += ':00'
    try:
        date = datetime.datetime.strptime(day + ' ' + time, '%d.%m.%Y %H:%M').isoformat()
    except:
        raise ValueError('Preferable format is "dd.mm.yyyy hh:mm"')
    return date


def _get_days(start_date, end_date):
    days = list()
    while start_date != end_date:
        days.append([WEEKDAYS[start_date.isoweekday()], start_date.day, MONTHS[start_date.month],
                     start_date.year, str(start_date)[:10], start_date])
        start_date += datetime.timedelta(days=1)
    return days


def _get_length(events):
    lengths1 = [len(event['summary']) for event in events]
    lengths2 = [len(event['description']) for event in events if 'description' in event]
    lengths3 = [len(event['location']) for event in events if 'location' in event]
    return max(lengths1) if lengths1 else 0, max(lengths2) if lengths2 else 0, max(lengths3) if lengths3 else 0


def _print_schedule(events, days):
    length1, length2, length3 = _get_length(events)
    for day in days:
        print(day[0] + ',', day[2], day[1])
        related_events = [event for event in events if event['start']['dateTime'][0:10] == day[4]]
        for event in related_events:
            print('   {} - {} | {:<{width1}} | {:<{width2}} | {:<{width3}} |'.
                  format(event['start']['dateTime'][11:16], event['end']['dateTime'][11:16],
                         event['summary'] if 'summary' in event else '',
                         event['description'] if 'description' in event else '',
                         event['location'] if 'location' in event else '',
                         width1=length1, width2=length2, width3=length3))
        print()


def sign_in():
    _connect(first=True)


def get_schedule(date, number):
    _connect()
    if date:
        start_date = datetime.datetime.strptime(date, '%d.%m.%Y')
    else:
        start_date = datetime.datetime.today()
        start_date = datetime.datetime(start_date.year, start_date.month, start_date.day)
    end_date = start_date + datetime.timedelta(days=number)
    days = _get_days(start_date, end_date)
    events = service.events().list(calendarId='primary', timeMin=start_date.isoformat() + 'Z',
                                   timeMax=end_date.isoformat() + 'Z', singleEvents=True,
                                   orderBy='startTime').execute().get('items', [])
    _print_schedule(events, days)


def add_event_quick():
    _connect()
    summary = None
    while not summary:
        summary = str(input('   Event summary: '))
    description = str(input('   Event description: '))
    start_day = str(input('   Please enter a day when event will start (dd.mm.yyy): '))
    start_time = str(input('   Please enter a time when event will start (hh:mm): '))
    start = _format(start_day, start_time)
    end_day = str(input('   Please enter a day when event will end (dd.mm.yyy): '))
    end_time = str(input('   Please enter a time when event will end (hh:mm): '))
    end = _format(end_day, end_time)
    event = {
        'summary': summary,
        'description': description,
        'start': {'timeZone': TIMEZONE, 'dateTime': start},
        'end': {'timeZone': TIMEZONE, 'dateTime': end},
        'reminders': {'useDefault': False},
        'colorId': random.randint(1, 12)
    }
    event = service.events().insert(calendarId='primary', body=event, sendNotifications=None).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def add_event_advanced():
    _connect()
    summary = None
    while not summary:
        summary = str(input('   Event summary: '))
    description = str(input('   Event description: '))
    location = str(input('   Event location (could be empty): '))
    start_day = str(input('   Please enter a day when event will start (dd.mm.yyy): '))
    start_time = str(input('   Please enter a time when event will start (hh:mm): '))
    start = _format(start_day, start_time)
    end_day = str(input('   Please enter a day when event will end (dd.mm.yyy): '))
    end_time = str(input('   Please enter a time when event will end (hh:mm): '))
    end = _format(end_day, end_time)
    use_recurrence = str(input('   Do you want it to make it recurrent? '))
    recurrence = None
    if use_recurrence in ['y', 'yes', 'Yes', 'YES']:
        print("      HELP: \n"
              "         FREQ — The frequency with which the event should be repeated (such as DAILY or WEEKLY). "
              "Required.\n"
              "         INTERVAL — Works together with FREQ to specify how often the event should be repeated. "
              "For example, FREQ=DAILY;INTERVAL=2 means once every two days.\n"
              "         COUNT — Number of times this event should be repeated.\n"
              "         You can use either COUNT or UNTIL to specify the end of the event recurrence. "
              "Don't use both in the same rule.\n"
              "         UNTIL — The date or date-time until which the event should be repeated (inclusive).\n"
              "         BYDAY — Days of the week on which the event should be repeated (SU, MO, TU, etc.). "
              "Other similar components include BYMONTH, BYYEARDAY, and BYHOUR.\n")
        recurrence = 'RRULE:'
        frequency = str(input('      Please enter the FREQ or leave empty: ')).upper()
        if frequency in ['DAILY', 'WEEKLY']:
            recurrence += 'FREQ=' + frequency + ';'
        interval = input('      Please enter the INTERVAL or leave empty: ')
        if interval and type(interval) == int:
            recurrence += 'INTERVAL=' + str(interval) + ';'
        count = input('      Please enter the COUNT or leave empty: ')
        if count and type(count) == int:
            recurrence += 'COUNT=' + str(count) + ';'
        else:
            until = input('      Please enter the UNTIL (example: 20150628) or leave empty: ')
            if until:
                recurrence += 'UNTIL=' + str(until) + ';'
        by = str(input('      Please enter the BY... (BYDAY, BYMONTH, BYYEARDAY, or BYHOUR) or leave empty: ')).upper()
        if by and by in ['BYDAY', 'BYMONTH', 'BYYEARDAY', 'BYHOUR']:
            by_input = str(input('      Please enter the (SU, MO, TU, etc.): ')).upper()
            recurrence += by + '=' + by_input
        if recurrence[-1] == ';':
            recurrence = recurrence[:-1]
    reminder = dict()
    use_reminder = str(input('   Use remainder? '))
    if use_reminder in ['y', 'yes', 'Yes', 'YES']:
        default_reminder = str(input('      Use default remainder? (30 min before event) '))
        if default_reminder in ['y', 'yes', 'Yes', 'YES']:
            reminder['useDefault'] = True
        else:
            reminder['useDefault'] = False
            reminder['overrides'] = list()
            popup_remainder = str(input('      Use popup remainder? '))
            if popup_remainder in ['y', 'yes', 'Yes', 'YES']:
                popup_minutes = input('         Before in min: ')
                reminder['overrides'].append({'method': 'popup', 'minutes': popup_minutes})
            email_remainder = str(input('      Use email remainder? '))
            if email_remainder in ['y', 'yes', 'Yes', 'YES']:
                email_minutes = input('         Before in min: ')
                reminder['overrides'].append({'method': 'email', 'minutes': email_minutes})
    event = {
        'summary': summary,
        'location': location,
        'description': description,
        'start': {'timeZone': TIMEZONE, 'dateTime': start},
        'end': {'timeZone': TIMEZONE, 'dateTime': end},
        'recurrence': [recurrence],
        'reminders': reminder,
        'colorId': random.randint(1, 12)
    }
    event = service.events().insert(calendarId='primary', body=event, sendNotifications=None).execute()
    print('Event created: %s' % (event.get('htmlLink')))


def get_id_from_name(name):
    _connect()
    events = service.events().list(calendarId='primary', q=name, singleEvents=True,
                                   orderBy='startTime').execute().get('items', [])
    length1, length2, _ = _get_length(events)
    for event in enumerate(events):
        output = event[1]['summary'] + (' (' + event[1]['description'] + ')' if 'description' in event[1] else '')
        print('   {}. {:<{width}} : {}'.format(event[0] + 1, output, event[1]['id'],
                                               width=(length1 + length2 + (0 if 'description' in event[1] else 3))))


def edit_event(event_id):
    _connect()
    event = service.events().get(calendarId='primary', eventId=event_id).execute()
    i = int(input('   How many items do you want to change? '))
    for _ in range(i):
        update_key = str(input('   What do you want to update? '
                               '(summary, location, description, start, end, recurrence, reminders) '))
        update_value = str(input('   Please enter new value: '))
        event[update_key] = update_value
    updated_event = service.events().update(calendarId='primary', eventId=event['id'], body=event).execute()
    print('Event updated: %s' % (updated_event.get('htmlLink')))


def delete_event(event_id):
    _connect()
    service.events().delete(calendarId='primary', eventId=event_id).execute()
    print('Event deleted')
