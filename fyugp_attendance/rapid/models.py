from django.db import models
from django.contrib.auth.models import User
class Department(models.Model):
    department_id=models.AutoField(primary_key=True)
    department_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.department_name

class Course(models.Model):
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=20, unique=True)
    course_title = models.CharField(max_length=100)
    credit = models.DecimalField(max_digits=4, decimal_places=2)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    strength = models.IntegerField()
    #semester = models.IntegerField()
    year_offered = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.course_title 

#class ProgramLevel(models.Model):
#    program_level_id = models.AutoField(primary_key=True)
#    program_level_name = models.CharField(max_length=100, unique=True)

#    def __str__(self):
#        return self.program_level_name

class Program(models.Model):
    program_id = models.AutoField(primary_key=True)
    program_name = models.CharField(max_length=100, unique=True)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    #program_level_id = models.ForeignKey(ProgramLevel, on_delete=models.CASCADE)

    def __str__(self):
        return self.program_name
    
class Student(models.Model):
    student_id = models.AutoField(primary_key=True)
    student_name = models.CharField(max_length=100)
    student_register_number = models.CharField(max_length=20, unique=True)
    student_admission_number = models.CharField(max_length=20, unique=True)
    student_roll_number = models.CharField(max_length=20, unique=True)
    #abc_id = models.IntegerField()
    #email = models.EmailField(unique=True)
    #phone = models.CharField(max_length=15)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    #dob = models.DateField()
    #parent_name = models.CharField(max_length=100)
    #parent_mobile_number = models.CharField(max_length=15)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)   
    #course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.student_name
    
"""class Role(models.Model):
    role_id = models.AutoField(primary_key=True)
    role_name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.role_name"""
    
"""class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=128)  # Storing hashed passwords
    role_id = models.ForeignKey(Role, on_delete=models.CASCADE)

    def __str__(self):
        return self.username"""
    
class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=100)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])

    def __str__(self):
        return self.teacher_name
class StudentCourse(models.Model):
    id = models.AutoField(primary_key=True)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    class Meta:
        db_table = 'student_course'  # Custom table name
        unique_together = ('student_id', 'course_id')  # Prevent duplicate entries for the same student and course
        verbose_name = 'Student Course'
        verbose_name_plural = 'Student Courses'

    def __str__(self):
        return f"Student {self.student_id} enrolled in Course {self.course_id}"
    
class TeacherCourse(models.Model):
    id = models.AutoField(primary_key=True)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'teacher_course'  # Custom table name
        unique_together = ('teacher_id', 'course_id')  # Prevent duplicate entries for the same student and course
        verbose_name = 'Teacher Course'
        verbose_name_plural = 'Teacher Courses'
    
    

    def __str__(self):
        return f"Teacher {self.teacher_id} assigned in Course {self.course_id}"


class Section(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    section_id = models.AutoField(primary_key=True)
    course_id=models.ForeignKey(Course, on_delete=models.CASCADE)
    year=models.IntegerField()
    part=models.IntegerField()
    status = models.CharField(max_length=8, choices=STATUS_CHOICES, default='active')