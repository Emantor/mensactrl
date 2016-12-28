#!/usr/bin/env python2

import datetime
import time
import client
import urllib2
import json
import logging
from itertools import islice
from collections import OrderedDict

logging.basicConfig(level=logging.DEBUG)

tick = 11

def clear():
    pixels = [0] * client.HEIGHT * client.WIDTH
    client.blit(0,0,client.WIDTH,client.HEIGHT,pixels)

def filter_time(talks):
    for talk in talks:
        p = datetime.datetime.strptime(talk["date"][0:-6],"%Y-%m-%dT%H:%M:%S")
        if p > datetime.datetime.now():
            return talk

def fetch_scoreboard():
    board_json = urllib2.urlopen("https://33c3ctf.ccc.ac/scoreboard.json")
    return json.load(board_json)

client.write(0,5,"{:<30}".format("CTF Scoreboard (first 5):"))


while True:
    d = datetime.datetime.now()
    t = d.strftime(" %H:%M")
    delta = d - datetime.datetime(2016,12,27)
    logging.debug("Calculated delta.days: %s", delta)
    if tick > 10:
        j = urllib2.urlopen('https://fahrplan.events.ccc.de/congress/2016/Fahrplan/schedule.json')
        schedule = json.load(j)
        teams = fetch_scoreboard()
        tick = 0
        for i in range(5,10):
            team = teams["standings"][i-5]
            client.write(0,i,"{:>1}. {:<29} : {:<4}     ".format(team["pos"],team["team"],team["score"]))
    if schedule:
        saale = ["Saal 1", 'Saal 2', "Saal G", "Saal 6"]
        talks = OrderedDict()
        for saal in saale:
            talks[saal] = schedule['schedule']['conference']['days'][delta.days]['rooms'][saal] 
        i = 0
        f_talk = OrderedDict()
        for saal in talks:
             f_talk[saal] = filter_time(talks[saal])
        logging.debug("f_talk: %s", f_talk)
        for saal in f_talk:
            if f_talk[saal]:
                client.write(0,i,'{} => {} : {:<78}'.format(saal,f_talk[saal]['start'].encode('utf-8').strip(), f_talk[saal]["title"].encode('utf-8').strip()))
            i = i + 1
        time.sleep(0.5)
        tick += 1
