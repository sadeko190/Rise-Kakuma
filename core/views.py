from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from .models import Course, Lesson, Job, JobApplication, Slot, Booking


# ---------------- PUBLIC PAGES ----------------
def home(request):
    return render(request, 'core/home.html')

def about(request):
    return render(request, 'core/about.html')

def contact(request):
    if request.method == 'POST':
        return redirect('contact_success')
    return render(request, 'core/contact.html')

def contact_success(request):
    return render(request, 'core/contact_success.html')


# ---------------- AUTH ----------------
def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


# ---------------- DASHBOARD ----------------
@login_required(login_url='login')
def dashboard(request):
    context = {
        'total_courses': Course.objects.count(),
        'total_jobs': Job.objects.count(),
        'total_lessons': Lesson.objects.count(),
    }
    return render(request, 'core/dashboard.html', context)


# ---------------- COURSES ----------------
@login_required(login_url='login')
def course_list(request):
    courses = Course.objects.all()
    return render(request, 'courses/course_list.html', {'courses': courses})

@login_required(login_url='login')
def course_detail(request, course_id):
    course = get_object_or_404(Course, id=course_id)
    return render(request, 'courses/course_detail.html', {'course': course})

@login_required(login_url='login')
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})


# ---------------- JOBS ----------------
@login_required(login_url='login')
def job_list(request):
    jobs = Job.objects.all()
    return render(request, 'jobs/job_list.html', {'jobs': jobs})

@login_required(login_url='login')
def apply_job(request, job_id):
    job = get_object_or_404(Job, id=job_id)

    if request.method == 'POST':
        resume_file = request.FILES.get('resume')  # get uploaded file
        cover_letter = request.POST.get('cover_letter', '')  # optional

        if resume_file:
            JobApplication.objects.create(
                job=job,
                user=request.user,
                resume=resume_file,
                cover_letter=cover_letter
            )
            return redirect('application_success')

    return render(request, 'jobs/apply_job.html', {'job': job})

@login_required(login_url='login')
def job_applicants(request, job_id):
    job = get_object_or_404(Job, id=job_id)
    applicants = JobApplication.objects.filter(job=job)
    return render(request, 'jobs/job_applicants.html', {'job': job, 'applicants': applicants})


# ---------------- BOOKING ----------------
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .models import Slot, Booking

@login_required(login_url='login')
def booking_list(request):
    # Show all slots
    slots = Slot.objects.all()
    return render(request, 'booking/booking_list.html', {'slots': slots})

@login_required(login_url='login')
def book_slot(request, slot_id):
    slot = get_object_or_404(Slot, id=slot_id)

    # Check if this user already booked this slot
    already_booked = Booking.objects.filter(slot=slot, user=request.user).exists()
    if already_booked:
        return HttpResponse("You already booked this slot!")

    if request.method == 'POST':
        notes = request.POST.get('notes', '')  # optional notes
        Booking.objects.create(slot=slot, user=request.user, notes=notes)
        return redirect('booking_success')

    return render(request, 'booking/book_slot.html', {'slot': slot})

@login_required(login_url='login')
def booking_success(request):
    return render(request, 'booking/booking_success.html')

@login_required(login_url='login')
def my_bookings(request):
    # Show only bookings for the logged-in user
    bookings = Booking.objects.filter(user=request.user)
    return render(request, 'booking/my_bookings.html', {'bookings': bookings})

@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('my_bookings')


# ---------------- CHALLENGES ----------------
# def challenge_list(request):
#     challenges = Challenge.objects.all()
#     return render(request, 'challenges/challenge_list.html', {'challenges': challenges})

# def challenge_detail(request, challenge_id):
#     challenge = get_object_or_404(Challenge, id=challenge_id)
#     return render(request, 'challenges/challenge_detail.html', {'challenge': challenge})


# ---------------- DONATE ----------------
# core/views.py

from django.shortcuts import render, redirect
from .forms import DonateForm

def donate(request):
    if request.method == 'POST':
        form = DonateForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donate_success')
    else:
        form = DonateForm()
    return render(request, 'core/donate.html', {'form': form})


def donate_success(request):
    return render(request, 'core/donate_success.html')

# ---------------- MPESA ----------------
@csrf_exempt
def stk_push(request):
    return HttpResponse("STK Push Simulated")

@csrf_exempt
def mpesa_callback(request):
    return HttpResponse("MPESA Callback Received")







from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Booking

@login_required(login_url='login')
def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id, user=request.user)
    booking.delete()
    return redirect('my_bookings')




from .forms import ContactForm
from .models import ContactMessage

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Save to database
            ContactMessage.objects.create(
                name=form.cleaned_data['name'],
                email=form.cleaned_data['email'],
                subject=form.cleaned_data['subject'],
                message=form.cleaned_data['message']
            )
            return redirect('contact_success')
    else:
        form = ContactForm()
    return render(request, 'core/contact.html', {'form': form})



from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required

# ---------------- AUTH ----------------
from django.contrib.auth.models import User
from django.contrib.auth import login

from .forms import CustomUserCreationForm
from django.contrib.auth import login

from .forms import CustomUserCreationForm

def signup_view(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
        else:
            # invalid login
            return render(request, 'registration/login.html', {'form': form, 'error': 'Invalid username or password'})
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('home')


@login_required(login_url='login')
def profile_view(request):
    # Get all courses
    courses = Course.objects.all()
    
    # Optionally, get lessons for each course
    lessons = Lesson.objects.all()
    
    # Get jobs the user applied to
    job_applications = JobApplication.objects.filter(user=request.user)
    
    context = {
        'courses': courses,
        'lessons': lessons,
        'job_applications': job_applications,
    }
    return render(request, 'registration/profile.html', context)

@login_required(login_url='login')
def lesson_detail(request, lesson_id):
    lesson = get_object_or_404(Lesson, id=lesson_id)
    return render(request, 'courses/lesson_detail.html', {'lesson': lesson})

@login_required(login_url='login')
def dashboard(request):
    context = {
        'total_courses': Course.objects.count(),
        'total_lessons': Lesson.objects.count(),
        'total_jobs': Job.objects.count(),
        'user_name': request.user.username,
        'user_email': request.user.email,
        'user_profile': getattr(request.user, 'profile', None),  # safe way to get profile
    }
    return render(request, 'core/dashboard.html', context)
