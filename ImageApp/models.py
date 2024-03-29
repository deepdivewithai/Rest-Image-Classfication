from django.db import models

# Create your models here.
class Profile(models.Model):
    name = models.CharField(max_length=200)
    picture = models.ImageField(upload_to="my_pictures", blank=True, null=True)

    def __str__(self):
        return self.name
