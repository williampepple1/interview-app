from django.db import models
from django.contrib.auth.models import User

class Assessment(models.Model):
    title = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Question(models.Model):
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    option1 = models.CharField(max_length=200)
    option2 = models.CharField(max_length=200)
    option3 = models.CharField(max_length=200)
    option4 = models.CharField(max_length=200)
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])

    def __str__(self):
        return self.question_text[:50]

class UserAssessment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    started_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    score = models.IntegerField(default=0)
    current_question_index = models.IntegerField(default=0)

    class Meta:
        unique_together = ['user', 'assessment']

class UserResponse(models.Model):
    user_assessment = models.ForeignKey(UserAssessment, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])
    is_correct = models.BooleanField(default=False)
    response_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['user_assessment', 'question']
