from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'username': user.username,
            'is_staff': user.is_staff
        })



#카카오톡 로그인 뷰
"""from django.shortcuts import render

def kakao_login_view(request):
    return render(request, 'kakao_login.html')

def kakao_user_info(request):
    access_token = request.headers.get('Authorization').split(' ')[1]
    headers = {
        "Authorization": f"Bearer {access_token}",
    }
    response = requests.get("https://kapi.kakao.com/v2/user/me", headers=headers)
    if response.status_code == 200:
        return JsonResponse(response.json())
    return JsonResponse({'error': 'Failed to retrieve user info'}, status=response.status_code)"""