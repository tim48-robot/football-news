from django.shortcuts import render
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect, JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json


@csrf_exempt
def login(request):
    print("\n" + "="*50)
    print("LOGIN REQUEST RECEIVED")
    print("="*50)
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            username = data.get('username')
            password = data.get('password')
            print(f"✅ JSON Parsed - Username: '{username}'")
        except json.JSONDecodeError:
            # Handle form data properly
            username = request.POST.get('username')
            password = request.POST.get('password')
            print(f"Using POST data - Username: '{username}', Password: {'*' * len(password) if password else 'None'}")
        
        print(f"Attempting to authenticate user: '{username}'")
        print(f"Password received: {'Yes' if password else 'No'}")
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            print(f"✅ User authenticated: {user.username}")
            if user.is_active:
                auth_login(request, user)
                print(f"✅ User logged in successfully")
                return JsonResponse({
                    "username": user.username,
                    "status": "success",
                    "message": "Login successful!"
                }, status=200)
            else:
                print(f"❌ User is not active")
                return JsonResponse({
                    "status": "failed",
                    "message": "Login failed, account is disabled."
                }, status=401)
        else:
            print(f"❌ Authentication failed for username: '{username}'")
            return JsonResponse({
                "status": "failed",
                "message": "Login failed, please check your username or password."
            }, status=401)
    
    return JsonResponse({
        "status": "failed",
        "message": "Invalid request method."
    }, status=400)

@csrf_exempt
def register(request):
    print("\n" + "="*50)
    print("REGISTER REQUEST RECEIVED")
    print("="*50)
    print(f"Method: {request.method}")
    print(f"Content-Type: {request.content_type}")
    print(f"Raw Body: {request.body}")
    print(f"POST Data: {request.POST}")
    print("="*50 + "\n")
    
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            print(f"✅ JSON Parsed Successfully: {data}")
            username = data.get('username')
            password1 = data.get('password1')
            password2 = data.get('password2')
        except json.JSONDecodeError as e:
            print(f"❌ JSON Decode Error: {e}")
            username = request.POST.get('username')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')
            print(f"Using POST data instead: {username}, {password1}, {password2}")

        print(f"Username: '{username}'")
        print(f"Password1: '{password1}'")
        print(f"Password2: '{password2}'")

        # Validation
        if not username or not password1 or not password2:
            print("❌ VALIDATION FAILED: Missing fields")
            return JsonResponse({
                "status": "failed",
                "message": "All fields are required."
            }, status=400)

        if password1 != password2:
            print("❌ VALIDATION FAILED: Passwords don't match")
            return JsonResponse({
                "status": "failed",
                "message": "Passwords do not match."
            }, status=400)
        
        if User.objects.filter(username=username).exists():
            print("❌ VALIDATION FAILED: Username exists")
            return JsonResponse({
                "status": "failed",
                "message": "Username already exists."
            }, status=400)
        
        try:
            user = User.objects.create_user(username=username, password=password1)
            user.save()
            print(f"✅ USER CREATED: {user.username}")
            
            return JsonResponse({
                "username": user.username,
                "status": "success",
                "message": "User created successfully!"
            }, status=200)
        except Exception as e:
            print(f"❌ ERROR CREATING USER: {str(e)}")
            return JsonResponse({
                "status": "failed",
                "message": f"Error: {str(e)}"
            }, status=400)
    
    else:
        return JsonResponse({
            "status": "failed",
            "message": "Invalid request method."
        }, status=400)


@csrf_exempt
def logout(request):
    username = request.user.username
    try:
        auth_logout(request)
        return JsonResponse({
            "username": username,
            "status": True,
            "message": "Logged out successfully!"
        }, status=200)
    except:
        return JsonResponse({
            "status": False,
            "message": "Logout failed."
        }, status=401)