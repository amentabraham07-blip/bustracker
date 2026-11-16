from django.shortcuts import render, redirect ,get_object_or_404
from django.db.models import Q
from django.contrib import messages
from expert.models import Course, Video, Exams ,Questions
from AdminDashboard.models import Language,User
from student.models import CourseEnrollment,Feedback,Doubts,ExamHistory
def AdminDashboard(request):
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    # Statistics
    total_students = User.objects.filter(roll="student").count()
    total_experts = User.objects.filter(roll="mentor").count()
    total_courses = Course.objects.count()
    total_videos = Video.objects.count()
    total_enrollments = CourseEnrollment.objects.count()
    pending_experts = User.objects.filter(roll="mentor", status="pending").count()
    approved_experts = User.objects.filter(roll="mentor", status="approved").count()
    
    # Recent users
    recent_students = User.objects.filter(roll="student").order_by('-id')[:5]
    recent_experts = User.objects.filter(roll="mentor").order_by('-id')[:5]
    
    context = {
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
        'roll': request.session.get('roll'),
        'total_students': total_students,
        'total_experts': total_experts,
        'total_courses': total_courses,
        'total_videos': total_videos,
        'total_enrollments': total_enrollments,
        'pending_experts': pending_experts,
        'approved_experts': approved_experts,
        'recent_students': recent_students,
        'recent_experts': recent_experts,
    }
    
    return render(request, 'admind.html', context)


def approve_experts(request):
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    pending_experts = User.objects.filter(roll="mentor", status="pending").order_by('-id')
    
    context = {
        'pending_experts': pending_experts,
        'pending_count': User.objects.filter(roll="mentor", status="pending").count(),
        'approved_count': User.objects.filter(roll="mentor", status="approved").count(),
        'rejected_count': User.objects.filter(roll="mentor", status="rejected").count(),
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "approve_experts.html", context)


def approve_expert_action(request, user_id):
    """
    Approve a pending expert
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    expert = get_object_or_404(User, id=user_id, roll="mentor")
    expert.status = "approved"
    expert.save()
    
    messages.success(request, f"Expert '{expert.name}' has been approved successfully!")
    return redirect("approve_experts")


def reject_expert_action(request, user_id):
    """
    Reject a pending expert
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    expert = get_object_or_404(User, id=user_id, roll="mentor")
    expert.status = "rejected"
    expert.save()
    
    messages.success(request, f"Expert '{expert.name}' has been rejected.")
    return redirect("approve_experts")


def manage_students(request):
    """
    Admin view to manage students with search and delete
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    # Get search query
    search_query = request.GET.get('search', '').strip()
    
    # Get all students
    students = User.objects.filter(roll="student").order_by('-id')
    
    # Apply search filter
    if search_query:
        students = students.filter(
            Q(name__icontains=search_query) | 
            Q(username__icontains=search_query)
        )
    
    context = {
        'students': students,
        'total_students': User.objects.filter(roll="student").count(),
        'search_query': search_query,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "manage_students.html", context)


def delete_student(request, user_id):
    """
    Delete a student
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    student = get_object_or_404(User, id=user_id, roll="student")
    student_name = student.name
    student.delete()
    
    messages.success(request, f"Student '{student_name}' has been deleted successfully!")
    return redirect("manage_students")


def manage_experts(request):
    """
    Admin view to manage experts with search and delete
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    # Get search query
    search_query = request.GET.get('search', '').strip()
    
    # Get all experts
    experts = User.objects.filter(roll="mentor").order_by('-id')
    
    # Apply search filter
    if search_query:
        experts = experts.filter(
            Q(name__icontains=search_query) | 
            Q(username__icontains=search_query)
        )
    
    # Count by status
    total_experts = User.objects.filter(roll="mentor").count()
    approved_experts = User.objects.filter(roll="mentor", status="approved").count()
    pending_experts = User.objects.filter(roll="mentor", status="pending").count()
    rejected_experts = User.objects.filter(roll="mentor", status="rejected").count()
    
    context = {
        'experts': experts,
        'total_experts': total_experts,
        'approved_experts': approved_experts,
        'pending_experts': pending_experts,
        'rejected_experts': rejected_experts,
        'search_query': search_query,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "manage_experts.html", context)


def delete_expert(request, user_id):
    """
    Delete an expert
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    expert = get_object_or_404(User, id=user_id, roll="mentor")
    expert_name = expert.name
    expert.delete()
    
    messages.success(request, f"Expert '{expert_name}' has been deleted successfully!")
    return redirect("manage_experts")



