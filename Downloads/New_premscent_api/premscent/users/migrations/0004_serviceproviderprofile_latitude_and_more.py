# Generated by Django 4.2.16 on 2024-11-16 13:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_remove_serviceproviderprofile_portfolio_images_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='serviceproviderprofile',
            name='latitude',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='serviceproviderprofile',
            name='longitude',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
