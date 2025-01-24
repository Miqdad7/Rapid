from django.urls import path
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
    path('create-program-level/', views.create_program_level, name='create_program_level'),
    path('create-teacher/', views.create_teacher, name='create_teacher'),
    path('create-role/', views.create_role, name='create_role'),
    path('create-user/', views.create_user, name='create_user'),
    
    # List views
    path('course-list/', views.course_list, name='course_list'),
    path('student-list/', views.student_list, name='student_list'),
    path('program-list/', views.program_list, name='program_list'),
    path('department-list/', views.department_list, name='department_list'),
    path('program-level-list/', views.program_level_list, name='program_level_list'),
    path('teacher-list/', views.teacher_list, name='teacher_list'),
    path('role-list/', views.role_list, name='role_list'),
    path('user-list/', views.user_list, name='user_list'),
]
