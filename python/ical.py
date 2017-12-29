#!/usr/bin/env python2

from ics import Calendar
from urllib2 import urlopen
import datetime
import client
import time

while True:

    fh = urlopen("https://events.ccc.de/congress/2017/wiki/index.php/Special:Ask/-5B-5BHas-20object-20type::Event-5D-5D-20-5B-5BHas-20session-20location::Room:Chaos-20West-20Stage-5D-5D/-3FHas-20event-20title%3Dsummary/-3FHas-20start-20time%3Dstart/-3FHas-20end-20time%3Dend/-3FHas-20session-20location%3Dlocation/-3FHas-20url%3Durl/-3FHas-20description%3Ddescription/format%3Dicalendar/limit%3D2342/searchlabel%3DExport-20this-20calendar-20as-20iCal/offset%3D0")
    ical = fh.read()

    cal = Calendar(ical.decode("iso-8859-1"))

    now = datetime.datetime.now()
    for e in cal.events.today():
        if now < e.begin.naive:
            print(e.begin)
            break

    client.write(0,7, "{:13}  {:02}:{:02}  {:<100}".format("Chaos West", e.begin.naive.hour, e.begin.naive.minute, e.name))
    time.sleep(10)
