# Student Management Portal

## Project Overview

The **Student Management Portal** is a web-based application developed using Python and Django to simplify and manage academic activities within an educational institution. It provides separate dashboards for administrators, teachers, and students, allowing them to manage and access academic information efficiently.

The system helps reduce manual work by providing a centralized platform for managing student records, teacher details, attendance, marks, subjects, timetables, and assignments.

## Features

### Admin Module
- Manage student information (Add, View, Update, Delete).
- Add and manage teacher details.
- Manage subjects and timetables.
- Upload and manage student results.
- Monitor student attendance.
- Access the admin dashboard.

### Teacher Module
- Access the teacher dashboard.
- View student information.
- Mark and manage student attendance.
- Upload student marks.
- Manage assignments.

### Student Module
- Access the student dashboard.
- View personal and academic details.
- Check attendance records.
- View marks and examination results.
- View, download, and upload assignments.

### Additional Features
- Separate login interfaces for Admin, Teachers, and Students.
- Dashboard-based navigation.
- Database-driven record management.
- Assignment and media file handling.
- Chat module.

## Technologies Used

| Category | Technologies |
|---|---|
| Backend | Python, Django |
| Frontend | HTML, CSS, JavaScript, Bootstrap |
| Database | SQLite |
| Tools | VS Code, Git, GitHub |

## Project Structure

```text
Student_Management_Portal/
│
├── Adminapp/
│   └── Admin dashboard and management
│
├── Student_Management/
│   └── Main project configuration
│
├── chat/
│   └── Chat functionality
│
├── mainapp/
│   └── Main application and home page
│
├── media/
│   └── Uploaded media files
│
├── studentapp/
│   └── Student functionalities
│
├── teacherapp/
│   └── Teacher functionalities
│
├── db.sqlite3
├── manage.py
└── README.md
```

## Installation and Setup

Follow these steps to run the project locally.

### 1. Clone the Repository

```bash
git clone https://github.com/ardra-asokan/Student_Management.git
```

### 2. Navigate to the Project Directory

```bash
cd Student_Management
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

**Windows:**

```bash
venv\Scripts\activate
```

### 5. Install Django

```bash
pip install django
```

If your project has a `requirements.txt` file, install all dependencies using:

```bash
pip install -r requirements.txt
```

### 6. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 7. Run the Development Server

```bash
python manage.py runserver
```

### 8. Open the Application

Open your browser and visit:

```text
http://127.0.0.1:8000/
```

## Future Enhancements

- Email and SMS notifications.
- Dashboard analytics and graphical reports.
- PDF generation for academic reports.
- Improved real-time communication.
- Enhanced user interface and security.

## Author

**Ardra Asokan**

B.Tech – Computer Science and Engineering

GitHub: [ardra-asokan](https://github.com/ardra-asokan)

---

*Developed as a web development project using Python and Django.*
