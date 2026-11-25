from django.shortcuts import get_object_or_404, render, redirect,HttpResponse
from django.http import HttpResponseRedirect,JsonResponse
from django.urls import reverse
from .forms import CourseForm, StudentForm, ProgramForm, DepartmentForm, TeacherForm, StudentCourseForm, TeacherCourseForm, HourDateCourseForm, AbsentDetailsForm, CSVUploadForm
from .models import Course, Student, Program, Department, Teacher, StudentCourse, TeacherCourse, HourDateCourse, AbsentDetails
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User, Group
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from datetime import date
from datetime import datetime
from django.db import IntegrityError
from django.core.exceptions import PermissionDenied
from functools import wraps
from .decorators import hod_required
from .decorators import admin_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from io import TextIOWrapper
import io
import csv

def calculate_year(current_date):
    """
    Calculate the academic year based on the date.
    June 1 of a year to May 31 of the next year is considered the same academic year.
    """
    if current_date.month >= 6:  # From June to December
        return current_date.year
    else:  # From January to May
        return current_date.year - 1
    
def clean_name(name):
    """Standardize the name format: convert to uppercase and replace periods with spaces."""
    return name.strip().replace('.', ' ').upper()

@login_required
@hod_required
def index(request):
    return render(request, 'rapid/index.html')
@login_required
def index_teacher(request):
    return render(request, 'rapid/index_teacher.html')


# Login Page    
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            
            if user.is_superuser:  # Admin login
                return redirect('admin_dashboard')

            try:
                teacher = Teacher.objects.get(user_id=user)
                if teacher.is_hod:
                    return redirect('hod_dashboard')  # Redirect HODs
                else:
                    return redirect('index_teacher')  # Redirect normal teachers
            except Teacher.DoesNotExist:
                return render(request, 'rapid/login.html', {'error': 'Unauthorized access'})  

        else:
            return render(request, 'rapid/login.html', {'error': 'Invalid username or password'})

    return render(request, 'rapid/login.html')


def custom_logout(request):
    logout(request)
    return redirect('login')

def reset_password(request, teacher_id):
    try:
        # Get the Teacher instance by ID
        teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
        
        # Reset the password for the corresponding User
        user = teacher.user_id  # Access the related user (one-to-one relationship)
        user.set_password("12345678")
        user.save()
        
        # Display success message
        messages.success(request, f"Password for teacher {teacher.user_id.username} has been reset.")
        
    except Teacher.DoesNotExist:
        # Handle the case if the teacher doesn't exist
        messages.error(request, "Teacher not found.")
    
    # Redirect back to the admin page or any page you prefer
    return HttpResponseRedirect(reverse('teacher_list_hod'))  # Change to your admin page URL

@login_required
def change_password(request, teacher_id):
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)
    user = teacher.user_id  # Access the associated user object

    if request.method == 'POST':
        form = PasswordChangeForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Keep the user logged in after password change
            messages.success(request, 'Your password has been successfully updated!')

            # Redirect based on role (HOD or normal teacher)
            if teacher.is_hod:
                return redirect('index')  # Redirect to HOD dashboard
            else:
                return redirect('index_teacher')  # Redirect to Teacher dashboard
    else:
        form = PasswordChangeForm(user)
    

    return render(request, 'rapid/change_password.html', {'form': form, 'teacher': teacher})

@login_required
def dashboard_view(request):
    if request.user.is_superuser:  # Admin dashboard
        return render(request, 'rapid/admin_dashboard.html')
    else:
        try:
            # Get the teacher object based on the logged-in user
            teacher = Teacher.objects.get(user_id=request.user)
            # Fetch the courses assigned to this teacher
            assigned_courses = TeacherCourse.objects.filter(teacher_id=teacher) 
            return render(request, 'rapid/user_dashboard.html', {'assigned_courses': assigned_courses})
        except Teacher.DoesNotExist:
            # Handle if the logged-in user is not a teacher (maybe a regular user)
            return redirect('user_dashboard')  # Or any appropriate action for non-teachers

@login_required
def hod_dashboard(request):
    try:
        # Get the logged-in HOD
        hod = Teacher.objects.get(user_id=request.user, is_hod=True)
        department = hod.department_id

        # Get students, teachers, and courses in the same department
        students = Student.objects.filter(department_id=department)
        teachers = Teacher.objects.filter(department_id=department)
        courses = Course.objects.filter(department_id=department)
        #assigned_courses = Course.objects.filter(teachercourse__teacher=hod)
        assigned_courses = Course.objects.filter(course_id__in=TeacherCourse.objects.filter(teacher_id=hod).values_list('course_id', flat=True))
        course_students = {
            course.course_id: StudentCourse.objects.filter(course_id=course).select_related('student')
            for course in courses
        }

        context = {
            'students': students,
            'teachers': teachers,
            'courses': courses,
            'department': department,
            'assigned_courses':assigned_courses,
            'course_students': course_students,
        }
        return render(request, 'rapid/index.html', context)

    except Teacher.DoesNotExist:
        return render(request, 'rapid/login.html', {'error': 'Unauthorized access'})

