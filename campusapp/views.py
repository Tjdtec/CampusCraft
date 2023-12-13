from django.http import JsonResponse

from django.http import HttpResponse
from django.conf import settings
import os
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
import json
from .models import Login
from django.http import JsonResponse

def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        try:
            login_record = Login.objects.get(user_name=username, user_password=password)
            response_data = {
                'username': login_record.user_name,
                'password': login_record.user_password,
                'user_type': login_record.get_user_type_display()
            }
            return JsonResponse(response_data)
        except Login.DoesNotExist:
            return JsonResponse({'error': 'Invalid username or password'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405) 