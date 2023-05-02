from django.db import models

# Create your models here.


class News(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField()
    image = models.ImageField(upload_to='media',blank=True,null=True)
    # add_time=models.DateTimeField(auto_now_add=True)


    def __str__(self):
        return self.title + ' -- ' + str(self.id)
