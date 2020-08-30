from django.dispatch.dispatcher import receiver
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from notes.models import Profile

@receiver(post_save,sender=User)
def save_profile(sender,instance,created,**kwarg):
	if created:
		Profile.objects.create(user=instance,fullname=instance.username)