# View for creating a new course
@login_required
@admin_required
def create_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new course to the database
            return redirect('course_list')  # Redirect to course list page
    else:
        form = CourseForm()  # Create an empty form instance for GET request
    
    return render(request, 'rapid/create_course.html', {'form': form})

# View for creating a new student
@login_required
@admin_required
def create_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the student record to the database
            return redirect('student_list')  # Redirect to student list page
    else:
        form = StudentForm()  # Create an empty form instance for GET request
    
    return render(request, 'rapid/create_student.html', {'form': form})

# View for creating a new program
@login_required
@admin_required
def create_program(request):
    if request.method == 'POST':
        form = ProgramForm(request.POST)
        if form.is_valid():
            form.save()  # Save the program to the database
            return redirect('program_list')  # Redirect to program list page
    else:
        form = ProgramForm()
    
    return render(request, 'rapid/create_program.html', {'form': form})

# View for creating a new department
@login_required
@admin_required
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the department to the database
            return redirect('department_list')  # Redirect to department list page
    else:
        form = DepartmentForm()
    
    return render(request, 'rapid/create_department.html', {'form': form})

# View for creating a new teacher
@login_required
@admin_required
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()  # Save the teacher to the database
            return redirect('teacher_list')  # Redirect to teacher list page
    else:
        form = TeacherForm()
    
    return render(request, 'rapid/create_teacher.html', {'form': form})

@login_required
@admin_required
def enroll_student(request):
    if request.method == 'POST':
        form = StudentCourseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('enroll_student_list')  # Replace with your success URL
    else:
        form = StudentCourseForm()

    return render(request, 'rapid/enroll_student.html', {'form': form})

@login_required
def assign_teacher(request):
    user = request.user
    
    # Ensure the logged-in user is an HOD
    try:
        hod = Teacher.objects.get(user_id=user, is_hod=True)
    except Teacher.DoesNotExist:
        messages.error(request, "You are not authorized to assign courses.")
        return redirect('hod_dashboard')  # Redirect HOD to their dashboard

    if request.method == 'POST':
        form = TeacherCourseForm(request.POST)
        if form.is_valid():
            teacher = form.cleaned_data['teacher_id']
            course = form.cleaned_data['course_id']

            # Ensure that the selected teacher and course belong to the HOD's department
            if teacher.department_id != hod.department_id or course.department_id != hod.department_id:
                messages.error(request, "You can only assign teachers and courses from your department.")
            else:
                form.save()
                messages.success(request, f"{teacher.teacher_name} assigned to {course.course_title}.")
                return redirect('assign_teacher_list')  # Redirect to success page
    else:
        # Limit form choices to only the HOD's department teachers and courses
        form = TeacherCourseForm()
        form.fields['teacher_id'].queryset = Teacher.objects.filter(department_id=hod.department_id)
        form.fields['course_id'].queryset = Course.objects.filter(department_id=hod.department_id)

    return render(request, 'rapid/assign_teacher.html', {'form': form})

# List view for all courses
@login_required
@admin_required
def course_list(request):
    courses = Course.objects.all()  # Fetch all courses from the database
    departments = Department.objects.all()  # Fetch all departments
    return render(request, 'rapid/course_list.html', {'courses': courses,"departments": departments})


# List view for all students
@login_required
@admin_required
def student_list(request):
    students = Student.objects.all()  # Fetch all students from the database
    departments = Department.objects.all()  # Fetch all departments
    return render(request, 'rapid/student_list.html', {'students': students,"departments": departments})

# List view for all programs
@login_required
@admin_required
def program_list(request):
    programs = Program.objects.all()  # Fetch all programs from the database
    return render(request, 'rapid/program_list.html', {'programs': programs})

# List view for all departments
@login_required
@admin_required
def department_list(request):
    departments = Department.objects.all()  # Fetch all departments from the database
    return render(request, 'rapid/department_list.html', {'departments': departments})

# List view for all teachers
@login_required
@admin_required
def teacher_list(request):
    teachers = Teacher.objects.all()  # Fetch all teachers from the database
    departments = Department.objects.all()  # Fetch all departments
    return render(request, 'rapid/teacher_list.html', {'teachers': teachers,"departments": departments})

@login_required
@admin_required
def enroll_student_list(request):
    enrollments = StudentCourse.objects.select_related('student_id', 'course_id').all()
    return render(request, 'rapid/enroll_student_list.html', {'enrollments': enrollments})

@login_required
def assign_teacher_list(request):
    user = request.user

    # Ensure the logged-in user is an HOD
    try:
        hod = Teacher.objects.get(user_id=user, is_hod=True)
    except Teacher.DoesNotExist:
        messages.error(request, "You are not authorized to view assigned courses.")
        return redirect('hod_dashboard')  # Redirect unauthorized users
    department=hod.department_id

    # Get only assignments related to the HOD's department
    assigns = TeacherCourse.objects.filter(
        teacher_id__department_id=hod.department_id
    ).select_related('teacher_id', 'course_id')

    return render(request, 'rapid/assign_teacher_list.html', {'assigns': assigns, 'department': department})

#editting tables

