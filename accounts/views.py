import uuid

from django.contrib.auth.hashers import check_password, make_password
from django.shortcuts import redirect
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenBlacklistView

from accounts.models import Users
from accounts.serializers import UserSerializer, MyTokenObtainPairSerializer


# 로그인 뷰
class UserLoginAPIView(APIView):
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'account_login.html'

    def get(self, request):
        # 로그인 페이지 렌더링
        return Response(template_name=self.template_name)

    def post(self, request):
        nickname = request.data.get('nickname')
        password = request.data.get('password')

        user = Users.objects.filter(nickname=nickname).first()

        if not user:
            return Response(
                {"message": "존재하지 않는 아이디입니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if not check_password(password, user.password):
            return Response(
                {"message": "비밀번호가 틀렸습니다."}, status=status.HTTP_400_BAD_REQUEST
            )

        if user is not None:
            token = MyTokenObtainPairSerializer.get_token(user)  # refresh 토큰 생성
            refresh_token = str(token)  # refresh 토큰 문자열화
            access_token = str(token.access_token)  # access 토큰 문자열화
            response = Response(
                {
                    "message": "로그인 성공",
                    "user": UserSerializer(user).data
                },
                template_name="category_list.html",  # 템플릿 렌더링
                status=status.HTTP_200_OK
            )

            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
            response.headers['Authorization'] = f"Bearer {access_token}"
            response.headers['Refresh-Token'] = refresh_token

            return response
        else:
            return Response(
                {"message": "로그인에 실패하였습니다."},
                status=status.HTTP_400_BAD_REQUEST
            )


# 회원가입 뷰
class RegisterAPIView(APIView):

    def post(self, request):
        nickname = request.data.get('nickname')

        # 닉네임 중복 확인
        if Users.objects.filter(nickname=nickname).exists():
            return Response(
                {"message": "이미 존재하는 닉네임입니다."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # 비밀번호 해싱
        raw_password = request.data.get('password')
        hashed_password = make_password(raw_password)

        # 사용자 데이터 생성
        user_uuid = uuid.uuid4()
        user_data = {
            "uuid": user_uuid,
            "nickname": nickname,
            "password": hashed_password,  # 해싱된 비밀번호 저장
        }
        serializer = UserSerializer(data=user_data)

        if serializer.is_valid():
            user = serializer.save()

            # JWT 토큰 생성
            token = MyTokenObtainPairSerializer.get_token(user)
            refresh_token = str(token)
            access_token = str(token.access_token)
            res = Response(
                {
                    "user": {
                        "uuid": user.uuid,
                        "nickname": user.nickname,
                    },
                    "message": "회원가입 성공",
                    "token": {
                        "access": access_token,
                        "refresh": refresh_token,
                    },
                },
                status=status.HTTP_201_CREATED
            )
            res.set_cookie("access", access_token, httponly=True)
            res.set_cookie("refresh", refresh_token, httponly=True)
            return res

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLogoutAPIView(TokenBlacklistView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def post(self, request, *args, **kwargs):
        # Refresh 토큰 가져오기
        refresh_token = request.COOKIES.get("refresh")
        if not refresh_token:
            return Response(
                {"message": "토큰이 존재하지 않습니다."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 토큰 블랙리스트 처리
        data = {"refresh": str(refresh_token)}
        serializer = self.get_serializer(data=data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        # 응답 설정
        response = Response(
            {"message": "로그아웃 성공"},
            status=status.HTTP_200_OK,
        )
        response.delete_cookie("refresh")
        response.delete_cookie("access")

        return response
