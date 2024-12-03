from django.shortcuts import render
from django.http import JsonResponse
from .models import Problem
from django.http import JsonResponse, HttpRequest 
import json


def problem(request : HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    problem = Problem.get_random_problem() 
    return JsonResponse({
        'message': 'Login successful',
        'problem': {
            'problemNo' : problem.number,
            'original-text': problem.original_code_block,
           'modified-text' : problem.modified_code_block
        }
        }, status=200)
    
    
def problem_statistics(request : HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
    
def user_problem_statistics(request : HttpRequest):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)