from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Event(models.Model):
    name = models.CharField(max_length=255, blank=False)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='events_created')
    attendees = models.ManyToManyField(User, related_name='events_attending')

    def __str__(self):
        return self.name
