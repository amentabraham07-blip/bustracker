from django.contrib import admin
from .models import CourseEnrollment, Feedback, Doubts, ExamHistory

admin.site.register(CourseEnrollment)
admin.site.register(Feedback)
admin.site.register(Doubts)
admin.site.register(ExamHistory)