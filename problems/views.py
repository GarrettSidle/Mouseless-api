from django.shortcuts import render
from django.http import JsonResponse
from .models import Problem
from django.http import JsonResponse, HttpRequest 
import json
from auth_app.models import Session
from .models import StatisticType
from .models import Problem_Statistics


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
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
    
    session_key = request.POST.get('session_key')
    problem_number = request.POST.get('problem_number')
    
    problem_time = request.POST.get('problem_time')
    problem_strokes = request.POST.get('problem_strokes')
    problem_speed = request.POST.get('problem_speed')
    
    isAuthorized = Session.check_session_key(session_key)
    
    problem: Problem = Problem.get_problem(problem_number)
    
    stat = Problem_Statistics.update_stat(problem, StatisticType.Time, )
    
    stat.save()
    
        
    
        
        
    
    