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

def tidyR(s):
        return s.replace("(R)", "").strip()

###
###Get the matches
###
doc = open("competitiekalender2021.html")
soup = BeautifulSoup(doc, 'html.parser')
soup.find_all('a')
#elke tr met 6 kinderen
trs = soup.find_all('tr')
matches = []
for t in trs:
    cells = t.find_all('td')
    if len(cells) == 6:
        match = {}
        match["Date"] = cells[1].text
        match["Location"] = cells[2].text
        match["Game"] = tidyR(cells[3].text) + "-" + tidyR(cells[5].text)

        #match["Game"] = match["Game"].replace("(R)", "")
        #match["Game"] = match["Game"].strip()
        matches.append(match)
        
   
###
### Filter the matches
###
matches = [m for m in matches if m["Game"].find(tidyR("Real Kiewit (R) ")) != -1 and m["Game"].find("bye ")==-1]
           
#for m in matches:
#    print("{}: {} // {}".format(m['Date'],m['Game'],m['Location']))
    
###
### Create calendar
###
#29 okt 2017 is DST terug weg
#25 maart 2018 is DST er weer
cal = Calendar()
fmt = "%d/%m/%Y %H:%M"
tzone = pytz.timezone("Europe/Brussels")
dststart = datetime(2018,10,28,2)
dstend = datetime(2019,3,31,2)
for m in matches:
    event = Event()
    event.add('summary', m["Game"])
    dtstart = datetime.strptime(m["Date"],fmt)  
    dtstart = tzone.localize(dtstart)
    dtend = dtstart + timedelta(0,60*60)
    event.add('dtstart', dtstart)
    event.add('dtend', dtend)
    #event.add('description', row['Activity'])
    event.add('location', m["Location"])
    cal.add_component(event)
    
    #write it
f = open('handbal.ics', 'wb')
f.write(cal.to_ical())
f.close()
