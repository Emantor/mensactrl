#!/usr/bin/env python2
import urllib
from bs4 import BeautifulSoup
import client
from time import sleep
from itertools import islice

score_list = []
ctf_name = ["","","C S","T C","F O","  R","  E","  S","",""]

def populate_scoreboard():
  scoreboard_html = urllib.urlopen('https://33c3ctf.ccc.ac/scoreboard/').read()
  soup = BeautifulSoup(scoreboard_html)
  table = soup.find('table')
  rows = table.findAll('tr',class_='scoreboard_row')
  for tr in rows:
    team = {}
    cols = tr.findAll('td', class_='scoreboard_name')
    for td in cols:
      for link in td.findAll('a'):
        team['name']  = link.text
    cols = tr.findAll('td', class_='scoreboard_score')
    for td in cols:
      team['score'] = td.text.strip()
    cols = tr.findAll('td', class_='scoreboard_rank')
    for td in cols:
      team['rank'] = td.text.strip()
    score_list.append(team)
  return score_list

while True:
  score_list = populate_scoreboard()
  for i in range(0,10):
    client.write(0,i,score_list[i]['rank'].rjust(3) + ". " + score_list[i]['name'].ljust(26) + " : " + score_list[i]['score'].rjust(3)+ "     " + ctf_name[i])
  i = 0
  for teams in islice(score_list,10,None):
    if(i > 9):
      sleep(5)
      i = 0
    client.write(48,i,teams['rank'].rjust(3) + ". " + teams['name'].ljust(26) + " : " + teams['score'].rjust(3))
    i += 1
  
