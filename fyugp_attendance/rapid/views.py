from django.shortcuts import render, redirect
from .forms import CourseForm, StudentForm, ProgramForm, DepartmentForm,ProgramLevelForm, TeacherForm, RoleForm, UserForm
from .models import Course, Student, Program, Department,ProgramLevel, Teacher, Role, User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm


# Landing Page
def landing(request):
    return render(request, 'rapid/landing.html')

# Login Page
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:  # Redirect admin to admin dashboard
                return redirect('admin_dashboard')
            else:  # Redirect regular user to user dashboard
                return redirect('user_dashboard')
        else:
            return render(request, 'rapid/login.html', {'error': 'Invalid username or password'})

    return render(request, 'rapid/login.html')

# Signup Page
def signup_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('course-list')  # Redirect to dashboard or home
    else:
        form = UserCreationForm()
    return render(request, 'rapid/signup.html', {'form': form})


def dashboard_view(request):
    # Check if the user is a superuser (admin)
    if request.user.is_superuser:
        return render(request, 'rapid/admin_dashboard.html')
    else:
        return render(request, 'rapid/user_dashboard.html')

# View for creating a new course
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
def create_department(request):
    if request.method == 'POST':
        form = DepartmentForm(request.POST)
        if form.is_valid():
            form.save()  # Save the department to the database
            return redirect('department_list')  # Redirect to department list page
    else:
        form = DepartmentForm()
    
    return render(request, 'rapid/create_department.html', {'form': form})


# View for creating a new program level
def create_program_level(request):
    if request.method == 'POST':
        form = ProgramLevelForm(request.POST)
        if form.is_valid():
            form.save()  # Save the program level to the database
            return redirect('program_level_list')  # Redirect to program level list page
    else:
        form = ProgramLevelForm()
    
    return render(request, 'rapid/create_program_level.html', {'form': form})

# View for creating a new teacher
def create_teacher(request):
    if request.method == 'POST':
        form = TeacherForm(request.POST)
        if form.is_valid():
            form.save()  # Save the teacher to the database
            return redirect('teacher_list')  # Redirect to teacher list page
    else:
        form = TeacherForm()
    
    return render(request, 'rapid/create_teacher.html', {'form': form})

# View for creating a new role
def create_role(request):
    if request.method == 'POST':
        form = RoleForm(request.POST)
        if form.is_valid():
            form.save()  # Save the role to the database
            return redirect('role_list')  # Redirect to role list page
    else:
        form = RoleForm()
    
    return render(request, 'rapid/create_role.html', {'form': form})

# View for creating a new user
def create_user(request):
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()  # Save the user to the database
            return redirect('user_list')  # Redirect to user list page
    else:
        form = UserForm()
    
    return render(request, 'rapid/create_user.html', {'form': form})

# Optional: List views for each model (e.g., Course, Student, etc.)

# List view for all courses
def course_list(request):
    courses = Course.objects.all()  # Fetch all courses from the database
    return render(request, 'rapid/course_list.html', {'courses': courses})

# List view for all students
def student_list(request):
    students = Student.objects.all()  # Fetch all students from the database
    return render(request, 'rapid/student_list.html', {'students': students})

# List view for all programs
def program_list(request):
    programs = Program.objects.all()  # Fetch all programs from the database
    return render(request, 'rapid/program_list.html', {'programs': programs})

# List view for all departments
def department_list(request):
    departments = Department.objects.all()  # Fetch all departments from the database
    return render(request, 'rapid/department_list.html', {'departments': departments})



# List view for all program levels
def program_level_list(request):
    program_levels = ProgramLevel.objects.all()  # Fetch all program levels from the database
    return render(request, 'rapid/program_level_list.html', {'program_levels': program_levels})

# List view for all teachers
def teacher_list(request):
    teachers = Teacher.objects.all()  # Fetch all teachers from the database
    return render(request, 'rapid/teacher_list.html', {'teachers': teachers})

# List view for all roles
def role_list(request):
    roles = Role.objects.all()  # Fetch all roles from the database
    return render(request, 'rapid/role_list.html', {'roles': roles})

# List view for all users
def user_list(request):
    users = User.objects.all()  # Fetch all users from the database
    return render(request, 'rapid/user_list.html', {'users': users})
