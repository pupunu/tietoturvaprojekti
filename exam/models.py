from django.db import models

# Create your models here.

class Answer(models.Model):
    answer_text = models.CharField(max_length=200)
    TF = models.BooleanField(default=False)
    
    def __str__(self):
        return self.answer_text

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    answers = []

    def __str__(self):
        return self.question_text