from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.contrib import messages

from .models import Teacher, Student, Assessment, Question, Choice, Submission, Answer
from .forms import AssessmentForm, QuestionForm, ChoiceForm, SubmissionForm


def teacher_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'teacher'):
            raise PermissionDenied("Only teachers can access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

def student_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not hasattr(request.user, 'student'):
            raise PermissionDenied("Only students can access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
# @teacher_required
def create_assessment(request):
    """View for teachers to create an assessment"""
    if request.method == "POST":
        form = AssessmentForm(request.POST)
        if form.is_valid():
            assessment = form.save(commit=False)
            assessment.teacher = request.user.teacher
            assessment.save()
            messages.success(request, "Assessment created successfully!")
            return redirect("home_page")
    else:
        form = AssessmentForm()

    return render(request, "assessment/create_assessment.html", {"form": form})

@login_required
@teacher_required
def edit_assessment(request, assessment_id):
    """View for teachers to edit an assessment"""
    assessment = get_object_or_404(Assessment, id=assessment_id, teacher=request.user.teacher)

    if request.method == "POST":
        form = AssessmentForm(request.POST, instance=assessment)
        if form.is_valid():
            form.save()
            messages.success(request, "Assessment updated successfully!")
            return redirect("teacher_dashboard")
    else:
        form = AssessmentForm(instance=assessment)

    return render(request, "assessment/edit_assessment.html", {"form": form, "assessment": assessment})

@login_required
@student_required
def take_assessment(request, assessment_id):
    """View for students to take an assessment"""
    assessment = get_object_or_404(Assessment, id=assessment_id)
    
    # Ensure student is taking an assessment under their assigned teacher
    if assessment.teacher not in request.user.student.teachers.all():
        raise PermissionDenied("You can only take assessments from your assigned teachers.")

    if request.method == "POST":
        submission = Submission.objects.create(student=request.user.student, assessment=assessment)

        for question in assessment.questions.all():
            selected_choices = request.POST.getlist(f"question_{question.id}")
            answer = Answer.objects.create(submission=submission, question=question)
            answer.selected_choices.set(Choice.objects.filter(id__in=selected_choices))

        total_questions = assessment.questions.count()
        correct_answers = sum(answer.is_correct() for answer in submission.answers.all())
        submission.score = (correct_answers / total_questions) * 100
        submission.save()

        messages.success(request, f"Assessment submitted! Your score: {submission.score:.2f}%")
        return redirect("student_dashboard")

    return render(request, "assessment/take_assessment.html", {"assessment": assessment})

@login_required
@teacher_required
def add_question(request, assessment_id):
    """View for teachers to add a question to an assessment"""
    assessment = get_object_or_404(Assessment, id=assessment_id, teacher=request.user.teacher)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.assessment = assessment
            question.save()
            messages.success(request, "Question added successfully!")
            return redirect("edit_assessment", assessment_id=assessment.id)
    else:
        form = QuestionForm()

    return render(request, "assessment/add_question.html", {"form": form, "assessment": assessment})

@login_required
@teacher_required
def add_choice(request, question_id):
    """View for teachers to add a choice to a question"""
    question = get_object_or_404(Question, id=question_id, assessment__teacher=request.user.teacher)

    if request.method == "POST":
        form = ChoiceForm(request.POST)
        if form.is_valid():
            choice = form.save(commit=False)
            choice.question = question
            choice.save()
            messages.success(request, "Choice added successfully!")
            return redirect("edit_assessment", assessment_id=question.assessment.id)
    else:
        form = ChoiceForm()

    return render(request, "assessment/add_choice.html", {"form": form, "question": question})

@login_required
def teacher_dashboard(request):
    """Show list of assessments created by the logged-in teacher"""
    if not hasattr(request.user, "teacher"):
        messages.error(request, "Only teachers can access this page.")
        return redirect("home")

    assessments = Assessment.objects.filter(teacher=request.user.teacher)
    return render(request, "assessment/teacher_dashboard.html", {"assessments": assessments})


@login_required
def assessment_detail(request, assessment_id):
    """Show assessment details with existing questions & allow adding questions"""
    assessment = get_object_or_404(Assessment, id=assessment_id, teacher=request.user.teacher)
    questions = Question.objects.filter(assessment=assessment)

    if request.method == "POST":
        form = QuestionForm(request.POST)
        if form.is_valid():
            question = form.save(commit=False)
            question.assessment = assessment
            question.save()
            messages.success(request, "Question added successfully!")
            return redirect("assessment_detail", assessment_id=assessment.id)
    else:
        form = QuestionForm()

    return render(request, "assessment/assessment_detail.html", {
        "assessment": assessment,
        "questions": questions,
        "form": form
    })
