from django.shortcuts import render
from django.http import JsonResponse


def problem(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
def problem_statistics(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
def user_problem_statistics(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)