import uuid

from django.contrib.auth.hashers import check_password, make_password
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from accounts.models import Users
from accounts.serializers import UserSerializer, MyTokenObtainPairSerializer


# 로그인 뷰
class UserLoginAPIView(APIView):
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
                    "user": UserSerializer(user).data,
                    "message": "로그인 성공",
                    "jwt_token": {
                        "access_token": access_token,
                        "refresh_token": refresh_token
                    },
                },
                status=status.HTTP_200_OK
            )

            response.set_cookie("access_token", access_token, httponly=True)
            response.set_cookie("refresh_token", refresh_token, httponly=True)
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