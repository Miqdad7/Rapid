from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    
    #path('', views.landing, name='landing'),
    path('', views.login_view, name='login'),
    path('index', views.index, name='index'),
    path('index-teacher', views.index_teacher, name='index_teacher'),
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
    
    path('course-students/<int:course_id>/', views.course_students, name='course_students'),
    path('course-students-teacher/<int:course_id>/', views.course_students_teacher, name='course_students_teacher'),
    
    path('hod-dashboard/', views.hod_dashboard, name='hod_dashboard'),

    path('course/<int:course_id>/take-attendance/', views.take_attendance, name='take_attendance'),
    
    path('students-list-hod/', views.student_list_hod, name='student_list_hod'),
    path('students-add/', views.add_student, name='add_student'),
    path('edit-student-hod/<int:pk>/', views.edit_student_hod, name='edit_student_hod'),
    path('teacher-list-hod/', views.teacher_list_hod, name='teacher_list_hod'),
    path('add-teacher/', views.add_teacher, name='add_teacher'),
    path('edit-teacher-hod/<int:pk>/', views.edit_teacher_hod, name='edit_teacher_hod'),
    path('course-list-hod', views.course_list_hod, name='course_list_hod'),
    path('course-list-teacher', views.course_list_teacher, name='course_list_teacher'),
    path('add-course/', views.add_course, name='add_course'),
    path('attendance/report/<int:course_id>/', views.attendance_report, name='attendance_report'),
    path('teacher/attendance/', views.teacher_attendance_list, name='teacher_attendance_list'),
    path('teacher/attendance/edit/<int:record_id>/', views.edit_attendance, name='edit_attendance'),
    path('teacher/attendance/remove/<int:record_id>/', views.remove_attendance, name='remove_attendance'),
    path('student-individual-report/<int:student_id>/', views.student_individual_report, name='student_individual_report'),
    path('department/<int:department_id>/', views.department_report, name='department_report'),
    #path('students/upload/', views.upload_students, name='upload_students'),
    #path('download_student_template/', views.download_student_template, name='download_student_template'),
    path('upload-students/', views.upload_students, name='upload_students'),
   
]