@login_required
@admin_required
def edit_course(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if request.method == "POST":
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            return redirect('course_list')
        else:
            print("Form Errors:", form.errors)  # Debug form validation issues
    else:
        form = CourseForm(instance=course)
    return render(request, 'rapid/edit_course.html', {'form': form})

@login_required
@admin_required
def edit_teacher(request, pk):
    # Retrieve the teacher object by its ID
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            # Save the teacher instance and the related user information
            form.save()
            messages.success(request, "Teacher information updated successfully!")
            return redirect('teacher_list')  # Redirect to the teacher list or another page
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'rapid/edit_teacher.html', {'form': form})

@login_required
@admin_required
def edit_program(request, pk):
    program = get_object_or_404(Program, pk=pk)
    if request.method == "POST":
        form = ProgramForm(request.POST, instance=program)
        if form.is_valid():
            form.save()
            return redirect('program_list')
        else:
            print("Form Errors:", form.errors)  # Debug form validation issues
    else:
        form = ProgramForm(instance=program)
    return render(request, 'rapid/edit_program.html', {'form': form})

@login_required
@admin_required
def edit_student(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list')
        else:
            print("Form Errors:", form.errors)  # Debug form validation issues
    else:
        form = StudentForm(instance=student)
    return render(request, 'rapid/edit_student.html', {'form': form})

@login_required
@admin_required
def edit_department(request, pk):
    department = get_object_or_404(Department, pk=pk)
    if request.method == "POST":
        form = DepartmentForm(request.POST, instance=department)
        if form.is_valid():
            form.save()
            return redirect('department_list')
        else:
            print("Form Errors:", form.errors)  # Debug form validation issues
    else:
        form = DepartmentForm(instance=department)
    return render(request, 'rapid/edit_department.html', {'form': form})

@login_required
@admin_required
def edit_studentCourse(request, pk):
    studentCourse = get_object_or_404(StudentCourse, pk=pk)
    if request.method == "POST":
        form = StudentCourseForm(request.POST, instance=studentCourse)
        if form.is_valid():
            form.save()
            return redirect('enroll_student_list')
        else:
            print("Form Errors:", form.errors)  # Debug form validation issues
    else:
        form = StudentCourseForm(instance=studentCourse)
    return render(request, 'rapid/edit_enroll_student_list.html', {'form': form})

@login_required
def edit_teacherCourse(request, pk):
    teacherCourse = get_object_or_404(TeacherCourse, pk=pk)

    # Ensure only HOD can edit
    if not request.user.is_staff and not request.user.teacher.is_hod:
        messages.error(request, "You are not authorized to edit course assignments.")
        return redirect('assign_teacher_list')

    # Get HOD's department
    hod_department = request.user.teacher.department_id  

    if request.method == "POST":
        form = TeacherCourseForm(request.POST, instance=teacherCourse)

        if form.is_valid():
            # Ensure only department-specific courses and teachers are assigned
            teacher = form.cleaned_data['teacher_id']
            course = form.cleaned_data['course_id']

            if teacher.department_id != hod_department or course.department_id != hod_department:
                messages.error(request, "You can only assign teachers and courses within your department.")
            else:
                form.save()
                messages.success(request, "Teacher assignment updated successfully.")
                return redirect('assign_teacher_list')
        else:
            messages.error(request, "There was an issue with your submission.")
    else:
        form = TeacherCourseForm(instance=teacherCourse)

        # Filter the teacher and course fields
        form.fields['teacher_id'].queryset = Teacher.objects.filter(department_id=hod_department)
        form.fields['course_id'].queryset = Course.objects.filter(department_id=hod_department)

    return render(request, 'rapid/edit_assign_teacher.html', {'form': form})

#deleting tables
@login_required
@admin_required
def delete_course(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    course.delete()
    return redirect('course_list')

@login_required
@admin_required
def delete_teacher(request, teacher_id):
    # Get the teacher object by its ID
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)

    #if request.method == 'POST':
        # Delete the teacher
    teacher.user_id.delete()  # Delete the related user (optional)
    teacher.delete()  # Delete the teacher

    messages.success(request, "Teacher deleted successfully.")
    return redirect('teacher_list')  # Redirect to the teacher list

    #return render(request, 'delete_teacher.html', {'teacher': teacher})
    
@login_required
@admin_required
def delete_program(request, program_id):
    program = get_object_or_404(Program, pk=program_id)
    program.delete()
    return redirect('program_list')

@login_required
@admin_required
def delete_student(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    return redirect('student_list')

@login_required
@admin_required
def delete_department(request, department_id):
    department = get_object_or_404(Department, pk=department_id)
    department.delete()
    return redirect('department_list')

@login_required
@admin_required
def delete_studentCourse(request, id):
    studentCourse = get_object_or_404(StudentCourse, pk=id)
    studentCourse.delete()
    return redirect('enroll_student_list')

@login_required

def delete_teacherCourse(request, id):
    teacherCourse = get_object_or_404(TeacherCourse, pk=id)
    teacherCourse.delete()
    return redirect('assign_teacher_list')

@login_required
def course_students(request, course_id):
    # Fetch the students enrolled in the selected course
    course = get_object_or_404(Course, course_id=course_id)
    student_course_list = StudentCourse.objects.filter(course_id=course_id)
    return render(request, 'rapid/course_students.html', {'student_course_list': student_course_list,'course': course})

@login_required
def course_students_teacher(request, course_id):
    # Fetch the students enrolled in the selected course
    course = get_object_or_404(Course, course_id=course_id)
    student_course_list = StudentCourse.objects.filter(course_id=course_id)
    return render(request, 'rapid/course_students_teacher.html', {'student_course_list': student_course_list,'course': course})


@login_required
@hod_required
def student_list_hod(request):
    # Get the logged-in teacher's department
    teacher = Teacher.objects.get(user_id=request.user)
    department = teacher.department_id
    
    # Filter students based on the department
    students = Student.objects.filter(program_id__department_id=department).order_by('student_register_number')
    
    return render(request, 'rapid/student_list_hod.html', {'students': students, 'department':department})

@login_required
@hod_required
def add_student(request):
    if request.method == 'POST':
        form = StudentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the student record to the database
            return redirect('student_list_hod')  # Redirect to student list page
    else:
        form = StudentForm()  # Create an empty form instance for GET request
    
    return render(request, 'rapid/add_student.html', {'form': form})

@login_required
@hod_required
def edit_student_hod(request, pk):
    student = get_object_or_404(Student, pk=pk)
    if request.method == "POST":
        form = StudentForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect('student_list_hod')
        else:
            print("Form Errors:", form.errors)  # Debug form validation issues
    else:
        form = StudentForm(instance=student)
    return render(request, 'rapid/edit_student_hod.html', {'form': form})

@login_required
@hod_required
def delete_student_hod(request, student_id):
    student = get_object_or_404(Student, pk=student_id)
    student.delete()
    return redirect('student_list_hod')

@login_required
@hod_required
def teacher_list_hod(request):
    # Get the logged-in teacher's department
    teacher = Teacher.objects.get(user_id=request.user)
    department = teacher.department_id
    
    # Filter students based on the department
    teachers = Teacher.objects.filter(department_id=department)
    
    return render(request, 'rapid/teacher_list_hod.html', {'teachers': teachers, 'department':department})

@login_required
@hod_required
def add_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()  # Save the teacher to the database
            return redirect('teacher_list_hod')  # Redirect to teacher list page
    else:
        form = TeacherForm()
    
    return render(request, 'rapid/add_teacher.html', {'form': form})

@login_required
@hod_required
def edit_teacher_hod(request, pk):
    # Retrieve the teacher object by its ID
    teacher = get_object_or_404(Teacher, pk=pk)

    if request.method == 'POST':
        form = TeacherForm(request.POST, instance=teacher)
        if form.is_valid():
            # Save the teacher instance and the related user information
            form.save()
            messages.success(request, "Teacher information updated successfully!")
            return redirect('teacher_list_hod')  # Redirect to the teacher list or another page
    else:
        form = TeacherForm(instance=teacher)

    return render(request, 'rapid/edit_teacher_hod.html', {'form': form})

@login_required
@hod_required
def delete_teacher_hod(request, teacher_id):
    # Get the teacher object by its ID
    teacher = get_object_or_404(Teacher, teacher_id=teacher_id)

    #if request.method == 'POST':
        # Delete the teacher
    teacher.user_id.delete()  # Delete the related user (optional)
    teacher.delete()  # Delete the teacher

    messages.success(request, "Teacher deleted successfully.")
    return redirect('teacher_list_hod')  # Redirect to the teacher list

@login_required
def course_list_hod(request):
    teacher = Teacher.objects.get(user_id=request.user)  # Fetch teacher based on user
    department = teacher.department_id
    user = request.user

    # Fetch courses based on the teacher role
    if teacher.is_hod:  
        courses = Course.objects.filter(department_id=teacher.department_id)
        hod_courses = TeacherCourse.objects.filter(teacher_id=teacher).values_list('course_id', flat=True)  
    else:
        teacher_courses = TeacherCourse.objects.filter(teacher_id=teacher)
        courses = Course.objects.filter(course_id__in=teacher_courses.values('course'))
        hod_courses = []

    teachers = Teacher.objects.filter(department_id=department)

    # Fetch students for each course (only if the teacher is an HOD)
    course_students = {}
    if teacher.is_hod:
        for course in courses:
            students = StudentCourse.objects.filter(course_id=course).values('student_id__student_name')
            course_students[course] = students

    return render(request, 'rapid/course_list_hod.html', {
        'teachers': teachers,
        'department': department,
        'courses': courses,
        'course_students': course_students if teacher.is_hod else None,
        'hod_courses': hod_courses,  # List of courses assigned to HOD
        'is_hod':teacher.is_hod
        
    })
    
@login_required
def course_list_teacher(request):
    teacher = get_object_or_404(Teacher, user_id=request.user)  # Fetch teacher based on user
    assigned_courses = TeacherCourse.objects.filter(teacher_id=teacher).values_list('course_id', flat=True)
    courses = Course.objects.filter(course_id__in=assigned_courses)

    course_students = {}
    for course in courses:
        students = StudentCourse.objects.filter(course_id=course).select_related('student_id')
        course_students[course.course_id] = students

    return render(request, 'rapid/course_list_teacher.html', {
        'courses': courses,
        'course_students': course_students,
    })

@login_required
@hod_required
def add_course(request):
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new course to the database
            return redirect('course_list_hod')  # Redirect to course list page
    else:
        form = CourseForm()  # Create an empty form instance for GET request
    
    return render(request, 'rapid/add_course.html', {'form': form})



@login_required
def take_attendance(request, course_id):
    teacher = request.user.teacher
    course = get_object_or_404(Course, course_id=course_id)

    student_courses = StudentCourse.objects.filter(course_id=course)
    students = [student_course.student_id for student_course in student_courses]

    # Get sorting option from the request
    sort_by = request.GET.get('sort_by', 'student_register_number')

    # Sort students based on the selected filter
    if sort_by == "student_roll_no":
        students.sort(key=lambda student: student.student_roll_no if student.student_roll_no else "")
    else:
        students.sort(key=lambda student: student.student_register_number)

    if request.method == 'POST':
        attendance_date_str = request.POST.get('date', '')

        if not attendance_date_str:
            messages.warning(request, "Please select a date for taking attendance.")
            return redirect(request.path)

        attendance_date = date.fromisoformat(attendance_date_str)
        selected_hours = request.POST.getlist('hours')

        if not selected_hours:
            messages.warning(request, "Please select at least one hour to record attendance.")
            return redirect(request.path)

        for hour in selected_hours:
            try:
                hour_date_course = HourDateCourse.objects.create(
                    course=course,
                    teacher=teacher,
                    date=attendance_date,
                    hour=int(hour),
                )
                messages.success(request, f"Attendance successfully recorded for Hour {hour}")
            except IntegrityError:
                existing_record = HourDateCourse.objects.get(course=course, date=attendance_date, hour=int(hour))
                teacher_full_name = f"{existing_record.teacher.teacher_name}"
                teacher_phone = existing_record.teacher.phone
                messages.warning(request, f"Attendance already taken by {teacher_full_name} ({teacher_phone}) in Hour {hour} on {attendance_date}")
                continue

            for student in students:
                if f'students_{student.student_id}' in request.POST:
                    AbsentDetails.objects.update_or_create(
                        hour_date_course=hour_date_course,
                        student=student,
                        defaults={'status': False}
                    )

        if teacher.is_hod:
            return redirect('course_list_hod')  # Redirect to HOD dashboard
        else:
            return redirect('course_list_teacher')  # Redirect to Teacher dashboard

    return render(request, 'rapid/take_attendance.html', {
        'course': course,
        'students': students,
        'today': date.today(),
        'hours': range(1, 6),
        'sort_by': sort_by,  # Pass sorting method to template
    })

@login_required
def teacher_attendance_list(request):
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "You are not authorized to access this page.")
        return redirect('index')

    teacher = request.user.teacher
    attendance_records = HourDateCourse.objects.filter(teacher=teacher).order_by('-date')

    # Render different templates based on the teacher's role
    if teacher.is_hod:
        template_name = "rapid/hod_teacher_attendance_list.html"
    else:
        template_name = "rapid/teacher_attendance_list.html"

    context = {
        'attendance_records': attendance_records,
    }
    return render(request, template_name, context)


@login_required
def edit_attendance(request, record_id):
    # Ensure the logged-in user is a teacher
    if not hasattr(request.user, 'teacher'):
        messages.error(request, "You are not authorized to access this page.")
        return redirect('index')

    # Get the attendance record (HourDateCourse) by ID
    attendance_record = get_object_or_404(HourDateCourse, id=record_id)

    # Ensure the logged-in teacher is the one who took the attendance
    if attendance_record.teacher != request.user.teacher:
        messages.error(request, "You are not authorized to edit this attendance.")
        return redirect('teacher_attendance_list')

    # Get all students associated with the course in this attendance record
    student_courses = StudentCourse.objects.filter(course_id=attendance_record.course).select_related('student_id')
    students = [sc.student_id for sc in student_courses]

    # Get existing absences for this attendance record
    existing_absences = AbsentDetails.objects.filter(hour_date_course=attendance_record)
    absent_students = {absence.student.student_id for absence in existing_absences}

    if request.method == 'POST':
        # Get student IDs marked as absent in the form
        selected_absent_ids = {
            int(key.split('_')[1])  # Extract student ID from checkbox name
            for key in request.POST.keys()
            if key.startswith('students_')
        }

        # Ensure students marked absent are recorded in AbsentDetails
        for student in students:
            if student.student_id in selected_absent_ids:
                # If student is not already absent, create an entry
                AbsentDetails.objects.get_or_create(
                    hour_date_course=attendance_record,
                    student=student,
                    defaults={'status': False}  # Absent
                )
            else:
                # If student is removed from absent list, delete the record
                AbsentDetails.objects.filter(hour_date_course=attendance_record, student=student).delete()

        messages.success(request, "Attendance updated successfully.")
        return HttpResponseRedirect(reverse('teacher_attendance_list'))

    context = {
        'attendance_record': attendance_record,
        'students': students,
        'absent_students': absent_students,
    }
    return render(request, 'rapid/edit_attendance.html', context)

@login_required
def remove_attendance(request, record_id):
    record = get_object_or_404(HourDateCourse, id=record_id, teacher=request.user.teacher)
    record.delete()
    messages.success(request, "Attendance record removed successfully!")
    return redirect('teacher_attendance_list')

@login_required
def attendance_report(request, course_id):
    course = Course.objects.get(course_id=course_id)
    total_hours = HourDateCourse.objects.filter(course=course).count()

    # Fetch students from the StudentCourse table, which links students to courses
    student_courses = StudentCourse.objects.filter(course_id=course)
    students = Student.objects.filter(student_id__in=student_courses.values_list('student_id', flat=True))

    # Fetch attendance records for the course
    attendance_records = AbsentDetails.objects.filter(hour_date_course__course=course)

    # Get the current date and time
    date_time = datetime.now()

    attendance_data = []
    for student in students:
        total_present = 0
        total_absent = 0
        
        # Iterate through each HourDateCourse for the course
        for hour_date_course in HourDateCourse.objects.filter(course=course):
            # Check if there is an attendance record for the student for this hour_date_course
            attendance_record = attendance_records.filter(student=student, hour_date_course=hour_date_course).first()
            
            if attendance_record:  # If there is an attendance record
                if attendance_record.status:  # Mark present if status is True
                    total_present += 1
                else:  # Mark absent if status is False
                    total_absent += 1
            else:  # If no attendance record exists, consider the student as present
                total_present += 1
        
        # Calculate attendance percentage
        attendance_percentage = (total_present / total_hours) * 100 if total_hours else 0

        # Add grace hours logic if applicable
        attendance_with_grace = attendance_percentage  # Adjust this if grace hours apply

        attendance_data.append({
            "student": student,
            "total_present": total_present,
            "total_absent": total_absent,
            "attendance_percentage": round(attendance_percentage, 2),
            "attendance_with_grace": round(attendance_with_grace, 2),
        })

    context = {
        "course": course,
        "total_hours": total_hours,
        "attendance_data": attendance_data,
        "date_time": date_time,  # Pass the current date and time to the template
        
    }

    return render(request, 'rapid/report.html', context)

@login_required
@hod_required
def student_individual_report(request, student_id):
    # Fetch the student and their enrolled courses
    student = Student.objects.get(student_id=student_id)
    student_courses = StudentCourse.objects.filter(student_id=student)
    
    # List of courses the student is enrolled in
    courses = [sc.course_id for sc in student_courses]
    
    # Get attendance records for the student
    attendance_data = []
    total_hours = 0
    total_present = 0
    total_absent = 0
    total_course_hours = 0  # Total hours across all courses
    total_attended_hours = 0  # Total hours the student was present across all courses

    # Iterate over each course the student is enrolled in
    for course in courses:
        course_data = {
            'course': course,
            'attendance_per_day': [],
            'total_hours': 0,
            'total_present': 0,
            'total_absent': 0,
            'attendance_percentage': 0,
        }

        # Fetch the class sessions for the course, ordered by date
        sessions = HourDateCourse.objects.filter(course=course).order_by('date')

        for session in sessions:
            # Check if there is an attendance record for this student for this session
            attendance_record = AbsentDetails.objects.filter(student=student, hour_date_course=session).first()
            
            # Calculate attendance status
            if attendance_record:
                status = 'Present' if attendance_record.status else 'Absent'
                if attendance_record.status:
                    course_data['total_present'] += 1
                    total_attended_hours += 1  # Increase the attended hours for the student
                else:
                    course_data['total_absent'] += 1
            else:
                status = 'Present'  # Assume present if no record exists
                course_data['total_present'] += 1
                total_attended_hours += 1  # Assume student is present if no record exists

            course_data['attendance_per_day'].append({
                'date': session.date,
                'status': status,
                'hour': session.hour,
            })
            course_data['total_hours'] += 1
        
        # Calculate attendance percentage for the course
        if course_data['total_hours'] > 0:
            course_data['attendance_percentage'] = (course_data['total_present'] / course_data['total_hours']) * 100
        
        # Add the course data to the attendance data
        attendance_data.append(course_data)

        # Accumulate total course hours and total attended hours for the entire student
        total_course_hours += course_data['total_hours']
        total_present += course_data['total_present']
        total_absent += course_data['total_absent']

    # Calculate overall attendance percentage for the student
    if total_course_hours > 0:
        overall_attendance_percentage = (total_attended_hours / total_course_hours) * 100
    else:
        overall_attendance_percentage = 0

    context = {
        'student': student,
        'attendance_data': attendance_data,
        'total_hours': total_course_hours,
        'total_present': total_present,
        'total_absent': total_absent,
        'overall_attendance_percentage': round(overall_attendance_percentage, 2),
    }

    return render(request, 'rapid/student_report.html', context)

@login_required
@hod_required
def department_report(request, department_id):
    # Fetch the department
    department = Department.objects.get(department_id=department_id)
    
    # Get all students in the department, ordered by their university register number
    students = Student.objects.filter(program_id__department_id=department).order_by('student_register_number')
    
    # Calculate total hours taken for the department (sum of all hours in all courses)
    total_hours_taken = HourDateCourse.objects.filter(course__studentcourse__student_id__program_id__department_id=department).count()

    # Prepare the data for each student
    student_data = []

    # Iterate over each student in the department
    for student in students:
        total_present = 0
        total_hours = 0  # Total hours the student could attend (across all their courses)
        total_absent = 0
        total_attended_hours = 0  # Total hours the student was present across all courses
        
        # Fetch the courses assigned to this student
        courses = student.studentcourse_set.values_list('course_id', flat=True)

        # Loop through the courses the student is enrolled in
        for course_id in courses:
            # Calculate the total number of hours for this course
            course_hours = HourDateCourse.objects.filter(course_id=course_id).count()
            total_hours += course_hours  # Accumulate the total hours for this student
            
            # Fetch all the sessions for this course
            sessions = HourDateCourse.objects.filter(course_id=course_id).order_by('date')
            
            # Loop through each session and calculate present/absent status
            for session in sessions:
                # Check if there is an attendance record for this student for this session
                attendance_record = AbsentDetails.objects.filter(student=student, hour_date_course=session).first()
                
                if attendance_record:
                    if attendance_record.status:
                        total_present += 1
                        total_attended_hours += 1
                    else:
                        total_absent += 1
                else:
                    # If no record exists, assume the student is present
                    total_present += 1
                    total_attended_hours += 1

        # Calculate attendance percentage for this student
        attendance_percentage = (total_attended_hours / total_hours * 100) if total_hours > 0 else 0

        # Append the student's data to the list
        student_data.append({
            'student': student,
            'total_present': total_present,
            'attendance_percentage': round(attendance_percentage, 2),
            'total_hours_taken': total_hours,  # Total hours across all courses
        })
    
    # Prepare context for rendering
    context = {
        'department': department,
        'students': student_data,
        'total_hours_taken': total_hours_taken,
        'is_hod': request.user.groups.filter(name='HOD').exists()  # Check if the user is HOD
    }

    return render(request, 'rapid/department.html', context)

@login_required
@admin_required
def upload_students(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Only CSV files are allowed.")
                return redirect('upload_students')

            try:
                decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
                reader = csv.DictReader(decoded_file)  # Use DictReader for column-based reading
                count = 0

                for row in reader:
                    # Extract only necessary fields
                    student_name = row.get('student_name', '').strip()
                    student_register_number = row.get('student_register_number', '').strip()
                    student_admission_number = row.get('student_admission_number', '').strip()
                    
                    program_name = row.get('program_name', '').strip()
                    department_name = row.get('department_name', '').strip()

                    # Check for missing required values
                    if not student_name or not student_register_number or not student_admission_number:
                        messages.warning(request, f"Skipping entry with missing required fields: {row}")
                        continue

                    # Fetch or create foreign key references
                    department, _ = Department.objects.get_or_create(department_name=department_name)
                    program, _ = Program.objects.get_or_create(program_name=program_name)

                    # Check if student already exists based on admission number
                    if Student.objects.filter(student_admission_number=student_admission_number).exists():
                        messages.warning(request, f"Skipping duplicate student with admission number {student_admission_number}")
                        continue

                    # Create the student object
                    Student.objects.create(
                        student_name=student_name,
                        student_register_number=student_register_number,
                        student_admission_number=student_admission_number,
                        program_id=program,  # Use the primary key
                        department_id=department,  # Use the primary key
                    )
                    count += 1

                messages.success(request, f"Successfully imported {count} students.")
            
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
            
            return redirect('upload_students')
    
    else:
        form = CSVUploadForm()

    return render(request, 'rapid/upload_students.html', {'form': form})

@login_required
@admin_required
def upload_teachers_csv(request):
    if request.method == "POST":
        csv_file = request.FILES.get("csv_file")

        if not csv_file.name.endswith('.csv'):
            messages.error(request, "This is not a CSV file.")
            return redirect("upload_teachers_csv")

        # Read CSV file
        data_set = csv_file.read().decode('utf-8')
        io_string = io.StringIO(data_set)
        csv_reader = csv.reader(io_string, delimiter=',')

        next(csv_reader, None)  # Skip header row if present

        for row in csv_reader:
            if len(row) < 5:
                messages.error(request, f"Skipping row {row}: Missing required fields.")
                continue
            
            teacher_name, email, phone, department_name, is_hod = row[:6]

            # Validate department
            try:
                department = Department.objects.get(department_name=department_name)
            except Department.DoesNotExist:
                messages.error(request, f"Skipping {teacher_name}: Invalid department name '{department_name}'.")
                continue

            # Convert is_hod to Boolean
            is_hod = is_hod.strip().lower() in ['true', '1', 'yes']

            # Create user if not exists
            user, created = User.objects.get_or_create(username=email, email=email)
            if created:
                user.set_password("defaultpassword")  # Set a default password
                user.save()

            # Create or update teacher
            teacher, created = Teacher.objects.get_or_create(
                user_id=user,
                defaults={
                    'teacher_name': teacher_name,
                    'email': email,
                    'phone': phone,
                
                    'department_id': department,
                    'is_hod': is_hod,
                }
            )

            if not created:
                # Update existing teacher details
                teacher.teacher_name = teacher_name
                teacher.email = email
                teacher.phone = phone
                
                teacher.department_id = department
                teacher.is_hod = is_hod
                teacher.save()
                messages.warning(request, f"Updated {teacher_name}.")
            else:
                messages.success(request, f"Added {teacher_name} successfully.")

        return redirect("upload_teachers_csv")

    return render(request, "rapid/upload_teachers.html")

@login_required
@admin_required
def upload_courses(request):
    if request.method == "POST":
        form = CSVUploadForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, "Only CSV files are allowed.")
                return redirect('upload_courses')
            try:
                decoded_file = TextIOWrapper(csv_file.file, encoding='utf-8')
                reader = csv.DictReader(decoded_file)
                count = 0
                for row in reader:
                    course_code = row.get('course_code', '').strip()
                    course_title = row.get('course_title', '').strip()
                    credit = row.get('credit', '').strip()
                    department_name = row.get('department_name', '').strip()
                    semester = row.get('semester', '').strip()
                    
                    if not course_code or not course_title or not department_name or not semester:
                        messages.warning(request, f"Skipping entry with missing required fields: {row}")
                        continue
                    
                    try:
                        credit = float(credit)  # Ensure credit is a valid decimal number
                    except ValueError:
                        messages.warning(request, f"Skipping entry with invalid credit value: {row}")
                        continue
                    
                    department, _ = Department.objects.get_or_create(department_name=department_name)
                    
                    Course.objects.create(
                        course_code=course_code,
                        course_title=course_title,
                        credit=credit,
                        department_id=department,
                        semester=semester,
                    )
                    count += 1
                messages.success(request, f"Successfully imported {count} courses.")
            except Exception as e:
                messages.error(request, f"Error: {str(e)}")
            return redirect('upload_courses')
    else:
        form = CSVUploadForm()
    return render(request, 'rapid/upload_courses.html', {'form': form})

@login_required
@hod_required
def enroll_students_hod(request):
    hod = request.user

    try:
        hod_teacher = Teacher.objects.get(user_id=hod, is_hod=True)
    except Teacher.DoesNotExist:
        messages.error(request, "You are not authorized to enroll students.")
        return redirect("hod_dashboard")

    if request.method == "POST":
        student_id = request.POST.get("student_id")
        selected_courses = request.POST.get("selected_courses", "").split(",")

        if not student_id or not selected_courses:
            messages.error(request, "Please select a student and at least one course.")
            return redirect("enroll_students_hod")

        try:
            student = Student.objects.get(student_id=student_id, department_id=hod_teacher.department_id)

            for course_id in selected_courses:
                if course_id:  # Avoid empty values
                    course = Course.objects.get(course_id=course_id)

                    # Check if the student is already enrolled in this course
                    if not StudentCourse.objects.filter(student_id=student, course_id=course).exists():
                        StudentCourse.objects.create(student_id=student, course_id=course)

            messages.success(request, "Student successfully enrolled in selected courses.")
        except Student.DoesNotExist:
            messages.error(request, "Invalid student selected.")
        except Course.DoesNotExist:
            messages.error(request, "One or more selected courses are invalid.")

        return redirect("enroll_students_hod")

    students = Student.objects.filter(department_id=hod_teacher.department_id)
    courses = Course.objects.all()

    return render(request, "rapid/enroll_students_hod.html", {"students": students, "courses": courses})

@login_required
@hod_required
def enrolled_students_list_hod(request):
    if request.user.teacher.is_hod:  # Ensure only HODs can access
        hod_department_id = request.user.teacher.department_id.department_id  # Get HOD's department ID

        # Filter enrollments to show only students from the HOD's department
        enrolled_students = StudentCourse.objects.select_related('student_id', 'course_id').filter(
            student_id__department_id=hod_department_id  # Use department ID
        )

        return render(request, 'rapid/enrolled_students_hod.html', {'enrolled_students': enrolled_students})
    
    else:
        messages.error(request, "You do not have permission to access this page.")
        return redirect('hod_dashboard')

@login_required
@hod_required
def remove_enrollment_hod(request, enrollment_id):
    try:
        enrollment = StudentCourse.objects.get(id=enrollment_id)

        # Ensure the HOD can only remove students from their own department
        if request.user.teacher.is_hod and enrollment.student_id.department_id == request.user.teacher.department_id:
            enrollment.delete()
            messages.success(request, "Enrollment removed successfully.")
        else:
            messages.error(request, "You do not have permission to remove this enrollment.")

    except StudentCourse.DoesNotExist:
        messages.error(request, "Enrollment record not found.")

    return redirect("enrolled_students_list_hod")









# View for creating a new program level
"""def create_program_level(request):
    if request.method == 'POST':
        form = ProgramLevelForm(request.POST)
        if form.is_valid():
            form.save()  # Save the program level to the database
            return redirect('program_level_list')  # Redirect to program level list page
    else:
        form = ProgramLevelForm()
    
    return render(request, 'rapid/create_program_level.html', {'form': form})"""
    
"""def program_level_list(request):
    program_levels = ProgramLevel.objects.all()  # Fetch all program levels from the database
    return render(request, 'rapid/program_level_list.html', {'program_levels': program_levels})"""