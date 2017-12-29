mport urllib
import json
import client
from time import sleep
import clearscreen

#global foo
minpts = 200
standings = []
header = """ _________      _____      _    __ 
|___ /___ \ ___|___ /  ___| |_ / _|
  |_ \ __) / __| |_ \ / __| __| |_ 
 ___) / __/ (__ ___) | (__| |_|  _|
|____/_____\___|____/ \___|\__|_|  """

# ======
# config
# ======
#x-offset for the scoreboard
xoff = 0 

#y-offset for the scoreboard
yoff = 5

#Width of the banner in the middle
bwidth = 5

width  = 96 - xoff
height = 10 - yoff

colwidth = int((width - bwidth)/2)

if colwidth < 10:
    print "resulting colwidth too low. can't do that :("
    exit()

def loadStandings():
    global standings
    url = "https://32c3ctf.ccc.ac/scoreboard.json"
    resp = urllib.urlopen(url)
    d = json.loads(resp.read())
    standings = d['standings']

def getPretty(i):
    global standings
    global colwidth

    return '{0}. {1} {2}'.format(str(standings[i]['pos']).rjust(3),(standings[i]['team'][:(colwidth-13)]+ (standings[i]['team'][(colwidth-13):] and '...')).ljust(colwidth-9), str(standings[i]['score']).rjust(4))


def drawheader():
    ml = 0
    for l in header.splitlines():
        if len(l) > ml:
            ml = len(l)

    i = 0
    for l in header.splitlines():
        client.write((96-ml)/2,i, l)
        i += 1

    client.write(2,2, "https://32c3ctf.ccc.ac")
    client.write(73,2, "https://32c3ctf.ccc.ac")

clearscreen.clear()
drawheader()

while True:
    loadStandings()

    for i in range(0, height):
        print getPretty(i)
        client.write(xoff,yoff+i, getPretty(i))

    j = 0
    for i in range(height, len(standings)):
        if j == height:
            j = 0
            if standings[i]['score'] < minpts:
                print 'and many more ...'
                client.write(xoff + bwidth + colwidth, yoff + height - 1, '     and many more ...'.ljust(colwidth + 1))
                sleep(12)
                break
            else:
                sleep(4)
                

        print getPretty(i)
        client.write(xoff + bwidth + colwidth, yoff + j, getPretty(i))

        j += 1

