from django import forms
from .models import Course, Student, Program, Department,ProgramLevel, Teacher, Role, User

# Form for Department model
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_id', 'department_name']

# Form for Course model
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'course_code', 'course_title', 'credit', 'department_id', 'strength', 'semester']
        widgets = {
            'semester': forms.Select(choices=[(1, 'Semester 1'), (2, 'Semester 2'), (3, 'Semester 3')])
        }

# Form for ProgramLevel model
class ProgramLevelForm(forms.ModelForm):
    class Meta:
        model = ProgramLevel
        fields = ['program_level_id','program_level_name']

# Form for Program model
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['program_id', 'program_name', 'department_id', 'program_level_id']
        widgets = {
            'program_level_id': forms.Select()
        }

# Form for Student model
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'student_register_number', 'student_admission_number', 'student_roll_number',
                  'abc_id', 'email', 'phone', 'gender', 'dob', 'parent_name', 'parent_mobile_number', 'program_id', 'course_id', 'department_id']
        widgets = {
            'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
        }

# Form for Role model
class RoleForm(forms.ModelForm):
    class Meta:
        model = Role
        fields = ['role_id','role_name']

# Form for User model
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['user_id','username', 'password', 'role_id']
        widgets = {
            'password': forms.PasswordInput()
        }

# Form for Teacher model
class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id','teacher_name', 'user_id', 'department_id', 'phone', 'email', 'gender']
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
        }

