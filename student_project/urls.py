from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_student_list(request):
    return redirect('student_list')

urlpatterns = [
    path('', redirect_to_student_list, name='home'),  # Add redirect for root URL
    path('admin/', admin.site.urls),
    path('students/', include('student_app.urls')),  # Include your app's URLs
]

