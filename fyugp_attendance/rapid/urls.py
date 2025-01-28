from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    path('', views.landing, name='landing'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('admin-dashboard/', views.dashboard_view, name='admin_dashboard'),
    path('user-dashboard/', views.dashboard_view, name='user_dashboard'),

    path('create-course/', views.create_course, name='create_course'),
    path('create-student/', views.create_student, name='create_student'),
    path('create-program/', views.create_program, name='create_program'),
    path('create-department/', views.create_department, name='create_department'),
    #path('create-program-level/', views.create_program_level, name='create_program_level'),
    path('create-teacher/', views.create_teacher, name='create_teacher'),
    #path('create-role/', views.create_role, name='create_role'),
    #path('create-user/', views.create_user, name='create_user'),
    
    # List views
    path('course-list/', views.course_list, name='course_list'),
    path('student-list/', views.student_list, name='student_list'),
    path('program-list/', views.program_list, name='program_list'),
    path('department-list/', views.department_list, name='department_list'),
    #path('program-level-list/', views.program_level_list, name='program_level_list'),
    path('teacher-list/', views.teacher_list, name='teacher_list'),
    #path('role-list/', views.role_list, name='role_list'),
    #path('user-list/', views.user_list, name='user_list'),
    
    #edit views
    path('edit-course/<int:pk>/', views.edit_course, name='edit_course'),
    path('edit-teacher/<int:pk>/', views.edit_teacher, name='edit_teacher'),
    path('edit-program/<int:pk>/', views.edit_program, name='edit_program'),
    path('edit-student/<int:pk>/', views.edit_student, name='edit_student'),
    path('edit-department/<int:pk>/', views.edit_department, name='edit_department'),
    path('edit-studentCourse/<int:pk>/', views.edit_studentCourse, name='edit_studentCourse'),
    path('edit-teacherCourse/<int:pk>/', views.edit_teacherCourse, name='edit_teacherCourse'),
    
    #delete views
    path('delete-course/<int:course_id>/', views.delete_course, name='delete_course'),
    path('delete-teacher/<int:teacher_id>/', views.delete_teacher, name='delete_teacher'),
    path('delete-program/<int:program_id>/', views.delete_program, name='delete_program'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('delete-department/<int:department_id>/', views.delete_department, name='delete_department'),
    path('delete-studentCourse/<int:id>/', views.delete_studentCourse, name='delete_studentCourse'),
    path('delete-teacherCourse/<int:id>/', views.delete_teacherCourse, name='delete_teacherCourse'),
    
    
    path('enrollments-list/', views.enroll_student_list, name='enroll_student_list'),
    path('add-enrollments/', views.enroll_student, name='enroll_student'),
    path('assigned-list/', views.assign_teacher_list, name='assign_teacher_list'),
    path('assign-teachers/', views.assign_teacher, name='assign_teacher'),
    
    
    path('logout/', views.custom_logout, name='logout'),
]
