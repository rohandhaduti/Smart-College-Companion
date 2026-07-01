# SMART COLLEGE COMPANION

from django.db import models


# Create your models here.

class userlogin(models.Model):
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=255)  # store hashed passwords
    utype = models.CharField(max_length=20, choices=[('admin','Admin'),('staff','Staff'),('student','Student')])

    def __str__(self):
        return self.username

class newuser(models.Model):
    username = models.CharField(max_length=20)
    mobileno = models.CharField(max_length=15, unique=True,null=True)

class studentdetails(models.Model):
    student_id = models.CharField(max_length=40)
    name = models.CharField(max_length=40)
    email_id = models.CharField(max_length=20)
    department = models.CharField(max_length=40)
    sem = models.IntegerField()
    year = models.IntegerField()
    mobile_no = models.CharField(max_length=10)


class assignments(models.Model):
    title = models.CharField(max_length=50)
    description = models.CharField(max_length=100)
    instructor_id = models.CharField(max_length=10)
    deadline = models.DateField(null=True, blank=True)
    given_date = models.DateTimeField(null=True, blank=True)
    assignment_id = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    sem = models.IntegerField(default=1)

class submissions(models.Model):
    Assignments_id = models.CharField(max_length=50)
    Student_id = models.CharField(max_length=10)
    file_url = models.FileField(upload_to='submissions/')
    submitted_date = models.DateField()
    status = models.CharField(max_length=10)

class Attendance(models.Model):
    student_id = models.CharField(max_length=20)
    subject = models.CharField(max_length=50)
    status = models.CharField(max_length=10)
    sem = models.IntegerField()

class feedback(models.Model):
    instructor_id = models.CharField(max_length=10)
    comments = models.CharField(max_length=50)
    grade = models.CharField(max_length=10)
    given_date = models.DateField()

class subjects(models.Model):
    course_name = models.CharField(max_length=50)
    instructor_id = models.CharField(max_length=10)
    department = models.CharField(max_length=50)
   # student_id = models.CharField(max_length=10)
    enrolled_at = models.CharField(max_length=50)
    sem=models.IntegerField()

class timetable(models.Model):
    dept = models.CharField(max_length=50)
    sem = models.CharField(max_length=50)
    subject = models.CharField(max_length=50)
    day = models.CharField(max_length=10)
    time = models.CharField(max_length=50)
    instructor_id = models.CharField(max_length=10)
    

class Exams(models.Model):
    exam_id = models.CharField(max_length=40)
    course_id = models.CharField(max_length=30)
    exam_name = models.CharField(max_length=100)
    date = models.DateField()
    max_score = models.IntegerField()


class StudentExamScores(models.Model):
    student_id = models.CharField(max_length=40)
    exam_id = models.CharField(max_length=30)
    score = models.IntegerField()
    performance_level = models.CharField(max_length=40)


class notifications(models.Model):
    given_by = models.CharField(max_length=10)
    message = models.CharField(max_length=50)
    type = models.CharField(max_length=100)
    target = models.CharField(max_length=20, default='all')

class departments(models.Model):
    department_id=models.CharField(max_length=50)
    dept_name=models.CharField(max_length=100)
    hod=models.CharField(max_length=100)

class Instructor(models.Model):
    instructor_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=20)
    mobileno = models.CharField(max_length=15, unique=True,)    
    qualification = models.CharField(max_length=100)
    experience = models.IntegerField()
    joining_date = models.DateField()
   # profile_photo = models.ImageField(upload_to='instructors/', blank=True, null=True)
    department = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    sem = models.IntegerField()

class StudyMaterial(models.Model):
    material_id = models.CharField(max_length=20, primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200)
    subject = models.CharField(max_length=50)
    semester = models.CharField(max_length=10)
    instructor_name = models.CharField(max_length=100)
    file = models.FileField(upload_to='materials/')
    upload_date = models.DateField()

class announcements(models.Model):
    announcement_id = models.CharField(max_length=50)
    event_id = models.CharField(max_length=10)
    massage = models.CharField(max_length=50)
    date = models.DateField()
