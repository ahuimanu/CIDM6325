from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    """
    When Django processes this model, 
    it identifies that it has a ManyToManyField on itself
    and does not add a profile_set attribute to the Person class. 
    The ManyToManyField is assumed to be symmetrical 
    if I follow you, then you follow me.
    """
    follows = models.ManyToManyField(
        "self",
        # allowsaccess to data entries from the other end of this relationship 
        # through the descriptive name "followed_by"
        related_name="followed_by",
        # When symmetry in many-to-many relationships with self is not desired, set symmetrical to False.
        symmetrical=False,
        blank=True,
    )

    # shows up better in the admin
    def __str__(self) -> str:
        return self.user.username
    

"""
We also use the signals API in Django to detect whenever a user is created
so that a profile object can automatically be created.
See: https://docs.djangoproject.com/en/4.2/topics/signals/
"""
# Create a profile for each new user
# see: https://docs.djangoproject.com/en/4.2/topics/signals/#receiver-functions
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.add(instance.profile)
        user_profile.save()

