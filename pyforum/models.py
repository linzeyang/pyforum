from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
    """
    """
    signature = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.username


class Forum(models.Model):
    """
    """
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=200)

    def __unicode__(self):
        return self.title


class Thread(models.Model):
    """
    """
    title = models.CharField(max_length=100)
    forum = models.ForeignKey(Forum)
    time_posted = models.DateTimeField(auto_now_add=True)
    pinned = models.BooleanField(default=False)
    highlighted = models.BooleanField(default=False)
    num_of_clicks = models.IntegerField("have been clicked", default=0)

    class Meta:
        ordering = ['-time_posted']

    def __unicode__(self):
        return self.title


class Post(models.Model):
    """
    """
    title = models.CharField(max_length=100)
    thread = models.ForeignKey(Thread)
    user = models.ForeignKey(User)
    time_posted = models.DateTimeField(auto_now_add=True)
    time_last_modified = models.DateTimeField(auto_now=True)
    content = models.TextField(blank=False)

    def __unicode__(self):
        return self.title

    def ever_modified(self):
        return self.time_last_modified > self.time_posted
