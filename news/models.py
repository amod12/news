from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='media',blank=True,null=True)
    add_time=models.DateTimeField(null=True)


    def __str__(self):
        return f'{self.title}   -- {self.id}'
