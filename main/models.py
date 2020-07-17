from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
# Create your models here.


class Question(models.Model):
    ques = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username + ' - '+self.ques[:100]


class Answere(models.Model):
    ans = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    ques = models.ForeignKey(Question, on_delete=models.CASCADE)
    date = models.DateTimeField(default=now)

    def __str__(self):
        return self.user.username + ' - '+self.ans[:100]
