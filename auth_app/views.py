from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User
from .models import Session

@csrf_exempt
def register_user(request):
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
def login_user(request):
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
def verify_session(request):
    if request.method != "GET":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)
    raw_session_key = request.GET.get('session_id')
    if(Session.check_session_key(request, raw_session_key)):
        return JsonResponse({'message': 'Session is Verified', }, status=200)
    return JsonResponse({'message': 'Session is NOT Verified', }, status=401)
    
    
    
def logout(request):
    if request.method != "POST":
        return JsonResponse({"error": "Invalid HTTP method."}, status=405)