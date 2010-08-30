import os
import time
import threading
import urllib
import Queue
import sys
from time import strftime
time = [
        '_07_00','_07_15','_07_30','_07_45',
        '_08_00','_08_15','_08_30','_08_45',
        '_09_00','_09_15','_09_30','_09_45',
       ]


class ProcessItem ( threading.Thread ):

    def __init__ (self, queue):
        threading.Thread.__init__(self)
        self.queue = queue

    def run ( self ):
        while True:
            download = True
            filename = self.queue.get()
            if len(sys.argv) > 1 :
                folder = sys.argv[1]
            else:
                folder = strftime("%Y_%m_%d_%A")
            if folder == 'nodownload':
                folder = strftime("%Y_%m_%d_%A")
                print 'nodownlload' + folder + filename 
                download = False
                
            baseurl = 'http://alagu.net/stream/' + folder + '/'
            self.filename = folder + filename + '.asf'
            self.baseurl  = baseurl
            print '[QUEUE] ' + self.filename
            fullname =  self.baseurl + self.filename
            if (download and (not os.path.isfile(self.filename)) or (os.path.getsize(self.filename) < 3677680)):
                print '[DOWNLOADING] ' + self.filename
                try:
                    f,status = urllib.urlretrieve(fullname, self.filename)
                except IOError:
                    print "No internet connection"
                    os._exit(1)
                item_list = status.items()
                for i in status.items():
                    if(i[0] == 'content-type'):
                        if(i[1].find('text/html') != -1):
                            print '[DELETE] ' +  self.filename
                            os.remove(self.filename)
                            self.queue.task_done()
                            return
                print '[DOWNLOADED] ' + self.filename

            if (not os.path.isfile(self.filename + '.wav') or os.path.getsize(self.filename + '.wav') < 79090400):
                print '[WAV] ' + self.filename 
                mplayercmd = 'mplayer -really-quiet -vc null -vo null -ao pcm:file=%s.wav pcm:fast pcm:waveheader %s' % (self.filename, self.filename)
                os.system(mplayercmd)

            if (not os.path.isfile(self.filename + '.wav.mp3') or os.path.getsize(self.filename + '.wav.mp3') < 7192800):
                print '[MP3] ' + self.filename 
                lamecmd    = 'lame --quiet %s.wav' % (self.filename)
                os.system(lamecmd)

            print '[DONE] ' + self.filename 
            self.queue.task_done()
        

q = Queue.Queue()

for i in range(2):
    t = ProcessItem(q)
    t.setDaemon(True)
    t.start()

for t in time:
     q.put(t)

q.join()
#os.system('rm *.wav');
if len(sys.argv) > 1 :
    todayprogram = sys.argv[1]
else:
    todayprogram = strftime("%Y_%m_%d_%A")
os.system('cat *.mp3 > ' + todayprogram + '.mp3')
#os.system('rm *.wav.mp3');
print "\nYour file is " +todayprogram+".mp3. Thanks for flying!\n"
