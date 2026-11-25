# RAPID: Real-Time Attendance Progress Information Dashboard

A role-based attendance and course management system built for the Four-Year Undergraduate Programme (FYUGP). RAPID lets students enroll in courses from any department, gives each department head control over teacher and student assignments, and records attendance per course-hour.

## Why RAPID

With the introduction of FYUGP in 2024, traditional semester-based attendance systems became inefficient. Students can now enroll in courses across different departments, which makes student-course mapping, teacher assignment, and attendance tracking hard to manage with older systems.

RAPID is designed to:

- Handle FYUGP's cross-department enrollment, so a student can take courses from any department.
- Give HODs complete control over teacher and student course assignments.
- Track attendance accurately per course-hour, with role-based access.

## Features

- **FYUGP-compatible enrollment:** students can be enrolled in courses from any department.
- **Role-based dashboards:** separate Admin, HOD, and Teacher views.
- **Course and teacher management:** departments, programmes, courses, teachers, and students are managed in one place.
- **Hourly attendance tracking:** attendance is marked per course-hour.
- **Department-specific control:** HODs act only within their own department where it matters (for example, teacher assignment).
- **Real-time attendance monitoring:** attendance records and percentages are visible as soon as they are saved.
- **Reports:** course-wise report, department summary, and individual student report.

## User Roles

| Role | What they can do |
|---|---|
| **Admin** | Manages departments, programmes, teachers, students, and courses. Assigns HODs and controls system-wide settings. |
| **HOD (Head of Department)** | Manages teachers and students in their department. Assigns teachers to courses (only in their department). Enrolls students in courses of any department. Monitors attendance for departmental courses and views the department students summary. |
| **Teacher** | Views assigned courses and enrolled students. Marks attendance for assigned courses per course-hour. Views reports for assigned courses. |

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Database | MySQL |
| Frontend | HTML, CSS |

## Getting Started

> Adjust the file names, database settings, and commands below to match this repository.

```bash
git clone https://github.com/Miqdad7/Rapid.git
cd Rapid

# create and activate a virtual environment
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# install dependencies
pip install -r requirements.txt
```

1. Create a MySQL database and set its name, user, and password in the Django `DATABASES` setting.
2. Apply migrations and create an admin account:

   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   ```

3. Start the server and open `http://127.0.0.1:8000`:

   ```bash
   python manage.py runserver
   ```

4. Sign in as Admin, add departments, programmes, courses, teachers, and students, and assign an HOD to each department. HODs can then assign teachers and enroll students, and teachers can start marking attendance.

## Reports

- **Course-wise report:** attendance for every student enrolled in a course.
- **Department summary:** an overview of attendance for the department's students.
- **Individual report:** a single student's attendance across their courses.

## Future Work

- **Mobile app** for teachers and students to access attendance records on the go.
- **Student notification system** with automatic alerts for low attendance.
- **Offline mode** for marking attendance without internet and syncing once online.
- **Gamification** that encourages students to maintain attendance through rewards or leaderboards.

## Team

- Muhammad Miqdad T P
- Ajin N V

## License

Add a license of your choice (for example MIT) and state it here.
