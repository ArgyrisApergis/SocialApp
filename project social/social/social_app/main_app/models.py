from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_resized import ResizedImageField

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    follows = models.ManyToManyField("self", related_name="followed_by", 
    symmetrical=False, blank=True)

    def __str__(self):
        return self.user.username

# connect user + profile when new user is created
@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
        user_profile.follows.set([instance.profile.id])
        user_profile.save()

class Comments(models.Model):
    user = models.ForeignKey(User, related_name="comments", on_delete=models.DO_NOTHING,blank=True)
    body = models.CharField(max_length=140)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return (f"{self.user} "f"({self.created_at:%Y-%m-%d %H:%M})")




class Pet(models.Model):
    name = models.CharField(max_length=120)
    
    def __str__(self):
        return self.name

def upload_gallery_image(instance, filename):
    return f"images/{instance.pet.name}/gallery/{filename}"

class Image(models.Model):
    image = ResizedImageField(size=[400, 400], upload_to=upload_gallery_image)
    pet = models.ForeignKey(Pet, on_delete=models.CASCADE, related_name="images")