from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=50)
    label = models.SlugField(unique=True)

    def __str__(self):
        return self.label


class Message(models.Model):
    room = models.ForeignKey(Room, related_name='messages')
    handle = models.CharField(max_length=50)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)

    def __str__(self):
        return f'[{self.timestamp}] {self.handle}: {self.message}'

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')
