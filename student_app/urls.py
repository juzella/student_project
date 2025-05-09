from django.urls import path
from .views import student_list, student_create, student_update, student_delete, register_student
from . import views

urlpatterns = [
    path('', student_list, name='student_list'),
    path('new/', student_create, name='student_create'),
    path('register/', register_student, name='register_student'),  # New registration URL
    path('<int:pk>/edit/', student_update, name='student_update'),
    path('<int:pk>/delete/', student_delete, name='student_delete'),
    path('train-model/', views.train_model, name='train_model'),
    path('predict-course/', views.predict_course, name='predict_course'),
    path('model-status/', views.get_model_status, name='model_status'),
]
