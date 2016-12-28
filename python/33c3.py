#!/usr/bin/env python2

import datetime
import time
import client
import urllib2
import json
import logging
from collections import OrderedDict

logging.basicConfig(level=logging.DEBUG)

greeting = "Ein Service des Stratum 0, Hackerspace Braunschweig!"
tick = 0

j = urllib2.urlopen("https://fahrplan.events.ccc.de/congress/2016/Fahrplan/schedule.json")
schedule = json.load(j)

def clear():
    pixels = [0] * client.HEIGHT * client.WIDTH
    client.blit(0,0,client.WIDTH,client.HEIGHT,pixels)

def filter_time(talks):
    for talk in talks:
        p = datetime.datetime.strptime(talk["date"][0:-6],"%Y-%m-%dT%H:%M:%S")
        if p > datetime.datetime.now():
            return talk

while True:
    d = datetime.datetime.now()
    t = d.strftime(" %H:%M")
    delta = d - datetime.datetime(2016,12,27)
    logging.debug("Calculated delta.days: %s", delta)
    if tick > 10:
        j = urllib2.urlopen('https://fahrplan.events.ccc.de/congress/2016/Fahrplan/schedule.json')
        schedule = json.load(j)
        tick = 0
    if schedule:
        client.write(0,0,greeting)
        client.write(client.NUM_SEG_X - len(t), 0, t);
        client.write(0,1,"Fahrplan Version: {}".format(schedule['schedule']['version']))
        saale = ["Saal 1", 'Saal 2', "Saal G", "Saal 6"]
        talks = OrderedDict()
        for saal in saale:
            talks[saal] = schedule['schedule']['conference']['days'][delta.days]['rooms'][saal] 
        i = 3
        f_talk = OrderedDict()
        for saal in talks:
             f_talk[saal] = filter_time(talks[saal])
        logging.debug("f_talk: %s", f_talk)
        for saal in f_talk:
            client.write(0,i,'{} => {} : {:<78}'.format(saal,f_talk[saal]['start'].encode('utf-8').strip(), f_talk[saal]["title"].encode('utf-8').strip()))
            i = i + 1
        client.write(0,8,"        USE MORE BANDWIDTH!")

        time.sleep(0.5)
        tick += 1
