from django.db import models
from django.contrib.auth.models import User
from datetime import date

def calculate_year(current_date):
    """
    Calculate the academic year based on the date.
    June 1 of a year to May 31 of the next year is considered the same academic year.
    """
    if current_date.month >= 6:  # From June to December
        return current_date.year
    else:  # From January to May
        return current_date.year - 1
    
    
class Department(models.Model):
    department_id=models.AutoField(primary_key=True)
    department_name=models.CharField(max_length=100)
    
    def __str__(self):
        return self.department_name

class Course(models.Model):
    SEMESTER_CHOICES = [
        ('1', 'First Semester'),
        ('2', 'Second Semester'),
        ('3', 'Third Semester'),
        ('4', 'Fourth Semester'),
        ('5', 'Fifth Semester'),
        ('6', 'Sixth Semester'),
        ('7', 'Seventh Semester'),
        ('8', 'Eighth Semester'),
    ]
    course_id = models.AutoField(primary_key=True)
    course_code = models.CharField(max_length=20, unique=True)
    course_title = models.CharField(max_length=100)
    credit = models.DecimalField(max_digits=4, decimal_places=2)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    semester = models.CharField(max_length=1, choices=SEMESTER_CHOICES)
    

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
    #student_roll_number = models.CharField(max_length=20, unique=True)
    #abc_id = models.IntegerField()
    #email = models.EmailField(unique=True)
    #phone = models.CharField(max_length=15)
    #gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    #dob = models.DateField()
    #parent_name = models.CharField(max_length=100)
    #parent_mobile_number = models.CharField(max_length=15)
    program_id = models.ForeignKey(Program, on_delete=models.CASCADE)   
    #course_id = models.ForeignKey(Course, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.student_name

    
class Teacher(models.Model):
    teacher_id = models.AutoField(primary_key=True)
    teacher_name = models.CharField(max_length=100)
    user_id = models.OneToOneField(User, on_delete=models.CASCADE)
    department_id = models.ForeignKey(Department, on_delete=models.CASCADE)
    phone = models.CharField(max_length=15, unique=True)
    email = models.EmailField(unique=True)
    gender = models.CharField(max_length=10, choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')])
    is_hod = models.BooleanField(default=False)  # New field to mark HODs

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
    year = models.PositiveIntegerField(editable=False)  # Year is non-editable
    
    class Meta:
        db_table = 'teacher_course'  # Custom table name
        unique_together = ('teacher_id', 'course_id', 'year')  # Prevent duplicate entries for the same student and course
        verbose_name = 'Teacher Course'
        verbose_name_plural = 'Teacher Courses'
        
    def save(self, *args, **kwargs):
        # Calculate and set the year dynamically
        self.year = calculate_year(date.today())
        super().save(*args, **kwargs)
    
    

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
    
    
class HourDateCourse(models.Model):
    HOUR_CHOICES = [
        (1, 'Hour 1'),
        (2, 'Hour 2'),
        (3, 'Hour 3'),
        (4, 'Hour 4'),
        (5, 'Hour 5'),
    ]
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    date = models.DateField()
    hour = models.PositiveSmallIntegerField(choices=HOUR_CHOICES)  # Restrict to valid choices
    year = models.PositiveIntegerField(editable=False)  # Year is non-editable

    class Meta:
        unique_together = ('course', 'date', 'hour')  # Ensure only one teacher can mark attendance

    def save(self, *args, **kwargs):
        # Calculate the year based on the date field
        self.year = calculate_year(self.date)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.teacher.user_id.teacher} - {self.course.course_title} - {self.date} Hour {self.hour} - Year {self.year}"
    
class AbsentDetails(models.Model):
    hour_date_course = models.ForeignKey(HourDateCourse, on_delete=models.CASCADE)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    status = models.BooleanField(default=False)  # False for absent, True for present

    class Meta:
        unique_together = ('student', 'hour_date_course')

    def __str__(self):
        return f"{self.student.student_name} - {self.hour_date_course} - {'Present' if self.status else 'Absent'}"