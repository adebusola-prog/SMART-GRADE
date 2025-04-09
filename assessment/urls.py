from django.urls import path
from .views import (create_assessment, edit_assessment, 
                    take_assessment, add_choices, add_question, 
                    teacher_dashboard, assessment_detail, QuestionEditView)

app_name = "assessment"

urlpatterns = [
    path("create", create_assessment, name="create_assessment"),
    path("teacher/dashboard", teacher_dashboard, name="teacher_dashboard"),
    path("<int:assessment_id>", assessment_detail, name="assessment_detail"),
    path("<int:assessment_id>/edit", edit_assessment, name="edit_assessment"),
    path("<int:assessment_id>/take", take_assessment, name="take_assessment"),
    path("<int:assessment_id>/add-question", add_question, name="add_question"),
    path("<int:question_id>/add-choice", add_choices, name="add_choices"),
    path('question/<int:pk>/edit/', QuestionEditView.as_view(), name='edit_question'),
]

