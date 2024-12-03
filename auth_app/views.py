from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
from .models import Session
from django.http import JsonResponse, HttpRequest  
import json

@csrf_exempt
def register_user(request : HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
    username = request.POST.get('username')
    password = request.POST.get('password')
    
    # Check if user already exists
    if User.objects.filter(username=username).exists():
        return JsonResponse({"error": "Username already exists."}, status=400)
    
    # Create and save the new user
    user = User(username=username)
    user.set_password(password)
    user.save()

    print(user.id)
    return JsonResponse({"message": "User created successfully."}, status=201)

@csrf_exempt
def login_user(request : HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    username = request.POST.get('username')
    password = request.POST.get('password')

    user = User.authenticate(request, username, password)
    if not user:
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    session = Session.create_session_key(request, user)

    
    return JsonResponse({
        'message': 'Login successful',
        'session_key': session.session_key  
        }, status=200)

    
@csrf_exempt
def verify_session(request : HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    raw_session_key = request.POST.get('session_id')
    print(raw_session_key)
    if(Session.check_session_key(raw_session_key)):
        return JsonResponse({'message': 'Session is Verified', }, status=200)
    return JsonResponse({'message': 'Session is NOT Verified', }, status=401)
    
    
@csrf_exempt
def logout(request : HttpRequest):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    
    try:
        print(request.POST.get('session_id'))
        session = Session.objects.get(session_key=request.POST.get('session_id'))
    except Session.DoesNotExist:
        return JsonResponse({'message': 'Unable to find session', }, status=404)
    
    session.delete_session_key()
    return JsonResponse({'message': 'Session is ended', }, status=200)