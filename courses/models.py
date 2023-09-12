from django.db import models

class Course(models.Model):
    name = models.CharField(max_length=200)
    questions = []
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