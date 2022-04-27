from django.db import models

# Create your models here.
class Quotes(models.Model):
    quote = models.CharField(max_length=300, blank= False)
    def __str__(self):
        return self.quote
    