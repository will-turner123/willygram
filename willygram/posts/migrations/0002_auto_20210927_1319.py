# Generated by Django 3.1.7 on 2021-09-27 17:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='image',
            field=models.ImageField(default='default_post.jpg', upload_to='posts'),
        ),
    ]