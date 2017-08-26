# -*- coding: utf-8 -*-
"""
Created on Sat Aug 26 11:29:07 2017

@author: Bert
"""
from bs4 import BeautifulSoup
from datetime  import datetime, timedelta
from icalendar import Calendar, Event
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
           
for m in matches:
    print("{}: {} // {}".format(m['Date'],m['Game'],m['Location']))
    
###
### Create calendar
###
cal = Calendar()
for m in matches:
    event = Event()
    event.add('summary', m["Game"])
    fmt = "%d/%m/%y  %H:%M"
    #26/11/17  17:30
    #>>> datetime.datetime(2013, 9, 28, 20, 30, 55, 782000)
    
    dtstart = datetime.strptime(m["Date"],fmt)
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