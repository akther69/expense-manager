# Generated by Django 5.0.6 on 2024-08-08 05:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='category',
            unique_together={('name', 'owner')},
        ),
    ]
