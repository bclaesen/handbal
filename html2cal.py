#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 11:29:07 2017

@author: Bert
"""
from bs4 import BeautifulSoup
from datetime  import datetime, timedelta
from icalendar import Calendar, Event
import pytz

MY_TEAM = "Real Kiewit (R) "

def tidyR(team_name):
    """
    Clean up the (R) in every team name, indicating it's the "Regio" Team
    """
    return team_name.replace("(R)", "").strip()

def cells_to_game(cells):
    """
    maps the content of 6 <td>s to a calender object
    """
    match = {}
    match["Date"] = cells[1].text
    match["Location"] = cells[2].text
    home_team = tidyR(cells[3].text)
    away_team = tidyR(cells[5].text)
    match["Game"] = f"{home_team}-{away_team}"
    return match

###
###Get the matches
###
doc = open("competitiekalender2021.html")
soup = BeautifulSoup(doc, 'html.parser')

#Every <tr> with 6 children is a game
trs = soup.find_all('tr')
games = []
for t in trs:
    cells = t.find_all('td')
    if len(cells) == 6:
        game = cells_to_game(cells)
        games.append(game)

doc.close()
   
###
### Filter the matches
###
games = [m for m in games if m["Game"].find(tidyR(MY_TEAM)) != -1 and m["Game"].find("bye ")==-1]
           
###
### Create calendar
###
cal = Calendar()
fmt = "%d/%m/%Y %H:%M"
tzone = pytz.timezone("Europe/Brussels")

for m in games:
    event = Event()
    event.add('summary', m["Game"])
    event_start = datetime.strptime(m["Date"],fmt)  
    event_start = tzone.localize(event_start)
    event_end = event_start + timedelta(0,60 * 60)
    event.add('dtstart', event_start)
    event.add('dtend', event_end)
    event.add('location', m["Location"])
    cal.add_component(event)

###    
### Write to output file
###
f = open('handbal.ics', 'wb')
f.write(cal.to_ical())
f.close()