def admin_manage_courses(request):
    """
    Admin view to manage courses with search by expert name, course name, and language
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    # Get search query
    search_query = request.GET.get('search', '').strip()
    
    # Get all courses with related language
    courses = Course.objects.select_related('language').order_by('-id')
    
    # Apply search filter
    if search_query:
        # Get expert IDs matching the search query
        expert_ids = User.objects.filter(
            Q(name__icontains=search_query) | Q(username__icontains=search_query),
            roll="mentor"
        ).values_list('id', flat=True)
        
        # Search in course name, language, or expert
        courses = courses.filter(
            Q(course_name__icontains=search_query) |
            Q(language__language__icontains=search_query) |
            Q(expert_id__in=expert_ids)
        )
    
    # Attach expert names to courses
    courses_list = []
    for course in courses:
        try:
            expert = User.objects.get(id=course.expert_id)
            expert_name = expert.name
            expert_email = expert.email
        except User.DoesNotExist:
            expert_name = f"Expert {course.expert_id}"
            expert_email = ""
        
        courses_list.append({
            'course': course,
            'expert_name': expert_name,
            'expert_email': expert_email
        })
    
    # Get statistics
    total_courses = Course.objects.count()
    total_languages = Language.objects.count()
    
    context = {
        'courses_list': courses_list,
        'total_courses': total_courses,
        'total_languages': total_languages,
        'search_query': search_query,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "admin_manage_courses.html", context)


def admin_delete_course(request, course_id):
    """
    Delete a course
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    course = get_object_or_404(Course, id=course_id)
    course_name = course.course_name
    course.delete()
    
    messages.success(request, f"Course '{course_name}' has been deleted successfully!")
    return redirect("admin_manage_courses")



def admin_manage_videos(request):
    """
    Admin view to manage videos with search by video name, course name, expert name
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    # Get search query
    search_query = request.GET.get('search', '').strip()
    
    # Get all videos with related course
    videos = Video.objects.select_related('course', 'course__language').order_by('-uploaded_at')
    
    # Apply search filter
    if search_query:
        # Get expert IDs matching the search query
        expert_ids = User.objects.filter(
            Q(name__icontains=search_query) | Q(username__icontains=search_query),
            roll="mentor"
        ).values_list('id', flat=True)
        
        # Search in video name, course name, or expert
        videos = videos.filter(
            Q(name__icontains=search_query) |
            Q(course__course_name__icontains=search_query) |
            Q(course__expert_id__in=expert_ids)
        )
    
    # Attach expert names to videos
    videos_list = []
    for video in videos:
        try:
            expert = User.objects.get(id=video.course.expert_id)
            expert_name = expert.name
            expert_email = expert.email
        except User.DoesNotExist:
            expert_name = f"Expert {video.course.expert_id}"
            expert_email = ""
        
        videos_list.append({
            'video': video,
            'expert_name': expert_name,
            'expert_email': expert_email
        })
    
    # Get statistics
    total_videos = Video.objects.count()
    total_courses = Course.objects.count()
    
    context = {
        'videos_list': videos_list,
        'total_videos': total_videos,
        'total_courses': total_courses,
        'search_query': search_query,
        'name': request.session.get('name'),
        'username': request.session.get('username'),
        'email': request.session.get('email'),
    }
    
    return render(request, "admin_manage_videos.html", context)


def admin_delete_video(request, video_id):
    """
    Delete a video
    """
    # Check if user is logged in
    if "user_id" not in request.session:
        messages.error(request, "Please login to access this page.")
        return redirect("login")
    
    # Check if user role is admin
    if request.session.get("roll") != "admin":
        messages.error(request, "Access denied.")
        return redirect("login")
    
    video = get_object_or_404(Video, id=video_id)
    video_name = video.name
    
    # Delete video file if exists
    if video.video_file:
        try:
            video.video_file.delete()
        except:
            pass
    
    video.delete()
    
    messages.success(request, f"Video '{video_name}' has been deleted successfully!")
    return redirect("admin_manage_videos")