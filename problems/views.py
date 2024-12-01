from django.shortcuts import render
from django.http import JsonResponse
from .models import Problem


def problem(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    return JsonResponse({
        'message': 'Login successful',
        'session_key': Problem.get_random_problem() 
        }, status=200)
def problem_statistics(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
def user_problem_statistics(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)