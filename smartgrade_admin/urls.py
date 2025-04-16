from django.urls import path
from . import views

app_name = "smartgrade_admin"

urlpatterns = [
    path('teachers', views.list_teachers, name='teachers'),
    path('teachers/create', views.create_teacher, name='admin_create_teacher'),
    path('teachers/<int:teacher_id>/edit', views.update_teacher, name='admin_update_teacher'),
    path('teachers/<int:teacher_id>/delete', views.delete_teacher, name='admin_delete_teacher'),
    path('teachers/<int:teacher_id>/assign-students', views.assign_students_to_teacher, name='admin_assign_students'),
    path('teachers/<int:teacher_id>/<int:student_id>/unassign-student', views.unassign_student, name='admin_unassign_student'),

    path('students', views.list_students, name='students'),
    path('students/create', views.create_student, name='admin_create_student'),
    path('students/<int:student_id>/edit', views.update_student, name='admin_update_student'),
    path('students/<int:student_id>/delete', views.delete_student, name='admin_delete_student')
]
