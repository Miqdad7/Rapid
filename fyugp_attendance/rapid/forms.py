from django import forms
from django.contrib.auth.models import User
from .models import Course, Student, Program, Department, Teacher, StudentCourse, TeacherCourse

# Form for Department model
class DepartmentForm(forms.ModelForm):
    class Meta:
        model = Department
        fields = ['department_id', 'department_name']

# Form for Course model
class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['course_id', 'course_code', 'course_title', 'credit', 'department_id', 'strength','year_offered']
        


# Form for ProgramLevel model
"""class ProgramLevelForm(forms.ModelForm):
    class Meta:
        model = ProgramLevel
        fields = ['program_level_id','program_level_name']"""

# Form for Program model
class ProgramForm(forms.ModelForm):
    class Meta:
        model = Program
        fields = ['program_id','program_name', 'department_id']
        

# Form for Student model
class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['student_name', 'student_register_number', 'student_admission_number', 'student_roll_number',
                   'gender','program_id','department_id']
        widgets = {
            #'dob': forms.DateInput(attrs={'type': 'date'}),
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]),
            
        }

# Form for Role model
"""class RoleForm(forms.ModelForm):
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
        }"""

# Form for Teacher model
"""class TeacherForm(forms.ModelForm):
    class Meta:
        model = Teacher
        fields = ['teacher_id','teacher_name', 'user_id', 'department_id', 'phone', 'email', 'gender']
        widgets = {
            'gender': forms.Select(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
        }"""




class TeacherForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=True, help_text="Set a password for the teacher.")

    class Meta:
        model = Teacher
        fields = ['teacher_id','teacher_name', 'department_id', 'phone', 'email', 'gender']

    def save(self, commit=True):
        # Save the user instance
        teacher = super().save(commit=False)
        
        if teacher.pk:
            if teacher.user_id:
                teacher.user_id.delete()
        
        # Create the corresponding user
        user = User.objects.create_user(
            username=self.cleaned_data['teacher_name'],  # Use email as username
            email=self.cleaned_data['email'],
            password=self.cleaned_data['password'],  # Set the password
        )
        teacher.user_id = user  # Link the teacher to the user
        
        if commit:
            teacher.save()
        
        return teacher

class StudentCourseForm(forms.ModelForm):
    class Meta:
        model = StudentCourse
        fields = ['student_id', 'course_id']  # Fields to include in the form
        widgets = {
            'student_id': forms.Select(attrs={'class': 'form-control'}),
            'course_id': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'student_id': 'Student',
            'course_id': 'Course',
        }
        help_texts = {
            'student_id': 'Select the student to enroll.',
            'course_id': 'Select the course for enrollment.',
        }
class TeacherCourseForm(forms.ModelForm):
    class Meta:
        model = TeacherCourse
        fields = ['teacher_id', 'course_id']  # Fields to include in the form
        widgets = {
            'teacher_id': forms.Select(attrs={'class': 'form-control'}),
            'course_id': forms.Select(attrs={'class': 'form-control'}),
        }
        labels = {
            'teacher_id': 'Teacher',
            'course_id': 'Course',
        }
        help_texts = {
            'teacher_id': 'Select the Teacher to enroll.',
            'course_id': 'Select the course for enrollment.',
        }
