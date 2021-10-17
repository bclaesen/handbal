#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 11:29:07 2017

@author: Bert
"""
from bs4 import BeautifulSoup
from dataclasses import dataclass
from datetime import datetime, timedelta
from icalendar import Calendar, Event
from typing import List
import pytz

MY_TEAM = "Real Kiewit (R) "


@dataclass
class Game:
    """Keep track of game specific information."""
    date: str
    location: str
    home_team: str
    away_team: str

    def description(self):
        """Describes a game with its home and away team."""
        return f"{self.home_team}-{self.away_team}"

    def has_participant(self, team_name: str):
        """Indicate if a team is playing in this game or not."""
        return self.home_team == team_name or self.away_team == team_name


def tidyR(team_name: str):
    """Clean up the (R) in every team name, indicating it's the "Regio" Team."""
    return team_name.replace("(R)", "").strip()


def cells_to_game(cells):
    """Maps the content of 6 <td>s to a calender object."""
    date = cells[1].text
    location = cells[2].text
    home_team = tidyR(cells[3].text)
    away_team = tidyR(cells[5].text)
    return Game(date, location, home_team, away_team)


###
# Get the matches
###
doc = open("competitiekalender2021.html")
soup = BeautifulSoup(doc, 'html.parser')

# Every <tr> with 6 children is a game
trs = soup.find_all('tr')
games: List[Game] = []
for t in trs:
    cells = t.find_all('td')
    if len(cells) == 6:
        game = cells_to_game(cells)
        games.append(game)

doc.close()

###
# Filter the matches
###
my_team = tidyR(MY_TEAM)
games = [m for m in games if m.has_participant(
    my_team) and not m.has_participant("bye ")]

###
# Create calendar
###

def parse_datetime(s: str, fmt: str, tz):
    """Parse a string date to a timezone correct datetime"""
    raw_dt = datetime.strptime(m.date, fmt)
    return tzone.localize(raw_dt)


cal = Calendar()
fmt = "%d/%m/%Y %H:%M"
tzone = pytz.timezone("Europe/Brussels")

for m in games:
    event = Event()
    event.add('summary', m.description())
    event_start = parse_datetime(m.date, fmt, tzone)
    event.add('dtstart', event_start)
    event.add('dtend', event_start + timedelta(0, 60 * 60))
    event.add('location', m.location)
    cal.add_component(event)

###
# Write to output file
###
f = open('handbal.ics', 'wb')
f.write(cal.to_ical())
f.close()
