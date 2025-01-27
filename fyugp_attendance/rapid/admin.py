from django.contrib import admin
from .models import Course
from . models import Student
from .models import Program
from .models import Department
from .models import ProgramLevel
from .models import Teacher
#from .models import Role
#from .models import User

admin.site.register(Course)
admin.site.register(Student)
admin.site.register(Program)
admin.site.register(Department)
admin.site.register(ProgramLevel)
admin.site.register(Teacher)
#admin.site.register(Role)
#admin.site.register(User)

class CourseAdmin(admin.ModelAdmin):
    list_display=('course_id','course_code','course_title','credit','department_id','strength','semester')
    
class StudentAdmin(admin.ModelAdmin):
    list_display = (
        'student_id', 'student_name', 'student_register_number', 'student_admission_number',
        'student_roll_number', 'abc_id', 'email', 'phone', 'gender', 'dob',
        'parent_name', 'parent_mobile_number', 'program_id', 'course'
    )
    search_fields = ('student_name', 'student_register_number', 'email', 'phone')
    list_filter = ('gender', 'dob', 'course')

class ProgramAdmin(admin.ModelAdmin):
    list_display = ('program_id', 'program_name', 'department_id', 'program_level_id')
    search_fields = ('program_name',)
    
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('department_id', 'department_name')
    search_fields = ('department_name')

class ProgramLevelAdmin(admin.ModelAdmin):
    list_display = ('program_level_id', 'program_level_name')
    search_fields = ('program_level_name',)
    
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('teacher_id', 'teacher_name', 'user', 'department_id', 'phone', 'email', 'gender')
    search_fields = ('teacher_name', 'email', 'phone')
    list_filter = ('gender',)
    
"""class RoleAdmin(admin.ModelAdmin):
    list_display = ('role_id', 'role_name')
    search_fields = ('role_name',)
    
class UserAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'username', 'role')
    search_fields = ('username',)
    list_filter = ('role',)"""