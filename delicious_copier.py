import getpass
from pydelicious import DeliciousAPI, DeliciousItemExistsError
sourceUser   = raw_input("Username [source]: ")
sourcePasswd = getpass.getpass("Password [source]: ")
sourceDlcs   = DeliciousAPI(sourceUser, sourcePasswd)
print "Getting all bookmarks from source:" + sourceUser
sourceBkmrks = sourceDlcs.posts_all()['posts']
print "Done getting bookmarks" 
fromTag  = ' from:' + sourceUser
destUser   = raw_input("Username [destination]: ")
destPasswd = getpass.getpass("Password [destination]: ")
destDlcs   = DeliciousAPI(destUser, destPasswd)
sourceSize = len(sourceBkmrks)

for i in range(46,sourceSize):
	bkmrk = sourceBkmrks[i]
	href  = bkmrk['href']
	desc  = bkmrk['description']
	ext	  = bkmrk['extended'] if 'extended' in bkmrk else ''
	share = bkmrk['shared']  if 'shared' in bkmrk else 'yes'
	date  = bkmrk['time']
	tag   = bkmrk['tag'] if 'tag' in bkmrk else ''
	tag  += fromTag

	print 'Copying (' + str(i+1) + '/' + str(sourceSize) + ') '+ desc + ' (' + href + ')'
	try :
		destDlcs.posts_add(href, desc, extended = ext, tags = tag, dt= date, shared = share)
	except DeliciousItemExistsError:
		desc + ' (' + href  + ') already exists'
