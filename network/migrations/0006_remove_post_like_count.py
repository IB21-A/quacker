# Generated by Django 3.1.5 on 2021-05-01 05:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_post_like_count'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='like_count',
        ),
    ]
