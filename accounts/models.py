from django.db import models
from django.contrib.auth.models import User
from base.models import BaseModel
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid
from base.emails import send_account_sctivation_email

class Profile(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    is_email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    profile_image = models.ImageField(upload_to='profile')

    def __str__(self):
        return self.user.username

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        # Create a Profile for the user
        profile = Profile.objects.create(user=instance)
        # Generate email token and save it
        profile.email_token = str(uuid.uuid4())
        profile.save()
        
        # Send activation email
        email = instance.email
        if email:
            send_account_sctivation_email(profile.email_token, email)
