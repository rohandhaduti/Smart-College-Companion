import smtplib
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password,make_password
from .models import userlogin
from django.http import HttpResponse
from django.contrib.auth import authenticate, login as auth_login

from django.urls import reverse

from django.db.models import Count, Q

from student.models import studentdetails

from student.models import assignments

from student.models import subjects

from student.models import submissions

from student.models import notifications

from student.models import userlogin


from student.models import Instructor, StudyMaterial

from student.models import Attendance

from student.models import departments, Exams, StudentExamScores


# Create your views here.

from django.shortcuts import render, redirect
from django.contrib.auth.models import User

# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.conf import settings

from .models import userlogin   # your existing model


def college_admin_register(request):
    ACCESS_CODE = "SMARTCOLLEGE2026"   # change this

    if request.method == "POST":
        college_name = request.POST.get("college_name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        access_code = request.POST.get("access_code")

        # 1. secret code check
        if access_code != ACCESS_CODE:
            messages.error(request, "Invalid registration access code.")
            return redirect("college_admin_register")

        # 2. password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("college_admin_register")

        # 3. unique email
        if userlogin.objects.filter(username=email).exists():
            messages.error(request, "Email already registered.")
            return redirect("college_admin_register")

        # 4. save admin login
        userlogin.objects.create(
            username=email,
            password=make_password(password),
            utype="admin"
        )

        # 5. send email
        try:
            send_mail(
                subject="Smart College Companion Admin Registration",
                message=f"""
Welcome {college_name}

Your admin account has been created successfully.

Login Email: {email}
Password: {password}

Login URL: http://127.0.0.1:8000/login
                """,
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[email],
                fail_silently=True
            )
        except:
            pass

        messages.success(request, "Registration successful. Login details sent to email.")
        return redirect("user_login")

    return render(request, "college_admin_register.html")

def home(request):
    return render(request, 'index2.html')
    
    
from django.contrib import messages

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import messages

from django.contrib.auth.models import User
from .models import userlogin

def setup_admin(request):
    if userlogin.objects.filter(utype='admin').exists():
        return redirect('login')

    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        # ✅ Django user (optional)
        User.objects.create_superuser(
            username=email,
            email=email,
            password=password
        )

        # ✅ Your table (IMPORTANT)
        userlogin.objects.create(
        username=email,
        password=make_password(password),  # ✅ hashed
        utype='admin'
        )
        return redirect('login')

    return render(request, 'setup_admin.html')

def home(request):
    return render(request,'index2.html')

from django.shortcuts import render, redirect
from django.contrib import messages
from .models import userlogin, Instructor


from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import userlogin

from django.contrib.auth.hashers import check_password

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from .models import userlogin, Instructor, studentdetails


def user_login(request):

    # Ensure admin exists
    if not userlogin.objects.filter(utype='admin').exists():
        return redirect('setup_admin')

    if request.method == 'POST':
        username = request.POST.get('t1', '').strip()
        password = request.POST.get('t2', '').strip()

        # 🔍 Check user exists
        try:
            user = userlogin.objects.get(username=username)
        except userlogin.DoesNotExist:
            return render(request, 'login.html', {'msg': 'Invalid username'})

        # 🔐 ADMIN LOGIN
        if user.utype == 'admin':
            try:
                auth_user = User.objects.get(username=username)

                if not check_password(password, auth_user.password):
                    return render(request, 'login.html', {'msg': 'Invalid password'})

                # ✅ SESSION (ADMIN)
                request.session['name'] = auth_user.username
                request.session['user_id'] = "ADMIN001"
                request.session['department'] = "ADMIN"

            except User.DoesNotExist:
                return render(request, 'login.html', {'msg': 'Admin not found'})

        # 🔐 STAFF LOGIN
        elif user.utype == 'staff':
            if not check_password(password, user.password):
                return render(request, 'login.html', {'msg': 'Invalid password'})

            instructor = Instructor.objects.filter(email=username).first()

            request.session['name'] = instructor.name if instructor else username
            request.session['user_id'] = instructor.instructor_id if instructor else ""
            request.session['department'] = instructor.department if instructor else ""

        # 🔐 STUDENT LOGIN
        elif user.utype == 'student':
            if not check_password(password, user.password):
                return render(request, 'login.html', {'msg': 'Invalid password'})

            student = studentdetails.objects.filter(email_id=username).first()

            request.session['name'] = student.name if student else username
            request.session['user_id'] = student.student_id if student else ""
            request.session['department'] = student.department if student else ""

        # ✅ COMMON SESSION
        request.session['username'] = username
        request.session['utype'] = user.utype

        # ✅ REDIRECT
        if user.utype == 'admin':
            return redirect('show_admin')
        elif user.utype == 'staff':
            return redirect('show_staff')
        elif user.utype == 'student':
            return redirect('show_student')

    return render(request, 'login.html')

from django.shortcuts import redirect

def insert_student(request):
    if request.method == 'POST':
        s1=request.POST.get('t1')
        s2=request.POST.get('t2')
        s3=request.POST.get('t3')
        s4=request.POST.get('t4')
        s5=request.POST.get('t5')
        email = request.POST.get('t6').strip()
        mobile = request.POST.get('t7').strip()

        # Prevent duplicates
        if userlogin.objects.filter(username=email).exists():
            return render(request, "instructor.html", {'msg': f"User {email} already exists."})

        # Hash the password
        hashed_password = make_password(mobile)

        #create student
        studentdetails.objects.create(student_id=s1,name=s2,department=s3,sem=s4,year=s5,email_id=email,mobile_no=mobile)
        
        userlogin.objects.create(username=email,password=hashed_password,utype='student')
        User.objects.create_user(username=email,password=mobile)

        # Send email
        try:
            msg = f"Hello {request.POST.get('t7')},\nYour account has been created.\nUsername: {email}\nPassword: {mobile}"
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.starttls()
            mail.login('aqua41231@gmail.com', 'djsq vtfm uhwx hlbd')  
            mail.sendmail('aqua41231@gmail.com', [email], msg)
            mail.quit()
            
        except Exception as e:
            print("Email send failed:", e)

        return render(request,"student_details.html", {'msg': 'Student added successfully!'})

    return render(request,'student_details.html')


def insert_instructor(request):
    if request.method == 'POST':
        email = request.POST.get('t2').strip()
        mobile = request.POST.get('t3').strip()
        
        # Prevent duplicates
        if userlogin.objects.filter(username=email).exists():
            return render(request, "instructor.html", {'msg': f"User {email} already exists."})

        # Hash the password
        hashed_password = make_password(mobile)

        # Create instructor
        Instructor.objects.create(
            instructor_id=request.POST.get('t11'),
            name=request.POST.get('t1'),
            email=email,
            mobileno=mobile,
            qualification=request.POST.get('t4'),
            experience=request.POST.get('t5'),
            joining_date=request.POST.get('t6'),
           # profile_photo=request.POST.get('t7'),
            department=request.POST.get('t8'),
            subject=request.POST.get('t9'),
            sem=request.POST.get('t10')
        )

        # Create login
        userlogin.objects.create(username=email, password=hashed_password, utype='staff')
        User.objects.create_user(username=email, password=mobile)
        # Send email
        try:
            msg = f"Hello {request.POST.get('t2')},\nYour account has been created.\nUsername: {email}\nPassword: {mobile}"
            mail = smtplib.SMTP('smtp.gmail.com', 587)
            mail.starttls()
            mail.login('aqua41231@gmail.com', 'djsq vtfm uhwx hlbd')  # Use App Password
            mail.sendmail('aqua41231@gmail.com', [email], msg)
            mail.quit()
        except Exception as e:
            print("Email send failed:", e)

        return render(request,"instructor.html", {'msg': 'Instructor added successfully!'})

    return render(request,"instructor.html")




def forgotpassword(request):
    if request.method=="POST":
        uname = request.POST.get('t1', '')
        user = userlogin.objects.filter(username=uname).count()
        if user >= 1:
            userlog = userlogin.objects.filter(username=uname).values()
            for u in userlog:
                upass= u['password']
                content = upass
                mail = smtplib.SMTP('smtp.gmail.com', 587)
                mail.ehlo()
                mail.starttls()
                mail.login('aqua41231@gmail.com', 'djsq vtfm uhwx hlbd')
                mail.sendmail('aqua41231@gmail.com', uname , content)
                mail.close()
                return render(request,'login.html', {'msg': 'Your password has been sent to your E-mail'})
        else:
            return render(request,'forgotpass.html', {'msg': 'Enter a valid username'})
    return render(request,'forgotpass.html')


def sendmail(request):
    if request.method == "POST":
        to = request.POST.get('t1')
        message=request.POST.get('t2')

        mail = smtplib.SMTP('smtp.gmail.com', 587)
        mail.ehlo()
        mail.starttls()
        mail.login('aqua41231@gmail.com', 'djsq vtfm uhwx hlbd')
        mail.sendmail('aqua41231@gmail.com',to, message)
        mail.close()
        return render(request, 'mail.html')
    return render(request, 'mail.html')

def changepassword(request):
    uname=request.session.get('username')
    if request.method == 'POST':
        oldpass = request.POST.get('t1', '')
        newpass = request.POST.get('t2', '')
        confirmpass = request.POST.get('t3', '')

        ucheck = userlogin.objects.filter(username=uname).values()
        for a in ucheck:
            u = a['username']
            p = a['password']
            if u == uname and oldpass == p:
                if newpass == confirmpass:
                    userlogin.objects.filter(username=uname).update(password=newpass)
                    base_url=reverse('login')
                    msg='password has been changed successfully'
                    return redirect(base_url,msg=msg)
                else:
                    return render(request, 'changepass.html',{'msg': 'both the username and password are incorrect'})
            else:
                return render(request, 'changepass.html',{'msg': 'invalid username'})
    return render(request, 'changepass.html')



def show_studentdetails(request):
    dept = request.session.get('department')
    utype = request.session.get('utype')
    
    if utype == 'staff' and dept:
        userdict = studentdetails.objects.filter(department=dept)
    else:
        userdict = studentdetails.objects.all()
        
    return render(request,'view_student.html',{'userdict':userdict})

def show_student_admin(request):
    dept_query = request.GET.get('department', '').strip().upper()
    sem_query = request.GET.get('sem', '').strip()

    queryArgs = {}

    # ❌ Ignore SELECT or empty value
    if dept_query and dept_query != "SELECT":
        queryArgs['department__iexact'] = dept_query

    if sem_query and sem_query != "SELECT":
        queryArgs['sem__iexact'] = sem_query

    userdict = studentdetails.objects.filter(**queryArgs)

    return render(request, 'view_student_admin.html', {
        'userdict': userdict,
        'selected_dept': dept_query if dept_query else "SELECT",
        'selected_sem': sem_query if sem_query else "SELECT",
    })

def del_student(request,pk):
    try:
        instance = studentdetails.objects.get(id=pk)
        instance.delete()
    except studentdetails.DoesNotExist:
        pass
        
    userdict = studentdetails.objects.all()
    # Check if this isn't an admin, theoretically. Let's just render the admin one since we added the student link there.
    return render(request, 'view_student_admin.html', {'userdict': userdict})

from datetime import datetime
from django.shortcuts import render
from django.utils import timezone

from datetime import datetime
from django.shortcuts import render
from django.utils import timezone
from .models import assignments, Instructor


def insert_assignment(request):

    # ✅ Get instructor from session
    instructor_id = request.session.get('user_id')
    inst = Instructor.objects.filter(instructor_id=instructor_id).first()

    # ❗ Safety check
    if not inst:
        return render(request, 'assignment.html', {
            'msg': 'Instructor not found!',
        })

    # ✅ Auto increment Assignment ID
    last = assignments.objects.all().order_by('assignment_id').last()
    s1 = int(last.assignment_id) + 1 if last else 1

    if request.method == 'POST':
        try:
            title = request.POST.get('t1')
            description = request.POST.get('t2')
            subject = request.POST.get('t7')

            # ✅ Date handling
            given_date_str = request.POST.get('t5')
            deadline_str = request.POST.get('t4')

            if not given_date_str or not deadline_str:
                raise ValueError("Date fields missing")

            # Convert to datetime
            given_date = datetime.strptime(given_date_str, "%Y-%m-%dT%H:%M")
            given_date = timezone.make_aware(given_date)

            deadline = datetime.strptime(deadline_str, "%Y-%m-%d").date()

            # ✅ Save (semester auto from instructor)
            assignments.objects.create(assignment_id=s1,title=title,description=description,instructor_id=instructor_id,deadline=deadline,given_date=given_date,subject=subject,sem=inst.sem )  # 🔥 AUTO semester)

            return render(request, 'assignment.html', {'msg': 'Assignment created successfully!','instructor_id': instructor_id,'assignment_id': s1 + 1})  # next ID ready'instructor': inst

        except Exception as e:
            return render(request, 'assignment.html', {'msg': f'Error: {str(e)}','instructor_id': instructor_id,'assignment_id': s1,'instructor': inst})

    # ✅ GET request
    return render(request, 'assignment.html', {'instructor_id': instructor_id,'assignment_id': s1,'instructor': inst})

from django.shortcuts import render
from .models import assignments, studentdetails, subjects


from django.shortcuts import render
from .models import assignments, studentdetails, subjects


def show_assignment(request):
    semesters = subjects.objects.values_list('sem', flat=True).distinct().order_by('sem')
    return render(request, 'view_assignment.html', {'semesters': semesters})

from django.http import JsonResponse

def get_semesters(request):
    dept = request.GET.get('dept')

    sems = subjects.objects.filter(department=dept)\
        .values_list('sem', flat=True).distinct().order_by('sem')

    return JsonResponse(list(sems), safe=False)

def get_subjects(request):
    dept = request.GET.get('dept')
    sem = request.GET.get('sem')

    subs = subjects.objects.filter(
        department=dept,
        sem=sem
    ).values_list('course_name', flat=True)

    return JsonResponse(list(subs), safe=False)

def get_assignments(request):
    sem = request.GET.get('sem')
    subject = request.GET.get('subject')
    dept = request.GET.get('dept')

    data = assignments.objects.all()

    if dept:
        dept_subjects = subjects.objects.filter(
            department=dept
        ).values_list('course_name', flat=True)
        data = data.filter(subject__in=dept_subjects)

    if sem:
        sem_subjects = subjects.objects.filter(
            sem=sem,
            department=dept
        ).values_list('course_name', flat=True)
        data = data.filter(subject__in=sem_subjects)

    if subject:
        data = data.filter(subject=subject)

    result = list(data.values(
        'assignment_id', 'subject', 'title',
        'description', 'instructor_id',
        'given_date', 'deadline'
    ))

    return JsonResponse(result, safe=False)
    
def del_assignment(request,pk):
    id = assignments.objects.get(id=pk)
    id.delete()
    userdict = assignments.objects.all()
    return render(request, 'view_assignment.html', {'userdict': userdict})

def insert_subjects(request):
    if request.method=='POST':
        s1=request.POST.get('t1')
        s2=request.POST.get('t2')
        s3=request.POST.get('t3')
        #s4=request.POST.get('t4')
        s5=request.POST.get('t5')
        subjects.objects.create(course_name=s1,instructor_id=s2,department=s3,sem=s5,enrolled_at='2026')
        return render(request,'subjects.html')
    return render(request,'subjects.html')

def show_subjects(request):
    user_id = request.session.get('user_id')
    student = studentdetails.objects.filter(student_id=user_id).first()
    if student:
        userdict = subjects.objects.filter(department=student.department, sem=str(student.sem))
        for sub in userdict:
            inst = Instructor.objects.filter(
                instructor_id=sub.instructor_id
            ).first()

            sub.instructor_name = inst.name if inst else "Not Assigned"
    else:
        userdict = subjects.objects.none()
    return render(request,'view_subjects.html',{'userdict': userdict})

def del_subjects(request,pk):
    id = subjects.objects.get(id=pk)
    id.delete()
    userdict = subjects.objects.all()
    return render(request, 'view_subjects.html', {'userdict': userdict})

def insert_submissions(request):
    if request.method == 'POST':
        s1=request.POST.get('t1')
        s2 = request.session.get('user_id')
        file = request.FILES.get('myfile')   # IMPORTANT
        s4=request.POST.get('t4')
        s5=request.POST.get('t5', 'Submitted')
        if not s5:
            s5 = 'Submitted'
        
        submissions.objects.create(Assignments_id=s1,Student_id=s2,file_url=file,submitted_date=s4,status=s5)
        return render(request,"submission.html", {'msg': 'Assignment submitted successfully!'})
    return render(request,"submission.html")

def show_submissions(request):
    assign_id = request.GET.get('assignment_id', '').strip()
    instructor_id = request.session.get('user_id')
    utype = request.session.get('utype')

    # Get the assignments created by this instructor
    if utype == 'staff' and instructor_id:
        my_assignments = assignments.objects.filter(instructor_id=instructor_id)
        assign_ids = list(my_assignments.values_list('assignment_id', flat=True))
    else:
        my_assignments = assignments.objects.all()
        assign_ids = None

    if assign_id:
        # If manually searching by Assignment ID
        data = submissions.objects.filter(Assignments_id=assign_id)
    else:
        # Show all submissions for assignments belonging to the logged in staff
        if assign_ids is not None:
            data = submissions.objects.filter(Assignments_id__in=assign_ids)
        else:
            data = submissions.objects.all()

    return render(request, "view_submission.html", {
        "data": data,
        "my_assignments": my_assignments,
        "selected_assignment": assign_id
    })

def del_submissions(request,pk):
    id = submissions.objects.get(id=pk)
    id.delete()
    userdict = submissions.objects.all()
    return render(request, "view_submission.html", {'userdict': userdict})

from student.models import timetable

from student.models import announcements

from student.models import feedback


# Create your views here.


def insert_timetable(request):
    context = {}
    if request.method == 'POST':
        s1 = request.POST.get('t1') # Dept
        s2 = request.POST.get('t2') # Sem
        s3 = request.POST.get('t3') # Subject
        s4 = request.POST.get('t4') # Day
        s5 = request.POST.get('t5') # Time
        s6 = request.POST.get('t6') # Instructor ID

        # Clash Prevention Logic
        # 1. Instructor double-booking clash
        instructor_clash = timetable.objects.filter(instructor_id=s6, day=s4, time=s5).exists()
        
        # 2. Department & Semester overlap clash
        dept_clash = timetable.objects.filter(dept=s1, sem=s2, day=s4, time=s5).exists()

        if instructor_clash:
            context['error_msg'] = f"CRITICAL CLASH: Instructor ID {s6} is already scheduled on {s4} at {s5}!"
        elif dept_clash:
            context['error_msg'] = f"SCHEDULE CLASH: {s1} Semester {s2} already has a class scheduled on {s4} at {s5}."
        else:
            timetable.objects.create(dept=s1, sem=s2, subject=s3, day=s4, time=s5, instructor_id=s6)
            context['success_msg'] = "Timetable slot successfully scheduled without any clashes!"

        return render(request, 'timetable.html', context)
    return render(request, 'timetable.html', context)


def insert_announcements(request):
    if request.method == 'POST':
        s1=request.POST['t1']
        s2=request.POST['t2']
        s3=request.POST['t3']
        announcements.objects.create(announcement_id=s1,massage=s2,date=s3)
        return render(request, 'announcements.html')
    return render(request, 'announcements.html')


def insert_feedback(request):
    if request.method == 'POST':
        s1=request.POST.get('t1')
        s2=request.POST.get('t2')
        s3=request.POST.get('t3')
        s4=request.POST.get('t4')
        feedback.objects.create(instructor_id=s1,comments=s2,grade=s3,given_date=s4)
        return render(request, 'feedback.html')
    return render(request, 'feedback.html')

def get_timetable_data(s1, s2):
    table = {}
    timetable_data = timetable.objects.filter(dept=s1, sem=s2)
    for t in timetable_data:
        if t.day not in table:
            table[t.day] = {'t1': '', 't2': '', 't3': '', 't4': ''}
        time = t.time.strftime("%H:%M") if hasattr(t.time, 'strftime') else str(t.time).strip()
        if time in ['08:30', '8:30']: table[t.day]['t1'] = t.subject
        elif time in ['09:30', '9:30']: table[t.day]['t2'] = t.subject
        elif time == '10:30': table[t.day]['t3'] = t.subject
        elif time == '11:30': table[t.day]['t4'] = t.subject
    return table

def show_timetable(request):
    utype = request.session.get('utype')
    user_id = request.session.get('user_id')
    dept = request.session.get('department', '')
    sem = ''
    if utype == 'staff':
        inst = Instructor.objects.filter(instructor_id=user_id).first()
        if inst:
            dept = inst.department
            sem = str(inst.sem)

    s1 = request.POST.get('t1') if request.method == 'POST' else dept
    s2 = request.POST.get('t2') if request.method == 'POST' else sem
    table = get_timetable_data(s1, s2) if s1 and s2 else {}
    return render(request, 'view_timetable.html', {'table': table, 'selected_dept': s1, 'selected_sem': s2})

def show_timetable_student(request):
    user_id = request.session.get('user_id')
    dept = request.session.get('department', '')
    sem = ''
    stu = studentdetails.objects.filter(student_id=user_id).first()
    if stu:
        dept = stu.department
        sem = str(stu.sem)

    s1 = request.POST.get('t1') if request.method == 'POST' else dept
    s2 = request.POST.get('t2') if request.method == 'POST' else sem
    table = get_timetable_data(s1, s2) if s1 and s2 else {}
    return render(request, 'view_student_timetable.html', {'table': table, 'selected_dept': s1, 'selected_sem': s2})

def show_announcements(request):
    userdict = announcements.objects.all()
    utype = request.session.get('utype')
    if utype == 'staff' or utype == 'admin':
        return render(request, 'view_staff_announcements.html', {'userdict': userdict})
    else:
        return render(request, 'view_student_announcements.html', {'userdict': userdict})

def show_feedback(request):
    userdict=feedback.objects.all()
    return render(request,'view_feedback.html',{'userdict':userdict})

def del_timetable(request,pk):
    id = timetable.objects.get(id=pk)
    id.delete()
    userdict = timetable.objects.all()
    return render(request, 'view_timetable.html', {'userdict': userdict})

def del_attendance(request,pk):
    id = Attendance.objects.get(id=pk)
    id.delete()
    userdict = Attendance.objects.all()
    return render(request, 'view_attendence.html', {'userdict': userdict})

def del_announcements(request,pk):
    id = announcements.objects.get(id=pk)
    id.delete()
    userdict = announcements.objects.all()
    return render(request, 'view_announcements.html', {'userdict': userdict})

def del_feedback(request,pk):
    id = feedback.objects.get(id=pk)
    id.delete()
    userdict = feedback.objects.all()
    return render(request, 'view_feedback.html', {'userdict': userdict})

def insert_notifications(request):
    instructor_id = request.session.get('user_id')
    if request.method == 'POST':
        s1=request.POST['t1']
        s2=request.POST['t2']
        s3=request.POST['t3']
        notifications.objects.create(given_by=s1,message=s2,type=s3)
        return render(request,"notifications.html",{'instructor_id':instructor_id})
    return render(request,"notifications.html",{'instructor_id':instructor_id})

def view_notifications(request):
    user_id = request.session.get('user_id')
    utype = request.session.get('utype')
    if utype == 'student' and user_id:
        student = studentdetails.objects.filter(student_id=user_id).first()
        if student:
            instructors_same_dept = Instructor.objects.filter(department=student.department)
            inst_ids_dept = [str(i.instructor_id) for i in instructors_same_dept]
            inst_names_dept = [i.name for i in instructors_same_dept]
            userdict = notifications.objects.filter(Q(given_by__in=inst_names_dept) | Q(given_by__in=inst_ids_dept))
        else:
            userdict = notifications.objects.none()
    else:
        userdict = notifications.objects.all()
    return render(request,"view_notifications.html",{'userdict':userdict})

def del_notifications(request,pk):
    id = notifications.objects.get(id=pk)
    id.delete()
    userdict = notifications.objects.all()
    return render(request, "view_notifications.html", {'userdict': userdict})

def insert_exams(request):
    if request.method=='POST':
        s1=request.POST.get('t1')
        s2=request.POST.get('t2')
        s3=request.POST.get('t3')
        s4=request.POST.get('t4')
        s5=request.POST.get('t5')
        Exams.objects.create(exam_id=s1,course_id=s2,exam_name=s3,date=s4,max_score=s5)
        return render(request,'exams.html')
    return render(request,'exams.html')

def view_exams(request):
    userdict=Exams.objects.all()
    return render(request,'view_exam.html',{'userdict':userdict})

def del_exams(request,pk):
    id = Exams.objects.get(id=pk)
    id.delete()
    userdict = Exams.objects.all()
    return render(request, "view_exam.html", {'userdict': userdict})

def insert_examScores(request):
    if request.method=='POST':
        s1=request.POST.get('t1')
        s2=request.POST.get('t2')
        s3=request.POST.get('t3')
        s4=request.POST.get('t4')
        StudentExamScores.objects.create(student_id=s1,exam_id=s2,score=s3,performance_level=s4)
        return render(request,"examscores.html")
    return render(request,"examscores.html")

def view_examscores(request):
    userdict=StudentExamScores.objects.all()
    return render(request,'view_examScores.html',{'userdict':userdict})

def del_examscores(request,pk):
    id = StudentExamScores.objects.get(id=pk)
    id.delete()
    userdict = StudentExamScores.objects.all()
    userdict = StudentExamScores.objects.all()
    return render(request, 'view_examScores.html', {'userdict': userdict})


def show_instructor(request):
    user_id = request.session.get('user_id')
    utype = request.session.get('utype')
    if utype == 'student' and user_id:
        student = studentdetails.objects.filter(student_id=user_id).first()
        if student:
            userdict = Instructor.objects.filter(department=student.department)
        else:
            userdict = Instructor.objects.none()
    else:
        userdict = Instructor.objects.all()
    return render(request,'view_instructor.html',{'userdict':userdict})

def del_instructor(request,pk):
    try:
        inst = Instructor.objects.get(instructor_id=pk)
        inst.delete()
    except Instructor.DoesNotExist:
        pass
    userdict = Instructor.objects.all()
    # If the user is admin, they might want view_instructor_admin.html
    # but to be safe, we'll try to find out where they came from or return admin view
    return render(request, 'view_instructor_admin.html', {'userdict': userdict})


def insert_StudyMaterial(request):
    # Get logged-in instructor id from session
    user_id = request.session.get('user_id')

    # Fetch instructor details
    instructor = Instructor.objects.filter(instructor_id=user_id).first()

    # Get last material id
    last = StudyMaterial.objects.all().order_by('material_id').last()

    if last:
        # Remove MAT and take only number
        last_num = int(str(last.material_id).replace('MAT', ''))
        new_id = "MAT" + str(last_num + 1)
    else:
        new_id = "MAT101"

    if request.method == 'POST':

        s1 = request.POST.get('t1')
        s2 = request.POST.get('t2')
        s3 = request.POST.get('t3')

        s4 = instructor.subject if instructor else ""
        s5 = instructor.sem if instructor else ""
        s6 = instructor.name if instructor else ""

        file = request.FILES.get('myfile')
        s8 = request.POST.get('t8')

        StudyMaterial.objects.create(material_id=s1,title=s2,description=s3,subject=s4,semester=s5,instructor_name=s6,file=file,upload_date=s8)

        return redirect('insert_StudyMaterial')

    return render(request, "study_materials.html", {
        'instructor': instructor,
        'material_id': new_id
    })

def show_StudyMaterial(request):
    user_id = request.session.get('user_id')
    utype = request.session.get('utype')
    if utype == 'student' and user_id:
        student = studentdetails.objects.filter(student_id=user_id).first()
        if student:
            instructors_same_sem = Instructor.objects.filter(department=student.department, sem=student.sem)
            userdict = StudyMaterial.objects.filter(semester=student.sem, subject__in=instructors_same_sem.values_list('subject', flat=True))
        else:
            userdict = StudyMaterial.objects.none()
    else:
        userdict=StudyMaterial.objects.all()
    return render(request,"view_studymaterials.html",{'userdict':userdict})

def del_StudyMaterial(request,pk):
    id = StudyMaterial.objects.get(id=pk)
    id.delete()
    userdict = StudentExamScores.objects.all()
    return render(request, "view_studymaterials.html", {'userdict': userdict})

from django.shortcuts import render, redirect
from .models import Attendance, Instructor, subjects, studentdetails


def fill_attendance(request):
    instructor_id = request.session.get('user_id')
    instructor_name = request.session.get('name')

    instructor = Instructor.objects.filter(
        instructor_id=instructor_id
    ).first()

    dept = instructor.department if instructor else ""

    # subject + semester for dropdown
    instructor_subjects = subjects.objects.filter(
        instructor_id=instructor_id
    ).values('course_name', 'sem').distinct()

    if request.method == 'POST':
        sem = request.POST.get('semester')
        subject = request.POST.get('subject')

        students = studentdetails.objects.filter(
            department=dept,
            sem=sem
        )

        return render(request, 'take_attendance.html', {
            'userdict': students,
            'semester': sem,
            'subject': subject,
            'instructor': instructor
        })

    return render(request, 'attendance.html', {
        'instructor': instructor,
        'name': instructor_name,
        'instructor_id': instructor_id,
        'instructor_subjects': instructor_subjects
    })


def insert_attendance(request):
    if request.method == "POST":

        sem = request.POST.get('sem')
        subject = request.POST.get('subject')

        student_ids = request.POST.getlist('student_id')

        for sid in student_ids:

            status = request.POST.get(f'status_{sid}')

            try:
                Attendance.objects.create(
                    student_id=sid,
                    subject=subject,
                    status=status,
                    sem=sem
                )
                print("Saved:", sid)

            except Exception as e:
                print("ERROR:", e)

        return redirect('fill_attendance')

    return redirect('fill_attendance')     

from django.db.models import Count, Q
from django.shortcuts import render
from .models import Attendance
from django.db.models import Count, Q, F, FloatField, ExpressionWrapper, Case, When


def show_attedance(request):
    instructor_id = request.session.get('user_id')

    instructor = Instructor.objects.filter(
        instructor_id=instructor_id
    ).first()

    data = []

    # All semester + subjects of logged-in instructor
    instructor_subjects = subjects.objects.filter(
        instructor_id=instructor_id
    ).values('sem', 'course_name').distinct()

    semesters = subjects.objects.filter(
        instructor_id=instructor_id
    ).values_list('sem', flat=True).distinct()

    selected_sem = ""
    selected_subject = ""

    if request.method == 'POST':
        selected_sem = request.POST.get('sem')
        selected_subject = request.POST.get('subject')

        records = Attendance.objects.filter(
            sem=selected_sem,
            subject=selected_subject
        ).values('student_id').annotate(
            total_classes=Count('id'),
            attended_classes=Count(
                'id',
                filter=Q(status="Present")
            ),
            percentage=ExpressionWrapper(
                (F('attended_classes') * 100.0) / F('total_classes'),
                output_field=FloatField()
            )
        )

        for r in records:
            stu = studentdetails.objects.filter(
                student_id=r['student_id']
            ).first()

            data.append({
                'student_id': r['student_id'],
                'student_name': stu.name if stu else "Not Found",
                'total_classes': r['total_classes'],
                'attended_classes': r['attended_classes'],
                'percentage': round(r['percentage'], 2)
            })

    return render(request, "view_attendance.html", {
        "data": data,
        "instructor": instructor,
        "semesters": semesters,
        "instructor_subjects": instructor_subjects,
        "selected_sem": selected_sem,
        "selected_subject": selected_subject
    })



from django.db.models import Count, Q, FloatField, ExpressionWrapper

def show_student_attendance(request):

    user_id = request.session.get('user_id')
    utype = request.session.get('utype')

    userdict = None

    # 🎓 Only for logged-in student
    if utype == 'student' and user_id:

        userdict = Attendance.objects.filter(student_id=user_id)\
            .values('subject')\
            .annotate(
                total_classes=Count('id'),
                attended_classes=Count('id', filter=Q(status="Present")),
                percentage=ExpressionWrapper(
                    (Count('id', filter=Q(status="Present")) * 100.0) / Count('id'),
                    output_field=FloatField()
                )
            )

    return render(request, 'student_view_attendance.html', {"userdict": userdict})

def insert_department(request):
    if request.method == 'POST':
        s1=request.POST.get('t1')
        s2=request.POST.get('t2')
        s3=request.POST.get('t3')
        departments.objects.create(department_id=s1,dept_name=s2,hod=s3)
        return render(request,"department.html")
    return render(request,"department.html")

def show_department(request):
    userdict=departments.objects.all()
    return render(request,"view_department.html",{'userdict':userdict})

def show_department_admin(request):
    userdict=departments.objects.all()
    return render(request,"view_department_admin.html",{'userdict':userdict})

def show_feedback_admin(request):
    userdict = feedback.objects.all().order_by('-id')
    return render(request,"view_feedback_admin.html",{'userdict':userdict})

def del_department(request,pk):
    try:
        dept = departments.objects.get(id=pk)
        dept.delete()
    except departments.DoesNotExist:
        pass
    userdict = departments.objects.all()
    return render(request, "view_department_admin.html", {'userdict': userdict})

def show_instructor_admin(request):
    userdict = Instructor.objects.all()
    return render(request,'view_instructor_admin.html',{'userdict':userdict})


def show_admin(request):    
    context = {
        'recent_announcements': announcements.objects.count(),
        'student_count': studentdetails.objects.count(),
        'total_subjects': subjects.objects.count(),
        'total_feedbacks': feedback.objects.count(),
        'total_departments':departments.objects.count(),
        'total_staff':Instructor.objects.count(),
        'admin_notices': notifications.objects.all().order_by('-id')[:5],
        'feedbacks': feedback.objects.all().order_by('-id')[:5],
        'announcements_list': announcements.objects.all()
    }
    return render(request,'admin_home.html',context)

from django.shortcuts import render, redirect
from django.db.models import Q

def show_student(request):
    user_id = request.session.get('user_id')

    if not user_id:
        return redirect('login')

    student = studentdetails.objects.filter(student_id=user_id).first()

    if not student:
        return redirect('login')

    dept = student.department
    sem = student.sem

    # Instructors (same dept + sem)
    instructors_same_sem = Instructor.objects.filter(department=dept, sem=sem)
    inst_ids_sem = [str(i.instructor_id) for i in instructors_same_sem]

    # Instructors (same dept)
    instructors_same_dept = Instructor.objects.filter(department=dept)
    inst_ids_dept = [str(i.instructor_id) for i in instructors_same_dept]
    inst_names_dept = [i.name for i in instructors_same_dept]

    subject_count = subjects.objects.filter(department=dept, enrolled_at=str(sem)).count()

    study_materials_count = StudyMaterial.objects.filter(
        semester=sem,
        subject__in=instructors_same_sem.values_list('subject', flat=True)
    ).count()

    assignment_count = assignments.objects.filter(instructor_id__in=inst_ids_sem).count()
    my_assignments = assignments.objects.filter(instructor_id__in=inst_ids_sem)

    notices = notifications.objects.filter(
        Q(given_by__in=inst_names_dept) | Q(given_by__in=inst_ids_dept)
    )

    context = {
        'student': student,
        'subject_count': subject_count,
        'study_materials_count': study_materials_count,
        'assignment_count': assignment_count,
        'assignments': my_assignments,
        'notices': notices,
        'notif_count': notices.count(),

        # ✅ Announcements (LATEST FIRST)
        'announcements_list': announcements.objects.all().order_by('-id'),
    }

    return render(request, 'student_home.html', context)
    
from django.db.models import Q

def show_staff(request):
    ins_id = request.session.get('user_id')
    instructor = None

    student_count = 0
    my_subjects = subjects.objects.filter(instructor_id=ins_id)
    no_of_subjects = subjects.objects.filter(instructor_id=ins_id).count()
    print("Instructor ID:", ins_id)

    for sub in my_subjects:
        student_count += studentdetails.objects.filter(department=sub.department,sem=sub.sem).count()

    if ins_id:
        instructor = Instructor.objects.filter(instructor_id=ins_id).first()
        
    
    # ✅ Notifications added by this instructor
    recent_notifications = notifications.objects.filter(given_by=ins_id).order_by('-id')[:5]   # OR given_by=instructor (if FK)

    # ✅ Assignments created by this instructor
    recent_assignments = assignments.objects.filter(instructor_id=ins_id).order_by('-id')[:5]
    no_of_assignments = assignments.objects.filter(instructor_id=ins_id).order_by('-id')[:5].count()

    assign_id = assignments.objects.values_list('assignment_id', flat=True).first()
    no_of_submissions = submissions.objects.filter(Assignments_id=assign_id).count()

    # ✅ Feedback related to this instructor
    my_feedbacks = feedback.objects.filter(instructor_id=ins_id).order_by('-id')[:5]

    context = {
        'instructor': instructor,
        'no_of_subjects':no_of_subjects,
        'recent_notifications': recent_notifications,
        'recent_assignments': recent_assignments,
        'my_feedbacks': my_feedbacks,
        'student_count': student_count,
        'no_of_assignments': no_of_assignments,
        'total_submissions': no_of_submissions,
        'total_subjects': subjects.objects.count(),
        'total_feedbacks': feedback.objects.count(),
        'announcements_list':announcements.objects.all( )
    }

    return render(request, 'staff_home.html', context)