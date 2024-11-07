import uuid
from django.db import models
from accounts.models import User, AccessToken


class Question(models.Model):
    question_id = models.UUIDField(
        unique=True, primary_key=True, default=uuid.uuid4
    )
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    theme = models.CharField(max_length=40)
    question_text = models.TextField()
    choice1 = models.CharField(max_length=40)
    choice2 = models.CharField(max_length=40)

    def __str__(self):
        return self.theme
    
class User_Answer(models.Model):
    answer_id = models.CharField(max_length=10,primary_key=True)
    question_id = models.ForeignKey(Question, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
    choices = [
        ('1', 'choice1'),
        ('2', 'choice2')
    ]
    user_choice = models.CharField(max_length=1, choices=choices)
    choice_reason = models.TextField()
