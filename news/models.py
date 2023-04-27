from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='media',blank=True,null=True)
    image_url = models.URLField(blank=True,null=True)

    def __str__(self):
        return self.title + ' -- ' + str(self.id)
