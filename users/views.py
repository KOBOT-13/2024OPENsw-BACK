from django.contrib.sites import requests
from django.http import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmationHMAC


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'email': user.email,
            'username': user.username,
            'is_staff': user.is_staff
        })


class CustomConfirmEmailView(ConfirmEmailView):
    template_name = 'account/email/success_verify_email.html'
    
    def get_template_names(self) -> list[str]:
        return super().get_template_names()
    
    def dispatch(self, request, *args, **kwargs):
        key = kwargs.get('key', None)
        print(f'dispatch called with key: {key}')
        if key:
            email_confirmation = EmailConfirmationHMAC.from_key(key)
            if email_confirmation:
                email_address = email_confirmation.email_address
                print(f'EmailConfirmation found: {email_confirmation}') 
                
                # 여기서 이메일 인증을 완료
                email_confirmation.confirm(request)
                
                # 다시 한 번 확인
                email_address.refresh_from_db()
                
                if email_address and email_address.verified:
                    user = email_address.user
                    user.is_verified = True
                    user.save()
                    print(f'User {user.email} verified and saved')
                else:
                    print(f'EmailAddress not verified or not found: {email_address.email if email_address else "None"}')
            else:
                print(f'EmailConfirmation not found for key: {key}')
        
        return super().dispatch(request, *args, **kwargs)

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