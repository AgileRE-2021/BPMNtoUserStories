# Generated by Django 3.1.7 on 2021-06-25 16:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('bpmn_to_us', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='textuserstory',
            name='id_us',
            field=models.IntegerField(default=0, max_length=25),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='userstories',
            name='id_bpmn',
            field=models.IntegerField(default=0, max_length=25),
            preserve_default=False,
        ),
    ]