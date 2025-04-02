from django import forms
from .models import Assessment, Question, Choice, Submission

class AssessmentForm(forms.ModelForm):
    class Meta:
        model = Assessment
        fields = ["title", "description"]

class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ["text", "question_type"]

class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ["text", "is_correct"]

class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = []
