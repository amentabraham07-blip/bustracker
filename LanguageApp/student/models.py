from django.db import models

# Create your models here.
from expert.models import Course,Exams

class CourseEnrollment(models.Model):
    student_id = models.IntegerField()  # ID of the student
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrolled_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)  # For tracking if enrollment is active
    
    def __str__(self):
        return f"Student {self.student_id} enrolled in {self.course.course_name}"
    
    class Meta:
        ordering = ['-enrolled_at']
        unique_together = ['student_id', 'course']  # Prevent duplicate enrollments
        verbose_name = 'Course Enrollment'
        verbose_name_plural = 'Course Enrollments'

class Feedback(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='feedbacks')
    student_id = models.IntegerField()
    rating = models.IntegerField(choices=[(1, '1 Star'), (2, '2 Stars'), (3, '3 Stars'), (4, '4 Stars'), (5, '5 Stars')])
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Feedback by Student {self.student_id} for {self.course.course_name} - {self.rating} stars"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Feedback'
        verbose_name_plural = 'Feedbacks'

class Doubts(models.Model):
    sender = models.IntegerField()  # Student ID who sends the doubt
    receiver = models.IntegerField()  # Expert ID who receives the doubt
    course_id = models.IntegerField()  # Course related to the doubt
    video_id = models.IntegerField()  # Video related to the doubt
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Doubt from Student {self.sender} to Expert {self.receiver}"
    
    class Meta:
        ordering = ['-sent_at']
        verbose_name = 'Doubt'
        verbose_name_plural = 'Doubts'

class ExamHistory(models.Model):
    student_id = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exam_histories')
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE, related_name='exam_histories')
    scored_mark = models.IntegerField()
    total_mark = models.IntegerField()
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    def get_percentage(self):
        return round((self.scored_mark / self.total_mark) * 100, 2) if self.total_mark > 0 else 0
    
    def __str__(self):
        return f"Student {self.student_id} - {self.exam.exam_name} - Score: {self.scored_mark}/{self.total_mark}"
    
    class Meta:
        ordering = ['-attempted_at']
        verbose_name = 'Exam History'