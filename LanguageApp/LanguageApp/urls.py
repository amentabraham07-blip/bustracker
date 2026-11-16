"""
URL configuration for LanguageApp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from AdminDashboard import views as d_view
from LanguageApp import views as l_view
from expert import views as e_view 
from student import views as s_views 
from expert.views import logout_view
urlpatterns = [
    path('admin/', admin.site.urls),
    path('admindashboard/', d_view.AdminDashboard, name='admindashboard'),
    path('register/', l_view.register, name='register'),
    path("", l_view.login, name='login'),
    path('expertdashboard/', e_view.teacher_dashboard, name='expertdashboard'),
    path('add_course/', e_view.add_course, name='add_course'),
    path('manage-courses/', e_view.manage_courses, name='manage_courses'),
    path('edit-course/<int:course_id>/', e_view.edit_course, name='edit_course'),
    path('delete-course/<int:course_id>/', e_view.delete_course, name='delete_course'),
    path('logout/', logout_view, name='logout'),
    path('add-video/', e_view.add_video, name='add_video'),
    path('manage-videos/', e_view.manage_videos, name='manage_videos'),
    path('edit-video/<int:video_id>/', e_view.edit_video, name='edit_video'),
    path('delete-video/<int:video_id>/', e_view.delete_video, name='delete_video'),

    path('add-exam/', e_view.add_exam, name='add_exam'),
    path('manage-exams/', e_view.manage_exams, name='manage_exams'),
    path('manage-exam/<int:exam_id>/', e_view.manage_exam, name='manage_exam'),
    path('edit-exam/<int:exam_id>/', e_view.edit_exam, name='edit_exam'),
    path('delete-exam/<int:exam_id>/', e_view.delete_exam, name='delete_exam'),
    path('add-question/<int:exam_id>/', e_view.add_question, name='add_question'),
    path('edit-question/<int:question_id>/', e_view.edit_question, name='edit_question'),
    path('delete-question/<int:question_id>/', e_view.delete_question, name='delete_question'),
    path('student-dashboard/', s_views.student_dashboard, name='student_dashboard'),
    path('search-courses/', s_views.search_courses, name='search_courses'),
    path('enroll-course/<int:course_id>/', s_views.enroll_course, name='enroll_course'),
    path('my-courses/', s_views.my_courses, name='my_courses'),
    path('toggle-enrollment/<int:enrollment_id>/', s_views.toggle_enrollment, name='toggle_enrollment'),
    path('delete-enrollment/<int:enrollment_id>/', s_views.delete_enrollment, name='delete_enrollment'),
    path('add-feedback/<int:course_id>/', s_views.add_feedback, name='add_feedback'),
    path('my-videos/', s_views.my_videos, name='my_videos'),
    path('submit-doubt/<int:video_id>/', s_views.submit_doubt, name='submit_doubt'),
    path('my-exams/', s_views.my_exams, name='my_exams'),
    path('attempt-exam/<int:exam_id>/', s_views.attempt_exam, name='attempt_exam'),
    path('submit-exam/<int:exam_id>/', s_views.submit_exam, name='submit_exam'),
    path('exam-history/', s_views.exam_history, name='exam_history'),
    path('my-doubts/', s_views.my_doubts, name='my_doubts'),
    path('send-doubt-message/', s_views.send_doubt_message, name='send_doubt_message'),
    path('expert-doubts/', e_view.expert_doubts, name='expert_doubts'),
    path('expert-send-reply/', e_view.expert_send_reply, name='expert_send_reply'),
    path('expert-feedback/', e_view.expert_view_feedback, name='expert_view_feedback'),
    path('approve-expert/<int:user_id>/', d_view.approve_expert_action, name='approve_expert_action'),
    path('reject-expert/<int:user_id>/', d_view.reject_expert_action, name='reject_expert_action'),
    path('approve-experts/', d_view.approve_experts, name='approve_experts'),
    path('manage-students/', d_view.manage_students, name='manage_students'),
    path('delete-student/<int:user_id>/', d_view.delete_student, name='delete_student'),
    path('manage-experts/', d_view.manage_experts, name='manage_experts'),
    path('delete-expert/<int:user_id>/', d_view.delete_expert, name='delete_expert'),
    path('admin-manage-courses/', d_view.admin_manage_courses, name='admin_manage_courses'),
    path('admin-delete-course/<int:course_id>/', d_view.admin_delete_course, name='admin_delete_course'),
    path('admin-manage-videos/', d_view.admin_manage_videos, name='admin_manage_videos'),
    path('admin-delete-video/<int:video_id>/', d_view.admin_delete_video, name='admin_delete_video'),
    


]


from django.conf import settings
from django.conf.urls.static import static
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
