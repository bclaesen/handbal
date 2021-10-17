#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Copyright Bert Claesen 2017-2021

@author: Bert Claesen
@email: bert@imperfection.be
"""
import argparse
from bs4 import BeautifulSoup, PageElement
from dataclasses import dataclass
from datetime import datetime, timedelta, tzinfo
from icalendar import Calendar, Event
from result import Result, Ok, Err
from typing import List
from pytz import timezone
from sys import stderr

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


def parse_datetime(s: str, fmt: str, tz: tzinfo) -> Result[datetime, str]:
    """Parse a string date to a timezone correct datetime"""
    try:
        raw_dt = datetime.strptime(game.date, fmt)
    except ValueError:
        return Err(f"Unexpected date format: {s}")
    return Ok(tzone.localize(raw_dt))


def game_to_event(game: Game, fmt: str, tz: tzinfo) -> Result[Event, str]:
    """Get a calender event for a game."""
    event = Event({
        'summary': game.description(),
        'location': game.location,
    })
    # Adding the timestamps with Event::add, as this seems to nicely set the timezone
    event_start_or_err = parse_datetime(game.date, fmt, tzone)
    if event_start_or_err.is_err():
        return Err(f"Unexpected date format '{game.date}'' for game '{game.description()}'")

    event_start = event_start_or_err.value
    event.add('dtstart', event_start)
    event.add('dtend', event_start + timedelta(hours=1))
    return Ok(event)


def save_calendar_as(calender: Calendar, fname: str = "out.ics"):
    """Save a Calender object to file"""
    with open(fname, 'wb') as f:
        f.write(calender.to_ical())


def parse_handbal_args():
    ap = argparse.ArgumentParser(
        "Convert handbal.be competition calender to iCal format.")
    ap.add_argument("-i", "--input", help="Pathname of input html file",
                    type=str, default="competitiekalender2021.html")
    ap.add_argument("-o", "--output", help="Pathname of output ical file",
                    type=str, default="handbal.ics")
    ap.add_argument("-n", "--teamname",
                    help="Team name to filter for", type=str, default=MY_TEAM)
    ap.add_argument(
        "-s", "--strict", help="Indicate to fail when encountering an error or attempt to create an incomplete output", type=int, choices=[0, 1], default=1)

    return vars(ap.parse_args())


if __name__ == "__main__":
    args = parse_handbal_args()

    def err_or_warn(msg: str):
        """Print and exit on error when strict mode is enabled, else print a warning to stderr and try to continue."""
        exit(f"Error: {msg}") if bool(args["strict"]) else print(
            f"Warning: {msg}", file=stderr)

    all_games = html_to_games(args["input"])
    if 0 == len(all_games):
        err_or_warn(f"Could not find any games in file {args['input']}")

    # Filter for my team
    my_team = tidyR(args["teamname"])
    games = [game for game in all_games if game.has_participant(
        my_team) and not game.has_participant("bye ")]

    if 0 == len(games):
        err_or_warn(
            f"Could not find any games for the team called '{my_team}'.")

    # Convert to calendar
    calendar = Calendar()
    fmt = "%d/%m/%Y %H:%M"
    tzone = timezone("Europe/Brussels")

    for game in games:
        event_or_err = game_to_event(game, fmt, tzone)
        if event_or_err.is_ok():
            calendar.add_component(event_or_err.value)
        else:
            err_or_warn(event_or_err.value)

    # Write output
    save_calendar_as(calendar, args["output"])
