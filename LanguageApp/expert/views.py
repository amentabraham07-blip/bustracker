from django.shortcuts import render

# Create your views here.
from django.shortcuts import render,redirect
from django.contrib import messages
from expert.models import Course, Video, Exams ,Questions
from AdminDashboard.models import Language,User
from student.models import CourseEnrollment,Feedback,Doubts,ExamHistory
from django.db.models import Q



def teacher_dashboard(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get statistics
    total_courses = Course.objects.filter(expert_id=expert_id).count()
    total_videos = Video.objects.filter(course__expert_id=expert_id).count()
    total_exams = Exams.objects.filter(course__expert_id=expert_id).count()
    
    # Get total students enrolled in expert's courses
    course_ids = Course.objects.filter(expert_id=expert_id).values_list('id', flat=True)
    total_students = CourseEnrollment.objects.filter(course_id__in=course_ids).values('student_id').distinct().count()
    
    # Recent courses
    recent_courses = Course.objects.filter(expert_id=expert_id).select_related('language').order_by('-id')[:5]
    
    context = {
        'user_id': expert_id,
        'username': request.session.get('username'),
        'email': request.session.get('email'),
        'name': request.session.get('name'),
        'roll': request.session.get('roll'),
        'total_courses': total_courses,
        'total_videos': total_videos,
        'total_exams': total_exams,
        'total_students': total_students,
        'recent_courses': recent_courses,
    }
    
    return render(request, "expertd.html", context)

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from AdminDashboard.models import  Language
from expert.models import Course

def add_course(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    if request.method == "POST":
        language_id = request.POST.get("language")
        course_name = request.POST.get("course_name")
        description = request.POST.get("description")
        
        # Validation
        if not language_id or not course_name or not description:
            messages.error(request, "All fields are required.")
            return redirect("add_course")
        
        # Create course
        Course.objects.create(
            expert_id=request.session.get("user_id"),
            language_id=language_id,
            course_name=course_name,
            description=description
        )
        
        messages.success(request, "Course added successfully!")
        return redirect("manage_courses")
    
    # Get all languages for dropdown
    languages = Language.objects.all()
    
    context = {
        'languages': languages,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "add_course.html", context)


def manage_courses(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    # Get courses created by this expert
    expert_id = request.session.get("user_id")
    courses = Course.objects.filter(expert_id=expert_id).select_related('language')
    
    context = {
        'courses': courses,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "manage_courses.html", context)


def edit_course(request, course_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    # Get course and verify ownership
    course = get_object_or_404(Course, id=course_id, expert_id=request.session.get("user_id"))
    
    if request.method == "POST":
        language_id = request.POST.get("language")
        course_name = request.POST.get("course_name")
        description = request.POST.get("description")
        
        # Validation
        if not language_id or not course_name or not description:
            messages.error(request, "All fields are required.")
            return redirect("edit_course", course_id=course_id)
        
        # Update course
        course.language_id = language_id
        course.course_name = course_name
        course.description = description
        course.save()
        
        messages.success(request, "Course updated successfully!")
        return redirect("manage_courses")
    
    # Get all languages for dropdown
    languages = Language.objects.all()
    
    context = {
        'course': course,
        'languages': languages,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "edit_course.html", context)


def delete_course(request, course_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    # Get course and verify ownership
    course = get_object_or_404(Course, id=course_id, expert_id=request.session.get("user_id"))
    
    course.delete()
    messages.success(request, "Course deleted successfully!")
    
    return redirect("manage_courses")


from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    # Log out user (removes authenticated user)
    logout(request)

    # Completely flush session data
    request.session.flush()

    return redirect('login')


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Course, Video


def add_video(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    if request.method == "POST":
        course_id = request.POST.get("course")
        name = request.POST.get("name")
        description = request.POST.get("description")
        video_file = request.FILES.get("video_file")
        
        # Validation
        if not course_id or not name or not description or not video_file:
            messages.error(request, "All fields are required.")
            return redirect("add_video")
        
        # Verify course belongs to this expert
        course = Course.objects.filter(id=course_id, expert_id=expert_id).first()
        if not course:
            messages.error(request, "Invalid course selection.")
            return redirect("add_video")
        
        # Create video
        Video.objects.create(
            expert_id=expert_id,
            course_id=course_id,
            name=name,
            description=description,
            video_file=video_file
        )
        
        messages.success(request, "Video uploaded successfully!")
        return redirect("manage_videos")
    
    # Get courses created by this expert for dropdown
    courses = Course.objects.filter(expert_id=expert_id)
    
    context = {
        'courses': courses,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "add_video.html", context)


def manage_videos(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get filter parameter
    filter_course_id = request.GET.get("course_filter")
    
    # Get videos by this expert (ascending order of upload date)
    videos = Video.objects.filter(expert_id=expert_id).select_related('course').order_by('uploaded_at')
    
    # Apply course filter if selected
    if filter_course_id:
        videos = videos.filter(course_id=filter_course_id)
    
    # Get courses for filter dropdown
    courses = Course.objects.filter(expert_id=expert_id)
    
    context = {
        'videos': videos,
        'courses': courses,
        'selected_course': filter_course_id,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "manage_videos.html", context)


def edit_video(request, video_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get video and verify ownership
    video = get_object_or_404(Video, id=video_id, expert_id=expert_id)
    
    if request.method == "POST":
        name = request.POST.get("name")
        description = request.POST.get("description")
        
        # Validation
        if not name or not description:
            messages.error(request, "Name and description are required.")
            return redirect("edit_video", video_id=video_id)
        
        # Update video
        video.name = name
        video.description = description
        video.save()
        
        messages.success(request, "Video updated successfully!")
        return redirect("manage_videos")
    
    context = {
        'video': video,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "edit_video.html", context)


import os

def delete_video(request, video_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get video and verify ownership
    video = get_object_or_404(Video, id=video_id, expert_id=expert_id)
    
    # Try to delete video file
    try:
        if video.video_file:
            # Get the file path
            file_path = video.video_file.path
            
            # Delete the database record first
            video.delete()
            
            # Then try to delete the file
            if os.path.exists(file_path):
                try:
                    os.remove(file_path)
                except PermissionError:
                    # File is in use, skip deletion but inform user
                    messages.warning(request, "Video deleted !!.")
                    return redirect("manage_videos")
    except Exception as e:
        messages.error(request, f"Error deleting video: {str(e)}")
        return redirect("manage_videos")
    
    messages.success(request, "Video deleted successfully!")
    return redirect("manage_videos")


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Max
from .models import Course, Exams, Questions

def add_exam(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    if request.method == "POST":
        course_id = request.POST.get("course")
        exam_name = request.POST.get("exam_name")
        description = request.POST.get("description")
        
        # Validation
        if not course_id or not exam_name or not description:
            messages.error(request, "All fields are required.")
            return redirect("add_exam")
        
        # Verify course belongs to this expert
        course = Course.objects.filter(id=course_id, expert_id=expert_id).first()
        if not course:
            messages.error(request, "Invalid course selection.")
            return redirect("add_exam")
        
        # Auto-generate exam_no
        max_exam = Exams.objects.filter(course_id=course_id).aggregate(Max('exam_no'))
        exam_no = (max_exam['exam_no__max'] or 0) + 1
        
        # Create exam
        exam = Exams.objects.create(
            course_id=course_id,
            exam_name=exam_name,
            description=description,
            exam_no=exam_no
        )
        
        messages.success(request, f"Exam created successfully! Exam No: {exam_no}")
        return redirect("manage_exam", exam_id=exam.id)
    
    # Get courses created by this expert for dropdown
    courses = Course.objects.filter(expert_id=expert_id)
    
    context = {
        'courses': courses,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "add_exam.html", context)


def manage_exams(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get exams for courses created by this expert
    exams = Exams.objects.filter(course__expert_id=expert_id).select_related('course').order_by('-created_at')
    
    context = {
        'exams': exams,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "manage_exams.html", context)


def manage_exam(request, exam_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get exam and verify ownership
    exam = get_object_or_404(Exams, id=exam_id, course__expert_id=expert_id)
    
    # Get all questions for this exam
    questions = Questions.objects.filter(exam=exam).order_by('question_no')
    
    context = {
        'exam': exam,
        'questions': questions,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "manage_exam.html", context)


def add_question(request, exam_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get exam and verify ownership
    exam = get_object_or_404(Exams, id=exam_id, course__expert_id=expert_id)
    
    if request.method == "POST":
        question_text = request.POST.get("question")
        option_1 = request.POST.get("option_1")
        option_2 = request.POST.get("option_2")
        option_3 = request.POST.get("option_3")
        option_4 = request.POST.get("option_4")
        correct_option = request.POST.get("correct_option")
        
        # Validation
        if not all([question_text, option_1, option_2, option_3, option_4, correct_option]):
            messages.error(request, "All fields are required.")
            return redirect("manage_exam", exam_id=exam_id)
        
        # Auto-generate question_no
        max_question = Questions.objects.filter(exam=exam).aggregate(Max('question_no'))
        question_no = (max_question['question_no__max'] or 0) + 1
        
        # Create question
        Questions.objects.create(
            exam=exam,
            question_no=question_no,
            question=question_text,
            option_1=option_1,
            option_2=option_2,
            option_3=option_3,
            option_4=option_4,
            correct_option=correct_option
        )
        
        messages.success(request, f"Question {question_no} added successfully!")
        return redirect("manage_exam", exam_id=exam_id)
    
    return redirect("manage_exam", exam_id=exam_id)


def edit_question(request, question_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get question and verify ownership
    question = get_object_or_404(Questions, id=question_id, exam__course__expert_id=expert_id)
    
    if request.method == "POST":
        question_text = request.POST.get("question")
        option_1 = request.POST.get("option_1")
        option_2 = request.POST.get("option_2")
        option_3 = request.POST.get("option_3")
        option_4 = request.POST.get("option_4")
        correct_option = request.POST.get("correct_option")
        
        # Validation
        if not all([question_text, option_1, option_2, option_3, option_4, correct_option]):
            messages.error(request, "All fields are required.")
            return redirect("manage_exam", exam_id=question.exam.id)
        
        # Update question
        question.question = question_text
        question.option_1 = option_1
        question.option_2 = option_2
        question.option_3 = option_3
        question.option_4 = option_4
        question.correct_option = correct_option
        question.save()
        
        messages.success(request, "Question updated successfully!")
        return redirect("manage_exam", exam_id=question.exam.id)
    
    context = {
        'question': question,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "edit_question.html", context)


def delete_question(request, question_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get question and verify ownership
    question = get_object_or_404(Questions, id=question_id, exam__course__expert_id=expert_id)
    exam_id = question.exam.id
    
    question.delete()
    messages.success(request, "Question deleted successfully!")
    
    return redirect("manage_exam", exam_id=exam_id)


def edit_exam(request, exam_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get exam and verify ownership
    exam = get_object_or_404(Exams, id=exam_id, course__expert_id=expert_id)
    
    if request.method == "POST":
        exam_name = request.POST.get("exam_name")
        description = request.POST.get("description")
        
        # Validation
        if not exam_name or not description:
            messages.error(request, "All fields are required.")
            return redirect("edit_exam", exam_id=exam_id)
        
        # Update exam
        exam.exam_name = exam_name
        exam.description = description
        exam.save()
        
        messages.success(request, "Exam updated successfully!")
        return redirect("manage_exams")
    
    context = {
        'exam': exam,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "edit_exam.html", context)


def delete_exam(request, exam_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is mentor/expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only mentors can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get exam and verify ownership
    exam = get_object_or_404(Exams, id=exam_id, course__expert_id=expert_id)
    
    exam.delete()
    messages.success(request, "Exam and all its questions deleted successfully!")
    
    return redirect("manage_exams")


from django.utils import timezone

from django.utils import timezone
from django.db.models import Q, Max

def expert_doubts(request):
    """
    Expert doubts management - course-based with student chat list
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only experts can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get selected course and student from URL
    selected_course_id = request.GET.get('course_id')
    selected_student_id = request.GET.get('student_id')
    
    # Get all courses by this expert that have doubts
    course_ids_with_doubts = Doubts.objects.filter(receiver=expert_id).values_list('course_id', flat=True).distinct()
    courses_with_doubts = Course.objects.filter(id__in=course_ids_with_doubts, expert_id=expert_id).select_related('language')
    
    # Student chat list for selected course
    student_chats = []
    selected_course = None
    selected_student = None
    
    if selected_course_id:
        selected_course = Course.objects.filter(id=selected_course_id, expert_id=expert_id).first()
        
        if selected_course:
            # Get UNIQUE student IDs who asked doubts in this course
            # Group by sender and get distinct student IDs only
            unique_students = Doubts.objects.filter(
                course_id=selected_course_id,
                receiver=expert_id
            ).values('sender').annotate(
                last_message_time=Max('sent_at')
            ).order_by('-last_message_time')
            
            # Build chat list with unique students
            seen_students = set()
            for item in unique_students:
                student_id = item['sender']
                
                # Skip if already added
                if student_id in seen_students:
                    continue
                seen_students.add(student_id)
                
                # Get student details from User table
                try:
                    student = User.objects.get(id=student_id)
                    student_name = student.name
                    student_email = student.email
                except User.DoesNotExist:
                    student_name = f"Student {student_id}"
                    student_email = ""
                
                # Get last message from this student in this course
                last_doubt = Doubts.objects.filter(
                    course_id=selected_course_id
                ).filter(
                    Q(sender=student_id, receiver=expert_id) |
                    Q(sender=expert_id, receiver=student_id)
                ).order_by('-sent_at').first()
                
                student_chats.append({
                    'student_id': student_id,
                    'student_name': student_name,
                    'student_email': student_email,
                    'last_message': last_doubt.message if last_doubt else '',
                    'last_time': last_doubt.sent_at if last_doubt else None,
                })
            
            # Get selected student details
            if selected_student_id:
                try:
                    selected_student = User.objects.get(id=int(selected_student_id))
                except User.DoesNotExist:
                    selected_student = None
    
    elif courses_with_doubts.exists():
        # Auto-select first course
        selected_course = courses_with_doubts.first()
        selected_course_id = str(selected_course.id)
        
        # Get UNIQUE students for auto-selected course
        unique_students = Doubts.objects.filter(
            course_id=selected_course.id,
            receiver=expert_id
        ).values('sender').annotate(
            last_message_time=Max('sent_at')
        ).order_by('-last_message_time')
        
        seen_students = set()
        for item in unique_students:
            student_id = item['sender']
            
            if student_id in seen_students:
                continue
            seen_students.add(student_id)
            
            try:
                student = User.objects.get(id=student_id)
                student_name = student.name
                student_email = student.email
            except User.DoesNotExist:
                student_name = f"Student {student_id}"
                student_email = ""
            
            last_doubt = Doubts.objects.filter(
                course_id=selected_course.id
            ).filter(
                Q(sender=student_id, receiver=expert_id) |
                Q(sender=expert_id, receiver=student_id)
            ).order_by('-sent_at').first()
            
            student_chats.append({
                'student_id': student_id,
                'student_name': student_name,
                'student_email': student_email,
                'last_message': last_doubt.message if last_doubt else '',
                'last_time': last_doubt.sent_at if last_doubt else None,
            })
    
    # Get chat messages for selected student
    chat_messages = []
    if selected_course_id and selected_student_id:
        doubts = Doubts.objects.filter(
            course_id=selected_course_id
        ).filter(
            Q(sender=int(selected_student_id), receiver=expert_id) |
            Q(sender=expert_id, receiver=int(selected_student_id))
        ).order_by('sent_at')
        
        for doubt in doubts:
            try:
                video = Video.objects.get(id=doubt.video_id)
                chat_messages.append({
                    'doubt': doubt,
                    'video': video,
                    'is_mine': doubt.sender == expert_id
                })
            except Video.DoesNotExist:
                chat_messages.append({
                    'doubt': doubt,
                    'video': None,
                    'is_mine': doubt.sender == expert_id
                })
    
    # Get videos for selected course (for reply dropdown)
    videos_in_course = []
    if selected_course:
        videos_in_course = Video.objects.filter(course_id=selected_course.id).order_by('uploaded_at')
    
    # Statistics
    total_doubts = Doubts.objects.filter(receiver=expert_id).count()
    
    context = {
        'courses_with_doubts': courses_with_doubts,
        'selected_course': selected_course,
        'selected_course_id': selected_course_id,
        'student_chats': student_chats,
        'selected_student_id': selected_student_id,
        'selected_student': selected_student,
        'chat_messages': chat_messages,
        'videos_in_course': videos_in_course,
        'total_doubts': total_doubts,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "expert_doubts.html", context)

def expert_send_reply(request):
    """
    Expert sends reply to student doubt
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only experts can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        student_id = request.POST.get("student_id")
        video_id = request.POST.get("video_id")
        message_text = request.POST.get("message")
        
        if not message_text or not message_text.strip():
            return redirect(f"/expert-doubts/?course_id={course_id}&student_id={student_id}")
        
        if not video_id:
            return redirect(f"/expert-doubts/?course_id={course_id}&student_id={student_id}")
        
        # Verify course belongs to expert
        course = get_object_or_404(Course, id=course_id, expert_id=expert_id)
        video = get_object_or_404(Video, id=video_id)
        
        # Create reply message
        Doubts.objects.create(
            sender=expert_id,
            receiver=int(student_id),
            course_id=course.id,
            video_id=video.id,
            message=message_text.strip()
        )
        
        return redirect(f"/expert-doubts/?course_id={course_id}&student_id={student_id}")
    
    return redirect("expert_doubts")


def expert_view_feedback(request):
    """
    Expert view feedback from students - course filtered
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is expert
    if request.session.get("roll") != "mentor":
        messages.error(request, "Access denied. Only experts can access this page.")
        return redirect("login")
    
    expert_id = request.session.get("user_id")
    
    # Get filter parameter
    filter_course_id = request.GET.get('course_filter')
    
    # Get all courses by this expert
    expert_courses = Course.objects.filter(expert_id=expert_id).select_related('language')
    
    # Get feedbacks based on filter
    if filter_course_id:
        feedbacks = Feedback.objects.filter(
            course_id=filter_course_id,
            course__expert_id=expert_id
        ).select_related('course').order_by('-created_at')
        selected_course = Course.objects.filter(id=filter_course_id, expert_id=expert_id).first()
    else:
        feedbacks = Feedback.objects.filter(
            course__expert_id=expert_id
        ).select_related('course').order_by('-created_at')
        selected_course = None
    
    # Attach student names to feedbacks
    feedback_list = []
    for feedback in feedbacks:
        try:
            student = User.objects.get(id=feedback.student_id)
            student_name = student.name
            student_email = student.email
        except User.DoesNotExist:
            student_name = f"Student {feedback.student_id}"
            student_email = ""
        
        feedback_list.append({
            'feedback': feedback,
            'student_name': student_name,
            'student_email': student_email
        })
    
    # Calculate statistics
    total_feedbacks = feedbacks.count()
    
    # Average rating
    if total_feedbacks > 0:
        total_rating = sum([f.rating for f in feedbacks])
        average_rating = round(total_rating / total_feedbacks, 1)
    else:
        average_rating = 0
    
    # Rating distribution
    rating_counts = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for feedback in feedbacks:
        rating_counts[feedback.rating] += 1
    
    context = {
        'expert_courses': expert_courses,
        'selected_course': selected_course,
        'filter_course_id': filter_course_id,
        'feedback_list': feedback_list,
        'total_feedbacks': total_feedbacks,
        'average_rating': average_rating,
        'rating_counts': rating_counts,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "expert_feedback.html", context)
