# Generated by Django 4.0.3 on 2023-05-04 09:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('news', '0003_remove_news_image_url_news_add_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='news',
            name='add_time',
            field=models.DateTimeField(null=True),
        ),
    ]
