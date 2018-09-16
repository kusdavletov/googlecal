# Convenient Terminal Google Calendar

## Requirements 
- Python 3.6 or greater 
- virtualenv (to install: `python3 -m pip install virtualenv`)
- Internet haha

## HOW TO INSTALL

Go to `https://developers.google.com/calendar/quickstart/python` -> click `ENABLE THE GOOGLE CALENDAR API`

This opens a new dialog. In the dialog, do the following:
- Select **+ Create a new project**
- Download the configuration file
- Move the downloaded file to `src/auth` directory and ensure it is named credentials.json

Run `cd googlecal && sudo virtualenv env && sudo python3 -m pip install -e .` in terminal.

## HOW TO USE

Just run `googlecal COMMAND`, that's all!

```
Commands:
  googlecal add                     Add new event
  googlecal add_advanced            Add new event (detailed)
  googlecal delete ID               Delete event with id
  googlecal edit ID                 Edit event with id
  googlecal get_id NAME             Get an id from event name
  googlecal login                   Sign in to Google Calendar
  googlecal schedule [OPTIONS]      Get a schedule
                      --date        Specific date to print (default: starting from today)
                      --number      Number of days to print (default: 7 days)
```

For the very first time run `googlecal login` and verify account on the website. Enjoy:)
