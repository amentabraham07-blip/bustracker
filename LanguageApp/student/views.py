from django.shortcuts import render

# Create your views here.


from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Q, Count
from expert.models import Course, Video, Exams ,Questions
from AdminDashboard.models import Language
from student.models import CourseEnrollment,Feedback,Doubts,ExamHistory


def student_dashboard(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get student's enrolled courses count
    enrolled_courses_count = CourseEnrollment.objects.filter(student_id=student_id, is_active=True).count()
    
    # Get TOTAL system counts (not student-specific)
    total_videos = Video.objects.count()  # Total videos in system
    total_courses = Course.objects.count()  # Total courses in system
    total_experts = Course.objects.values('expert_id').distinct().count()  # Total unique experts
    
    # Get all available courses for enrollment
    all_courses = Course.objects.all().select_related('language')
    
    # Get student's enrolled course IDs to mark them
    enrolled_courses = CourseEnrollment.objects.filter(
        student_id=student_id, 
        is_active=True
    ).values_list('course_id', flat=True)
    
    # Get all languages for search dropdown
    
    languages = Language.objects.all()
    
    context = {
        'enrolled_courses_count': enrolled_courses_count,
        'total_videos': total_videos,
        'total_courses': total_courses,
        'total_experts': total_experts,
        'all_courses': all_courses,
        'enrolled_courses': list(enrolled_courses),
        'languages': languages,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "student_dashboard.html", context)


def search_courses(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get search parameters
    course_name = request.GET.get('course_name', '').strip()
    language_id = request.GET.get('language', '').strip()
    
    # Build query
    courses = Course.objects.all().select_related('language')
    
    if course_name:
        courses = courses.filter(course_name__icontains=course_name)
    
    if language_id:
        courses = courses.filter(language_id=language_id)
    
    # Get student's enrolled course IDs
    enrolled_courses = CourseEnrollment.objects.filter(
        student_id=student_id, 
        is_active=True
    ).values_list('course_id', flat=True)
    
    # Get student's enrolled courses count
    enrolled_courses_count = len(enrolled_courses)
    
    # Get TOTAL system counts
    total_videos = Video.objects.count()
    total_courses = Course.objects.count()
    total_experts = Course.objects.values('expert_id').distinct().count()
    
    # Get all languages for dropdown
    
    languages = Language.objects.all()
    
    context = {
        'enrolled_courses_count': enrolled_courses_count,
        'total_videos': total_videos,
        'total_courses': total_courses,
        'total_experts': total_experts,
        'all_courses': courses,
        'enrolled_courses': list(enrolled_courses),
        'languages': languages,
        'search_course_name': course_name,
        'search_language': language_id,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "student_dashboard.html", context)

def enroll_course(request, course_id):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Check if course exists
    course = get_object_or_404(Course, id=course_id)
    
    # Check if enrollment already exists
    enrollment = CourseEnrollment.objects.filter(student_id=student_id, course_id=course_id).first()
    
    if enrollment:
        if enrollment.is_active:
            messages.info(request, "You are already enrolled in this course.")
        else:
            # Reactivate enrollment
            enrollment.is_active = True
            enrollment.save()
            messages.success(request, f"Successfully re-enrolled in {course.course_name}!")
    else:
        # Create new enrollment
        CourseEnrollment.objects.create(
            student_id=student_id,
            course=course,
            is_active=True
        )
        messages.success(request, f"Successfully enrolled in {course.course_name}!")
    
    return redirect("student_dashboard")




from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.db.models import Avg



def my_courses(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get all enrollments (both active and inactive)
    enrollments = CourseEnrollment.objects.filter(
        student_id=student_id
    ).select_related('course', 'course__language').order_by('-enrolled_at')
    
    # Get existing feedbacks for this student
    student_feedbacks = Feedback.objects.filter(student_id=student_id).values_list('course_id', flat=True)
    
    # Debug print (remove after checking)
    print(f"Student ID: {student_id}")
    print(f"Enrollments count: {enrollments.count()}")
    print(f"Student feedbacks: {list(student_feedbacks)}")
    
    context = {
        'enrollments': enrollments,
        'student_feedbacks': list(student_feedbacks),
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "my_courses.html", context)


def toggle_enrollment(request, enrollment_id):
    """
    Toggle enrollment status between active and inactive
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get enrollment and verify ownership
    enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id, student_id=student_id)
    
    # Toggle is_active status
    enrollment.is_active = not enrollment.is_active
    enrollment.save()
    
    if enrollment.is_active:
        messages.success(request, f"Course '{enrollment.course.course_name}' activated successfully!")
    else:
        messages.warning(request, f"Course '{enrollment.course.course_name}' deactivated successfully!")
    
    return redirect("my_courses")


def delete_enrollment(request, enrollment_id):
    """
    Permanently delete an enrollment
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get enrollment and verify ownership
    enrollment = get_object_or_404(CourseEnrollment, id=enrollment_id, student_id=student_id)
    
    course_name = enrollment.course.course_name
    enrollment.delete()
    
    messages.success(request, f"Enrollment in '{course_name}' deleted successfully!")
    
    return redirect("my_courses")


def add_feedback(request, course_id):
    """
    Add or update feedback for a course
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    if request.method == "POST":
        rating = request.POST.get("rating")
        message = request.POST.get("message")
        
        # Validation
        if not rating or not message:
            messages.error(request, "Rating and message are required.")
            return redirect("my_courses")
        
        # Check if course exists and student is enrolled
        course = get_object_or_404(Course, id=course_id)
        enrollment = CourseEnrollment.objects.filter(
            student_id=student_id, 
            course_id=course_id, 
            is_active=True
        ).first()
        
        if not enrollment:
            messages.error(request, "You must be actively enrolled in this course to submit feedback.")
            return redirect("my_courses")
        
        # Check if feedback already exists
        existing_feedback = Feedback.objects.filter(student_id=student_id, course_id=course_id).first()
        
        if existing_feedback:
            # Update existing feedback
            existing_feedback.rating = rating
            existing_feedback.message = message
            existing_feedback.save()
            messages.success(request, "Your feedback has been updated successfully!")
        else:
            # Create new feedback
            Feedback.objects.create(
                course_id=course_id,
                student_id=student_id,
                rating=rating,
                message=message
            )
            messages.success(request, "Thank you for your feedback!")
        
        return redirect("my_courses")
    
    return redirect("my_courses")


def my_videos(request):
    """
    Display videos from enrolled courses with filter by course
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get enrolled courses (active only)
    enrolled_courses = CourseEnrollment.objects.filter(
        student_id=student_id,
        is_active=True
    ).select_related('course').values_list('course_id', flat=True)
    
    # Get courses for dropdown
    courses = Course.objects.filter(id__in=enrolled_courses).select_related('language')
    
    # Get selected course from filter
    selected_course_id = request.GET.get('course_filter')
    
    # Get videos based on filter
    if selected_course_id:
        videos = Video.objects.filter(
            course_id=selected_course_id,
            course_id__in=enrolled_courses
        ).select_related('course').order_by('uploaded_at')
    else:
        # Show all videos from enrolled courses
        videos = Video.objects.filter(
            course_id__in=enrolled_courses
        ).select_related('course').order_by('uploaded_at')
    
    context = {
        'courses': courses,
        'videos': videos,
        'selected_course_id': selected_course_id,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "my_videos.html", context)


def submit_doubt(request, video_id):
    """
    Submit a doubt for a specific video
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    if request.method == "POST":
        message = request.POST.get("message")
        
        # Validation
        if not message or not message.strip():
            messages.error(request, "Doubt message cannot be empty.")
            return redirect("my_videos")
        
        # Get video and course details
        video = get_object_or_404(Video, id=video_id)
        course = video.course
        
        # Check if student is enrolled in this course
        enrollment = CourseEnrollment.objects.filter(
            student_id=student_id,
            course_id=course.id,
            is_active=True
        ).first()
        
        if not enrollment:
            messages.error(request, "You must be enrolled in this course to ask doubts.")
            return redirect("my_videos")
        
        # Create doubt
        Doubts.objects.create(
            sender=student_id,
            receiver=course.expert_id,  # Expert who created the course
            course_id=course.id,
            video_id=video.id,
            message=message.strip()
        )
        
        messages.success(request, "Your doubt has been submitted successfully! The expert will respond soon.")
        return redirect("my_videos")
    
    return redirect("my_videos")


from django.db.models import Count

def my_exams(request):
    """
    Display available exams from enrolled courses with filter
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get enrolled courses (active only)
    enrolled_courses = CourseEnrollment.objects.filter(
        student_id=student_id,
        is_active=True
    ).values_list('course_id', flat=True)
    
    # Get courses for dropdown
    courses = Course.objects.filter(id__in=enrolled_courses).select_related('language')
    
    # Get selected course from filter
    selected_course_id = request.GET.get('course_filter')
    
    # Get exams based on filter
    if selected_course_id:
        exams = Exams.objects.filter(
            course_id=selected_course_id,
            course_id__in=enrolled_courses
        ).select_related('course').annotate(question_count=Count('questions')).order_by('exam_no')
    else:
        # Show all exams from enrolled courses
        exams = Exams.objects.filter(
            course_id__in=enrolled_courses
        ).select_related('course').annotate(question_count=Count('questions')).order_by('course', 'exam_no')
    
    # Get exam history to mark attempted exams
    attempted_exams = ExamHistory.objects.filter(student_id=student_id).values_list('exam_id', flat=True)
    
    context = {
        'courses': courses,
        'exams': exams,
        'selected_course_id': selected_course_id,
        'attempted_exams': list(attempted_exams),
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "my_exams.html", context)


def attempt_exam(request, exam_id):
    """
    Display exam questions for attempting
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get exam and verify enrollment
    exam = get_object_or_404(Exams, id=exam_id)
    
    enrollment = CourseEnrollment.objects.filter(
        student_id=student_id,
        course_id=exam.course.id,
        is_active=True
    ).first()
    
    if not enrollment:
        messages.error(request, "You must be enrolled in this course to attempt the exam.")
        return redirect("my_exams")
    
    # Get all questions for this exam
    questions = Questions.objects.filter(exam=exam).order_by('question_no')
    
    if not questions.exists():
        messages.error(request, "This exam has no questions yet.")
        return redirect("my_exams")
    
    context = {
        'exam': exam,
        'questions': questions,
        'total_questions': questions.count(),
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "attempt_exam.html", context)


def submit_exam(request, exam_id):
    """
    Submit exam, calculate score, and show results
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    if request.method == "POST":
        # Get exam
        exam = get_object_or_404(Exams, id=exam_id)
        
        # Get all questions
        questions = Questions.objects.filter(exam=exam).order_by('question_no')
        
        # Calculate score
        scored_mark = 0
        total_mark = questions.count()
        results = []
        
        for question in questions:
            student_answer = request.POST.get(f"question_{question.id}")
            is_correct = False
            
            if student_answer:
                student_answer = int(student_answer)
                if student_answer == question.correct_option:
                    scored_mark += 1
                    is_correct = True
            
            results.append({
                'question': question,
                'student_answer': student_answer,
                'is_correct': is_correct,
                'correct_answer': question.correct_option
            })
        
        # Save to exam history
        ExamHistory.objects.create(
            student_id=student_id,
            course=exam.course,  # Changed from course_id
            exam=exam,           # Changed from exam_id
            scored_mark=scored_mark,
            total_mark=total_mark
             )
        
        # Calculate percentage
        percentage = round((scored_mark / total_mark) * 100, 2) if total_mark > 0 else 0
        
        context = {
            'exam': exam,
            'results': results,
            'scored_mark': scored_mark,
            'total_mark': total_mark,
            'percentage': percentage,
            'name': request.session.get('name'),
            'username': request.session.get('username'),
            'email': request.session.get('email'),
        }
        
        return render(request, "exam_result.html", context)
    
    return redirect("my_exams")


def exam_history(request):
    """
    Display student's exam history with scores and statistics
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get filter parameter
    filter_course_id = request.GET.get('course_filter')
    
    # Get all exam attempts with related data
    exam_attempts_query = ExamHistory.objects.filter(
        student_id=student_id
    ).select_related('exam', 'exam__course', 'course')
    
    # Apply course filter if selected
    if filter_course_id:
        exam_attempts_query = exam_attempts_query.filter(course_id=filter_course_id)
    
    exam_attempts = exam_attempts_query.order_by('-attempted_at')
    
    # Calculate statistics (from all attempts, not filtered)
    all_attempts = ExamHistory.objects.filter(student_id=student_id)
    total_attempts = all_attempts.count()
    
    if total_attempts > 0:
        total_scored = sum([attempt.scored_mark for attempt in all_attempts])
        total_marks = sum([attempt.total_mark for attempt in all_attempts])
        average_percentage = round((total_scored / total_marks) * 100, 2) if total_marks > 0 else 0
        
        # Count pass/fail (assuming 50% is pass)
        passed = sum([1 for attempt in all_attempts if attempt.get_percentage() >= 50])
        failed = total_attempts - passed
    else:
        average_percentage = 0
        passed = 0
        failed = 0
    
    # Get courses for filter dropdown
    courses = Course.objects.filter(
        id__in=all_attempts.values_list('course_id', flat=True).distinct()
    ).select_related('language')
    
    context = {
        'exam_attempts': exam_attempts,
        'total_attempts': total_attempts,
        'average_percentage': average_percentage,
        'passed': passed,
        'failed': failed,
        'courses': courses,
        'selected_course_id': filter_course_id,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "exam_history.html", context)


from django.db.models import Q

def my_doubts(request):
    """
    Display course-based chat interface for doubts
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    # Get selected course from URL parameter
    selected_course_id = request.GET.get('course_id')
    
    # Get all courses where student has sent doubts
    course_ids_with_doubts = Doubts.objects.filter(sender=student_id).values_list('course_id', flat=True).distinct()
    courses_with_doubts = Course.objects.filter(id__in=course_ids_with_doubts).select_related('language')
    
    # Get chat messages for selected course
    chat_messages = []
    selected_course = None
    
    if selected_course_id:
        selected_course = Course.objects.filter(id=selected_course_id).first()
        if selected_course:
            # Get all doubts for this course (both from student and expert replies)
            doubts = Doubts.objects.filter(
                course_id=selected_course_id
            ).filter(
                Q(sender=student_id) | Q(receiver=student_id)
            ).order_by('sent_at')
            
            for doubt in doubts:
                try:
                    video = Video.objects.get(id=doubt.video_id)
                    chat_messages.append({
                        'doubt': doubt,
                        'video': video,
                        'is_mine': doubt.sender == student_id
                    })
                except Video.DoesNotExist:
                    chat_messages.append({
                        'doubt': doubt,
                        'video': None,
                        'is_mine': doubt.sender == student_id
                    })
    elif courses_with_doubts.exists():
        # Auto-select first course
        selected_course = courses_with_doubts.first()
        selected_course_id = str(selected_course.id)
        
        doubts = Doubts.objects.filter(
            course_id=selected_course.id
        ).filter(
            Q(sender=student_id) | Q(receiver=student_id)
        ).order_by('sent_at')
        
        for doubt in doubts:
            try:
                video = Video.objects.get(id=doubt.video_id)
                chat_messages.append({
                    'doubt': doubt,
                    'video': video,
                    'is_mine': doubt.sender == student_id
                })
            except Video.DoesNotExist:
                chat_messages.append({
                    'doubt': doubt,
                    'video': None,
                    'is_mine': doubt.sender == student_id
                })
    
    # Get videos for selected course (for dropdown in send message)
    videos_in_course = []
    if selected_course:
        videos_in_course = Video.objects.filter(course_id=selected_course.id).order_by('uploaded_at')
    
    # Statistics
    total_doubts = Doubts.objects.filter(sender=student_id).count()
    
    context = {
        'courses_with_doubts': courses_with_doubts,
        'selected_course': selected_course,
        'selected_course_id': selected_course_id,
        'chat_messages': chat_messages,
        'videos_in_course': videos_in_course,
        'total_doubts': total_doubts,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "my_doubts.html", context)


def send_doubt_message(request):
    """
    Send a new doubt message in the course chat
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is student
    if request.session.get("roll") != "student":
        messages.error(request, "Access denied. Only students can access this page.")
        return redirect("login")
    
    student_id = request.session.get("user_id")
    
    if request.method == "POST":
        course_id = request.POST.get("course_id")
        video_id = request.POST.get("video_id")
        message_text = request.POST.get("message")
        
        if not message_text or not message_text.strip():
            return redirect(f"/my-doubts/?course_id={course_id}")
        
        if not video_id:
            return redirect(f"/my-doubts/?course_id={course_id}")
        
        # Get course and video
        course = get_object_or_404(Course, id=course_id)
        video = get_object_or_404(Video, id=video_id)
        
        # Check enrollment
        enrollment = CourseEnrollment.objects.filter(
            student_id=student_id,
            course_id=course_id,
            is_active=True
        ).first()
        
        if not enrollment:
            messages.error(request, "You must be enrolled in this course.")
            return redirect("my_doubts")
        
        # Create doubt message
        Doubts.objects.create(
            sender=student_id,
            receiver=course.expert_id,
            course_id=course.id,
            video_id=video.id,
            message=message_text.strip()
        )
        
        # No success message - just redirect
        return redirect(f"/my-doubts/?course_id={course_id}")
    
    return redirect("my_doubts")