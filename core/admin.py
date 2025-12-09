from django.contrib import admin
from django.utils.html import format_html
from .models import Course, Lesson, UserProfile, UserProgress, Job, JobApplication, ContactMessage, Booking, Slot

# ---------------- COURSES ----------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')
    search_fields = ('title',)

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'course')
    search_fields = ('title', 'course__title')
    list_filter = ('course',)

@admin.register(UserProgress)
class UserProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'lesson', 'completed', 'completed_at')
    list_filter = ('completed',)
    search_fields = ('user__username', 'lesson__title')

# ---------------- JOBS ----------------
@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ('title', 'location', 'posted_at')
    search_fields = ('title', 'location')
    list_filter = ('location',)

@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('user', 'job', 'applied_at', 'resume_link')
    list_filter = ('job', 'applied_at')
    search_fields = ('user__username', 'job__title')

    def resume_link(self, obj):
        if obj.resume:
            return format_html('<a href="{}" target="_blank">View Resume</a>', obj.resume.url)
        return "No Resume"
    resume_link.short_description = "Resume"

# ---------------- CONTACT ----------------
@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'email', 'subject', 'message')

# ---------------- BOOKING ----------------
from django.contrib import admin
from .models import Slot, Booking

@admin.register(Slot)
class SlotAdmin(admin.ModelAdmin):
    list_display = ('title', 'slot_type', 'button_text')
    search_fields = ('title', 'description')

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'slot', 'notes', 'created_at')
    list_filter = ('created_at', 'slot')
    search_fields = ('user__username', 'slot__title', 'notes')



# ---------------- USER PROFILE ----------------
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'location')
    search_fields = ('user__username', 'phone', 'location')

admin.site.register(UserProfile, UserProfileAdmin)


from django.contrib.auth.models import User
# Default User admin
admin.site.unregister(User)
admin.site.register(User)

# core/admin.py
from django.contrib import admin
from django.contrib.auth.models import User
from .models import UserProfile

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(admin.ModelAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')

# Unregister default User
admin.site.unregister(User)
# Register User with profile inline
admin.site.register(User, CustomUserAdmin)
