from django.db import models
from papers.models import university

# Create your models here.
    
class college(models.Model):
    college_name = models.CharField(max_length=50, unique=True)
    university = models.ForeignKey(university, on_delete=models.CASCADE)
    college_logo = models.FileField(upload_to=f"static/institutes/logos/{university}", max_length=100)
    college_website = models.CharField(max_length=100)

    def __str__(self):
        return self.college_name
