from django.db import models

class LogData(models.Model):
    tellMarker = models.IntegerField()
    processData = models.IntegerField()

    def __unicode__(self):
        return unicode(self.processData)
