from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .models import User

@csrf_exempt
def register_user(request):
    if request.method == "POST":
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

    return JsonResponse({"error": "Invalid HTTP method."}, status=405)
