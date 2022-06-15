from django.db import models
from cloudinary.models import CloudinaryField
# Create your models here.

class Photo(models.Model):
  image = CloudinaryField('image')
  
  
def save_photo(self):
    self.save()  