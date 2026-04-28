from django.db import models

class Hospital(models.Model):
    name = models.CharField(max_length=200)
    participation_rate = models.IntegerField(default=0) # For the 98%, 84% bars
    last_sync = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
