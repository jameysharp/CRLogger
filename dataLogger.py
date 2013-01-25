import os
os.environ['DJANGO_SETTINGS_MODULE'] = "logger.settings"

from logapp.models import LogData
import const
import pData
from django.db import transaction
from itertools import *
import sys

logName = const.logName

def resumeCheck():
    """This looks for the highest 'id' in the database and returns the tell associated 
    with it.  This may be imporved by adding an index to the id field, but I'm really
    not sure."""
    try:
        entry = LogData.objects.latest('id')
    except LogData.DoesNotExist:
        return 0
    return entry.tellMarker

def logDataCheck(startPos):
    """Need to modify this to act inside of a loop.  Will get to that later."""
    with open(logName, 'r') as f:
        f.seek(startPos)
        nextLines = list(islice(f, const.numLines))
        if not nextLines:
            sys.exit()
        print nextLines
        startPos = f.tell()
        writeData(startPos, pData.processData(nextLines))
            
def writeData(tell, data):
    """Writes the data to the db in block.  A single write for all lines."""
    with transaction.commit_on_success():
        for d in data:
            entry = LogData(tellMarker = tell, processData = d)
            entry.save()

if __name__ == '__main__':
    #add some random lines to the log file and test resume
    import random
    random.seed()
    with open(logName, 'a+') as f:
        for i in range(random.randint(5, 10)):
            f.write("line, " + str(random.randint(1, 100)) + '\n')
    logDataCheck(resumeCheck())
