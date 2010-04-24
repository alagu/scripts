# Cricket scores in your (Pidgin) IM Status
# Works with Pidgin (Ubuntu)
# Needs Pidgin compiled with DBus, see "About" in Pidgin to see if "Dbus" is enabled
# python ipl.py <cricinfourl>
# Cricinfo URL has to be the iframe url for scoreboard.
# If cricinfo change their html, this will break :) 
# 
# Alagu (@alagu on twitter)

import dbus
import urllib2
import re
import sys


from BeautifulSoup import BeautifulSoup
url = sys.argv[1]

def remove_html_tags(data):
    p = re.compile(r'<.*?>')
    return p.sub('', data)


response = urllib2.urlopen(url)
html = response.read()
soup = BeautifulSoup(html)
elems = soup.findAll("p" , {"class" : "teamText"})
message =  elems[1].contents[0].replace("Chennai Super Kings","CSK").replace("Deccan Chargers","DC").replace("Bangalore","RCB")
print message

bus = dbus.SessionBus()
obj = bus.get_object("im.pidgin.purple.PurpleService", "/im/pidgin/purple/PurpleObject")
purple = dbus.Interface(obj, "im.pidgin.purple.PurpleInterface")
current = purple.PurpleSavedstatusGetType(purple.PurpleSavedstatusGetCurrent())
# Create new transient status and activate it
status = purple.PurpleSavedstatusNew("", current)
purple.PurpleSavedstatusSetMessage(status, message)
purple.PurpleSavedstatusActivate(status)
