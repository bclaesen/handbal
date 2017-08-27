# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 11:29:07 2017

@author: Bert
"""
from bs4 import BeautifulSoup
from datetime  import datetime, timedelta
from icalendar import Calendar, Event
import pytz
from dateutil.parser import parse
###
###Get the matches
###
doc = open("kalender.html")
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
        match["Game"] = cells[3].text + "-" + cells[5].text
        matches.append(match)
        
   
###
### Filter the matches
###
matches = [m for m in matches if m["Game"].find("R. Kiewit") != -1 and m["Game"].find("bye ")==-1]
           
#for m in matches:
#    print("{}: {} // {}".format(m['Date'],m['Game'],m['Location']))
    
###
### Create calendar
###
#29 okt 2017 is DST terug weg
#25 maart 2018 is DST er weer
cal = Calendar()
dststart = datetime(2017,10,29,2)
dstend = datetime(2018,3,25,2)
for m in matches:
    event = Event()
    event.add('summary', m["Game"])
    fmt = "%d/%m/%y  %H:%M"

    tzone = pytz.timezone("Europe/Brussels")
    dtstart = datetime.strptime(m["Date"],fmt)  
    #This math only works because I am running this in Brussels with DST
    if (dtstart-dststart) >= timedelta(hours=0) and (dstend-dtstart >= timedelta(hours=0)):
        dtstart += timedelta(hours=1)
    dtstart -= timedelta(hours=1)
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