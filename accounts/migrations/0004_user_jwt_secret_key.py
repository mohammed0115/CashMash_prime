# Generated by Django 3.1.5 on 2021-03-26 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_remove_user_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='jwt_secret_key',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
