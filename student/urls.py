"""
URL configuration for staff project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include

from student import views

urlpatterns = [
    # urls.py
    path('college_admin_register/', views.college_admin_register, name='college_admin_register'),       
    path('home',views.home,name='home'),
    path('staff/', include('staff.urls')),     # ✅ now valid
    path('sendmail',views.sendmail,name='sendmail'),
    path('changepassword',views.changepassword,name='changepassword'),
    path('forgotpassword',views.forgotpassword,name='forgotpassword'),

    #insert
    path('insert_student',views.insert_student,name='insert_student'),
    path('insert_assignment',views.insert_assignment,name='insert_assignment'),
    path('insert_subjects',views.insert_subjects,name='insert_subjects'),
    path('insert_submissions', views.insert_submissions, name='insert_submissions'),
    path('insert_timetable',views.insert_timetable,name='insert_timetable'),
    path('insert_announcements',views.insert_announcements,name='insert_announcements'),
    path('insert_feedback',views.insert_feedback,name='insert_feedback'),
    path('insert_notifications',views.insert_notifications,name='insert_notifications'),
    path('insert_exams',views.insert_exams,name='insert_exams'),
    path('insert_examScores',views.insert_examScores,name='insert_examScores'),
    path('insert_instructor',views.insert_instructor,name='insert_instructor'),
    path('insert_StudyMaterial',views.insert_StudyMaterial,name='insert_StudyMaterial'),
    path('fill_attendance',views.fill_attendance,name='fill_attendance'),
    path('insert_attendance',views.insert_attendance,name='insert_attendance'),
    path('insert_department',views.insert_department,name='insert_department'),

    

    #view
    path('show_student',views.show_student,name='show_student'),
    path('show_studentdetails',views.show_studentdetails,name='show_studentdetails'),
    path('show_assignment',views.show_assignment,name='show_assignment'),
    path('show_subjects',views.show_subjects,name='show_subjects'),
    path('show_submissions/',views.show_submissions,name='show_submissions'),
    path('show_timetable',views.show_timetable,name='show_timetable'),
    path('show_announcements',views.show_announcements,name='show_announcements'),
    path('show_feedback',views.show_feedback,name='show_feedback'),
    path('view_notifications',views.view_notifications,name='view_notifications'),
    path('view_exams',views.view_exams,name='view_exams'),
    path('view_examscores',views.view_examscores,name='view_examscores'),
    path('show_instructor',views.show_instructor,name='show_instructor'),
    path('show_instructor_admin',views.show_instructor_admin,name='show_instructor_admin'),
    
    path('show_StudyMaterial',views.show_StudyMaterial,name='show_StudyMaterial'),
    path('show_attedance',views.show_attedance,name='show_attedance'),
    path('show_student_attendance',views.show_student_attendance,name='show_student_attendance'),
    path('show_department',views.show_department,name='show_department'),

    #delete
    path('del_student<int:pk>',views.del_student,name='del_student'),
    path('del_assignment<int:pk>',views.del_assignment,name='del_assignment'),
    path('del_subjects<int:pk>',views.del_subjects,name='del_subjects'),
    path('del_submissions/<int:pk>', views.del_submissions, name='del_submissions'),
    path('del_timetable/<int:pk>',views.del_timetable,name='del_timetable'),
    path('del_attendance/<int:pk>',views.del_attendance,name='del_attendance'),
    path('del_announcements/<int:pk>',views.del_announcements,name='del_announcements'),
    path('del_feedback/<int:pk>',views.del_feedback,name='del_feedback'),
    path('del_notifications<int:pk>',views.del_notifications,name='del_notifications'),
    path('del_exams<int:pk>',views.del_exams,name='del_exams'),
    path('del_examscores<int:pk>',views.del_examscores,name='del_examscores'),
    path('del_instructor<int:pk>',views.del_instructor,name='del_instructor'),
    path('del_StudyMaterial<int:pk>',views.del_StudyMaterial,name='del_StudyMaterial'),
    path('del_department',views.del_department,name='del_department'),

    path('show_admin',views.show_admin,name='show_admin'),
    path('show_student',views.show_student,name='show_student'),
    path('show_staff',views.show_staff,name='show_staff'),
]
