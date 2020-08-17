from django.urls import path
from . import views

urlpatterns = [
        path('', views.register, name='register'),
        path('top_up/', views.top_up, name='top_up'),
        path('students/', views.student_list, name='student_list'),
        path('students/<slug:id>', views.student_info, name='student_info'),
        path('analysis/', views.analysis, name='analysis'),
]
