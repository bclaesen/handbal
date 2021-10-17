#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright Bert Claesen 2017-2021

@author: Bert Claesen
@email: bert@imperfection.be
"""
from bs4 import BeautifulSoup, PageElement
from dataclasses import dataclass
from datetime import datetime, timedelta, tzinfo
from icalendar import Calendar, Event
from typing import List
from pytz import timezone

MY_TEAM = "Real Kiewit (R) "


@dataclass
class Game:
    """Keep track of game specific information."""
    date: str
    location: str
    home_team: str
    away_team: str

    def description(self) -> str:
        """Describes a game with its home and away team."""
        return f"{self.home_team}-{self.away_team}"

    def has_participant(self, team_name: str) -> bool:
        """Indicate if a team is playing in this game or not."""
        return self.home_team == team_name or self.away_team == team_name

def tidyR(team_name: str) -> str:
    """Clean up the "(R)" in every team name, indicating it's the "Regio" Team."""
    return team_name.replace("(R)", "").strip()


def cells_to_game(cells: List[PageElement]) -> Game:
    """Maps the content of 6 TDs to a calender object."""
    assert(6 == len(cells))
    date, location = cells[1].text, cells[2].text
    home_team = tidyR(cells[3].text)
    away_team = tidyR(cells[5].text)
    return Game(date, location, home_team, away_team)


def html_to_games(input_fname: str) -> List[Game]:
    """Parse input html file and generate a list of games."""
    games: List[Game] = []
    with open(input_fname) as doc:
        soup = BeautifulSoup(doc, 'html.parser')

        # Every <tr> with 6 children is a game
        trs: List[PageElement] = soup.find_all('tr')
        for t in trs:
            cells = t.find_all('td')
            if len(cells) == 6:
                game = cells_to_game(cells)
                games.append(game)

    return games


def parse_datetime(s: str, fmt: str, tz: tzinfo) -> datetime:
    """Parse a string date to a timezone correct datetime"""
    raw_dt = datetime.strptime(game.date, fmt)
    return tzone.localize(raw_dt)


def game_to_event(game: Game, fmt: str, tz: tzinfo) -> Event:
    """Get a calender event for a game."""
    event = Event({
        'summary': game.description(),
        'location': game.location
    })
    # Adding the timestamps with Event::add, as this seems to nicely set the timezone
    event_start = parse_datetime(game.date, fmt, tzone)
    event.add('dtstart', event_start)
    event.add('dtend', event_start + timedelta(hours=1))
    return event


def save_calendar_as(calender: Calendar, fname: str = "out.ics"):
    """Save a Calender object to file"""
    with open(fname, 'wb') as f:
        f.write(calender.to_ical())


if __name__ == "__main__":
    all_games = html_to_games("competitiekalender2021.html")

    # Filter for my team
    my_team = tidyR(MY_TEAM)
    games = [game for game in all_games if game.has_participant(
        my_team) and not game.has_participant("bye ")]

    # Convert to calendar
    calendar = Calendar()
    fmt = "%d/%m/%Y %H:%M"
    tzone = timezone("Europe/Brussels")

    for game in games:
        event = game_to_event(game, fmt, tzone)
        calendar.add_component(event)

    # Write output
    save_calendar_as(calendar, 'handbal.ics')
