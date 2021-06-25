from django.db import models

class BPMN(models.Model):
    id_bpmn = models.AutoField(primary_key=True)
    nama_bpmn = models.CharField(max_length=25, null=False)
    uploaded_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'bpmn'

class UserStories(models.Model):
    id_us = models.AutoField(primary_key=True)
    nama_us = models.CharField(max_length=25, null=False)
    created_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'user_stories'

class TextUserStory(models.Model):
    id_text_us = models.AutoField(primary_key=True)
    text_who = models.CharField(max_length=25, null=False)
    text_what = models.CharField(max_length=25, null=False)
    text_why = models.CharField(max_length=25, null=True)
    nama_us = models.CharField(max_length=25, null=False)

    class Meta:
        db_table = 'text_user_stories'