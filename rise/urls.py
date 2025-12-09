from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),

    # ---------- Public Pages ----------
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),

    # ---------- Authentication ----------
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    # ---------- Dashboard ----------
    path('dashboard/', views.dashboard, name='dashboard'),

    # ---------- Booking ----------
    path('booking/', views.booking_list, name='booking_list'),
    path('booking/<int:slot_id>/', views.book_slot, name='book_slot'),
    path('booking/success/', views.booking_success, name='booking_success'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),
    path('booking/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    # ---------- Courses ----------
    path('courses/', views.course_list, name='course_list'),
    path('courses/<int:course_id>/', views.course_detail, name='course_detail'),
    path('lessons/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),

    # ---------- Jobs ----------
    path('jobs/', views.job_list, name='job_list'),
    path('jobs/<int:job_id>/apply/', views.apply_job, name='apply_job'),
    path('jobs/<int:job_id>/applicants/', views.job_applicants, name='job_applicants'),
    path('application-success/', TemplateView.as_view(
        template_name='application_success.html'
    ), name='application_success'),

    # ---------- Challenges ----------
    # path('challenges/', views.challenge_list, name='challenge_list'),
    # path('challenges/<int:challenge_id>/', views.challenge_detail, name='challenge_detail'),

    # ---------- Donate & Mpesa ----------
    path('donate/', views.donate, name='donate'),
    path('donate/success/', views.donate_success, name='donate_success'),
    path('mpesa/stk/', views.stk_push, name='stk_push'),
    path('mpesa/callback/', views.mpesa_callback, name='mpesa_callback'),
    
    path('profile/', views.profile_view, name='profile'),
]

# ---------- Media Files (development only) ----------
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
