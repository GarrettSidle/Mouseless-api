from django.urls import path
from . import views

urlpatterns = [
    path('problem/', views.problem, name='problem'),
    path('problem-statistics/', views.problem_statistics, name='problem_statistics'),
    path('user-problem-statistics/', views.user_problem_statistics, name='user_problem_statistics'),
]