from django.db import models
from AdminDashboard.models import Language

# Create your models here.
class Course(models.Model):
    expert_id = models.IntegerField()  # ID of the logged-in expert/mentor
    language = models.ForeignKey(Language, on_delete=models.CASCADE, related_name='courses')
    course_name = models.CharField(max_length=200)
    description = models.TextField()
    
    def __str__(self):
        return f"{self.course_name} - {self.language.language}"
    
class Video(models.Model):
    expert_id = models.IntegerField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='videos')
    name = models.CharField(max_length=200)
    description = models.TextField()
    video_file = models.FileField(upload_to='videos/')  # Video file upload
    uploaded_at = models.DateTimeField(auto_now_add=True)  # Track upload time
    
    def __str__(self):
        return f"{self.name} - {self.course.course_name}"  
    

class Exams(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='exams')
    exam_name = models.CharField(max_length=200)
    description = models.TextField()
    exam_no = models.IntegerField()  # Exam number (e.g., 1, 2, 3)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.exam_name} - {self.course.course_name} (Exam {self.exam_no})"
    
    class Meta:
        ordering = ['course', 'exam_no']
        unique_together = ['course', 'exam_no']  # Prevent duplicate exam numbers in same course
        verbose_name = 'Exam'
        verbose_name_plural = 'Exams'


class Questions(models.Model):
    exam = models.ForeignKey(Exams, on_delete=models.CASCADE, related_name='questions')
    question_no = models.IntegerField()  # Question number within the exam
    question = models.TextField()  # The actual question text
    option_1 = models.CharField(max_length=500)
    option_2 = models.CharField(max_length=500)
    option_3 = models.CharField(max_length=500)
    option_4 = models.CharField(max_length=500)
    correct_option = models.IntegerField(choices=[(1, 'Option 1'), (2, 'Option 2'), (3, 'Option 3'), (4, 'Option 4')])
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.exam.exam_name} - Q{self.question_no}: {self.question[:50]}"
    
    class Meta:
        ordering = ['exam', 'question_no']
        unique_together = ['exam', 'question_no']  # Prevent duplicate question numbers in same exam
        verbose_name = 'Question'
        verbose_name_plural = 'Questions'