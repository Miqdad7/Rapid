from django.contrib import admin
from .models import Course
from . models import Student
from .models import Program
from .models import Department
from .models import StudentCourse
from .models import Teacher
from .models import TeacherCourse,AbsentDetails,HourDateCourse
from django.contrib.auth.models import Group
#from .models import Role
#from .models import User

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Program)
admin.site.register(Department)
admin.site.register(StudentCourse)
admin.site.register(Teacher)
admin.site.register(TeacherCourse)

#admin.site.register(Role)
#admin.site.register(User)

class CourseAdmin(admin.ModelAdmin):
    list_display=('course_id','course_code','course_title','credit','department_id','semester')
    
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'student_name', 'student_register_number', 'student_admission_number',
        'program_id','department_id')
    search_fields = ('student_name', 'student_register_number')
    list_filter = ('department_id')

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_id', 'program_name', 'department_id')
    search_fields = ('program_name',)
    
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name')
    search_fields = ('department_name')

"""class ProgramLevelAdmin(admin.ModelAdmin):
    list_display = ('program_level_id', 'program_level_name')
    search_fields = ('program_level_name',)"""
    
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'teacher_name', 'user', 'department_id', 'phone', 'email')
    search_fields = ('teacher_name', 'email', 'phone')
    list_filter = ('department', 'is_hod')
    
"""class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name')
    search_fields = ('role_name',)
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'role')
    search_fields = ('username',)
    list_filter = ('role',)"""
    
class StudentCourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'student_id', 'course_id')  
    search_fields = ('student__id', 'course__id')  
    list_filter = ('course_id',) 

class TeacherCourseAdmin(admin.ModelAdmin):
    list_display = ('id', 'teacher_id', 'course_id')  
    search_fields = ('teacher__id', 'course__id')  
    list_filter = ('course_id',)
    
# Customizing the admin interface for HourDateCourse model
class HourDateCourseAdmin(admin.ModelAdmin):
    list_display = ('course', 'teacher', 'date', 'hour', 'year')
    search_fields = ('course__name', 'teacher__user__username', 'date')
    list_filter = ('hour', 'year')

admin.site.register(HourDateCourse, HourDateCourseAdmin)

# Customizing the admin interface for AbsentDetails model
class AbsentDetailsAdmin(admin.ModelAdmin):
    list_display = ('student', 'hour_date_course', 'status')
    search_fields = ('student__name', 'hour_date_course__course__name', 'hour_date_course__teacher__user__username')
    list_filter = ('status',)

admin.site.register(AbsentDetails, AbsentDetailsAdmin)