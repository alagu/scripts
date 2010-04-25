# Cricket scores in your (Pidgin) IM Status
# Works with Pidgin (Ubuntu)
# Needs Pidgin compiled with DBus, see "About" in Pidgin to see if "Dbus" is enabled
# python ipl.py <cricinfourl> <team>
# Cricinfo URL has to be the iframe url for scoreboard.
# <team> is 1 or 2
# If cricinfo change their html, this will break :) 
#
# Run it in a shell loop for updating regularly
#
# Example:
# while [ 1 ]; do python  ipl.py "http://www.cricinfo.com/ipl2010/engine/current/match/419164.html?view=live;wrappertype=live" 1; sleep 15; done
# 
# Alagu (@alagu on twitter)

import dbus
import urllib2
import re
import sys


from BeautifulSoup import BeautifulSoup
url = sys.argv[1]

response = urllib2.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
elems = soup.findAll("p" , {"class" : "teamText"})
team = int(sys.argv[2])-1
message =  elems[team].contents[0].replace("Chennai Super Kings","CSK").replace("Deccan Chargers","DC").replace("Bangalore","RCB").replace("Mumbai Indians","MI")
print message

bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
current = purple.PurpleSavedstatusGetType(purple.PurpleSavedstatusGetCurrent())
# Create new transient status and activate it
status = purple.PurpleSavedstatusNew("", current)
purple.PurpleSavedstatusSetMessage(status, message)
purple.PurpleSavedstatusActivate(status)
