from django.db import models
from django.contrib.auth.models import User
'''
class Course(models.Model):
    name = models.CharField(max_length=200)
    questions = []
    teacher = models.ForeignKey(User, models.SET_NULL,
    blank=True,
    null=True)
    def __str__(self):
        return self.name

class Question(models.Model):
    text = models.CharField(max_length=200)
    answers = []
    def __str__(self):
        return self.text

class Answer(models.Model):
    text=models.CharField(max_length=200)
    right= models.BooleanField(default=False)
    def __str__(self):
        return self.text
        '''