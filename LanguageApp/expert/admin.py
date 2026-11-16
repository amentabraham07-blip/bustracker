from django.contrib import admin
from .models import Course, Video, Exams, Questions

# Simple registration
admin.site.register(Course)
admin.site.register(Video)
admin.site.register(Exams)
admin.site.register(Questions)