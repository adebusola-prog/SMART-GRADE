from django.db import models
from accounts.models import Student, Teacher
from base.models import DeletableBaseModel


class Assessment(DeletableBaseModel):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name="assessments")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title


class Question(DeletableBaseModel):
    QUESTION_TYPES = (
        ('single_choice', 'Single Choice'),
        ('multiple_choice', 'Multiple Choice'),
    )
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="questions")
    text = models.TextField()
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES)

    def __str__(self):
        return self.text


class Choice(DeletableBaseModel):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="choices")
    text = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.text


class Submission(DeletableBaseModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="submissions")
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE, related_name="submissions")
    submitted_at = models.DateTimeField(auto_now_add=True)
    score = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.student.user.email} - {self.assessment.title} - {self.score}"


class Answer(DeletableBaseModel):
    submission = models.ForeignKey(Submission, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name="answers")
    selected_choices = models.ManyToManyField(Choice)

    def is_correct(self):
        """Check if the selected choices match the correct answers"""
        correct_choices = set(self.question.choices.filter(is_correct=True))
        selected_choices = set(self.selected_choices.all())
        return correct_choices == selected_choices
