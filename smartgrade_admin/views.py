from django.db import transaction
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.shortcuts import render, redirect, get_object_or_404
from accounts.models import User, Teacher, Student
from .forms import TeacherForm, StudentForm, AssignStudentForm

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.user.is_superuser:
            raise PermissionDenied("Only admin can access this page.")
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@login_required
@admin_required
def list_teachers(request):
    teachers = Teacher.active_objects.all()
    return render(request, 'smartgrade_admin/teachers_list.html', {'teachers': teachers})

@login_required
@admin_required
def list_students(request):
    students = Student.active_objects.all()
    return render(request, 'smartgrade_admin/students_list.html', {'students': students})

@login_required
@admin_required
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    Teacher.objects.create(user=user)
                    messages.success(request, 'Teacher created successfully.')
                    return redirect('smartgrade_admin:teachers')
                    
            except Exception as e:
                messages.error(request, f'Error creating teacher: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = TeacherForm()
    
    return render(request, 'smartgrade_admin/teacher_create.html', {'form': form})

@login_required
@admin_required
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    user = form.save()
                    Student.objects.create(user=user)
                    messages.success(request, 'Student created successfully.')
                    return redirect('smartgrade_admin:students')
            except Exception as e:
                messages.error(request, f'Error creating student: {str(e)}')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = StudentForm()
    return render(request, 'smartgrade_admin/student_create.html', {'form': form})

@login_required
@admin_required
def update_teacher(request, teacher_id):
    teacher = Teacher.active_objects.filter(id=teacher_id).first()
    form = TeacherForm(request.POST or None, instance=teacher.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Teacher updated successfully.')
        return redirect('admin_list_teachers')
    return render(request, 'smartgrade_admin/teachers_form.html', {'form': form})

@login_required
@admin_required
def update_student(request, student_id):
    student = Student.active_objects.filter(id=student_id).first()
    form = StudentForm(request.POST or None, instance=student.user)
    if form.is_valid():
        form.save()
        messages.success(request, 'Student updated successfully.')
        return redirect('admin_list_students')
    return render(request, 'smartgrade_admin/students_form.html', {'form': form})

# @login_required
# @admin_required
# def assign_students_to_teacher(request, teacher_id):
#     teacher = Teacher.active_objects.filter(id=teacher_id).first()
#     form = AssignStudentForm(request.POST, instance=teacher)
#     if form.is_valid():
#         form.save()
#         messages.success(request, 'Students assigned to teacher.')
#         return redirect('smartgrade_admin:teachers')
#     return render(request, 'smartgrade_admin/assign_students.html', {'form': form, 'teacher': teacher})

@login_required
@admin_required
def assign_students_to_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    
    if request.method == 'POST':
        form = AssignStudentForm(request.POST, instance=teacher)
        if form.is_valid():
            form.save()
            messages.success(request, f'Students successfully assigned to {teacher.get_full_name()}')
            return redirect('smartgrade_admin:teachers')
    else:
        form = AssignStudentForm(instance=teacher)

    assigned_students = teacher.students.all()
    
    return render(request, 'smartgrade_admin/assign_students.html', {
        'form': form,
        'teacher': teacher,
        'assigned_students': assigned_students
    })

@login_required
@admin_required
def unassign_student(request, teacher_id, student_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        teacher.students.remove(student)
        messages.success(request, f'{student.user.get_full_name()} unassigned from {teacher.user.get_full_name()}')
    
    return redirect('smartgrade_admin:admin_assign_students', teacher_id=teacher.id)

@login_required
@admin_required
def delete_teacher(request, teacher_id):
    teacher = Teacher.active_objects.filter(id=teacher_id).first()
    teacher.user.is_active = False
    teacher.save()
    messages.success(request, 'Teacher deleted successfully.')
    return redirect('smartgrade_admin:teachers')

@login_required
@admin_required
def delete_student(request, student_id):
    student = Student.active_objects.filter(id=student_id).first()
    student.user.is_active = False
    student.save()
    messages.success(request, 'Student deleted successfully.')
    return redirect('smartgrade_admin:admin_list_students')

