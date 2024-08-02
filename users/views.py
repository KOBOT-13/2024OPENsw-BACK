from django.contrib.sites import requests
from django.http import JsonResponse
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmationHMAC
from allauth.account.models import EmailAddress
from rest_framework import status, mixins
from dj_rest_auth.views import LoginView
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

from users.adapter import CustomAccountAdapter
from rest_framework import generics

from .models import CustomUser
from .serializers import CustomUserSerializer, ProfileUpdateSerializer
from allauth.account.utils import send_email_confirmation
from django.contrib.auth import authenticate, login, get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    serializer_class = CustomUserSerializer

    def perform_create(self, serializer):
        user = serializer.save()  # 사용자를 저장합니다.

        # 이메일 주소를 가져옵니다.
        email_address = EmailAddress.objects.create(user=user, email=user.email, primary=True, verified=False)
        
        # 이메일 인증 링크를 보내는 함수 호출
        self.send_email_confirmation(user, email_address)

    def send_email_confirmation(self, user, email_address):
        request = self.request  # 현재 요청 객체를 사용합니다.

        # 이메일 인증 메일 전송
        send_email_confirmation(request, user)

class CheckUsernameView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        if User.objects.filter(username=username).exists():
            return Response({"detail": "이미 존재하는 닉네임입니다."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "사용 가능한 닉네임입니다."}, status=status.HTTP_200_OK)

class CheckEmailView(APIView):
    def post(self, request, *args, **kwargs):
        email = request.data.get('email')
        if User.objects.filter(email=email).exists():
            return Response({"detail": "이미 존재하는 이메일 주소입니다."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "사용 가능한 이메일 주소입니다."}, status=status.HTTP_200_OK)

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

'''class CustomLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        print('custom login view call')

        # 요청에서 email과 password 가져오기
        email = request.data.get('email')  # 이메일 필드
        password = request.data.get('password')  # 비밀번호 필드
        print(email)
        print(password)

        # 이메일로 사용자 인증
        user = authenticate(request, username=email, password=password)

        if user is not None:
            # 이메일 주소로 사용자 가져오기
            email_address = EmailAddress.objects.filter(email=email, primary=True).first()
            if email_address and not email_address.verified:
                
                # 이메일 주소가 인증되지 않은 경우
                adapter = CustomAccountAdapter()
                adapter.send_email_confirmation(request, user)  # 인증 이메일 재전송
                return Response(
                    {"detail": "이메일 인증이 필요합니다. 인증 이메일이 재전송되었습니다."},
                    status=status.HTTP_401_UNAUTHORIZED
                )

            # 이메일 인증이 완료된 경우 로그인
            login(request, user)
            return super().post(request, *args, **kwargs)
        else:
            # 로그인 실패 시 처리
            if not EmailAddress.objects.filter(email=email).exists():
                return Response(
                    {"detail": "등록된 이메일 주소가 아닙니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )

            user = User.objects.filter(email=email).first()
            if user and not user.check_password(password):
                return Response(
                    {"detail": "비밀번호가 잘못되었습니다."},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            return Response(
                {"detail": "이메일 주소 또는 비밀번호가 잘못되었습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )'''

class CustomLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({"detail": "로그아웃 성공"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"detail": f"로그아웃 실패: {str(e)}"}, status=status.HTTP_400_BAD_REQUEST)

class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        return Response({
            'id' : user.id,
            'email': user.email,
            'username': user.username,
            'is_staff': user.is_staff
        })

class ProfileUpdateView(generics.GenericAPIView, mixins.UpdateModelMixin):
    queryset = CustomUser.objects.all()
    serializer_class = ProfileUpdateSerializer
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        return self.request.user

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

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