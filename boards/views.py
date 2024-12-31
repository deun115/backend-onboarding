from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import AccessToken

from boards.models import Category, Board, Comment
from boards.permissions import IsOwnerOrReadOnly
from boards.serializers import CategorySerializer, BoardSerializer, CommentSerializer


# 헤더에서 토큰 가져오기
def get_user_instance(request):
    try:
        access_token = request.headers['Authorization']
        decoded = access_token.split(' ')[1]
        print(decoded)
        user_id = decoded['uuid']
        user_nickname = decoded['nickname']

        if not access_token:
            raise ValueError("Access token not found in cookies.")

        return user_id, user_nickname
    except (KeyError, ValueError, ObjectDoesNotExist) as e:
        # 오류 발생 시 적절한 예외 처리
        raise PermissionDenied("유효하지 않은 사용자입니다.") from e


# 카테고리 관련 ViewSet
class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]


# 게시글 ViewSet
class BoardAPIView(viewsets.ModelViewSet):
    queryset = Board.objects.all().order_by('created_at').order_by('title')
    serializer_class = BoardSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = PageNumberPagination


# class BoardViewSet(viewsets.ViewSet):
#     permission_classes = [IsAuthenticatedOrReadOnly]
#     pagination_class = PageNumberPagination
#
#     def list(self, request):
#         queryset = Board.objects.all()
#         serializer = BoardSerializer(queryset, many=True)
#         return Response(serializer.data)
#
#     def retrieve(self, request, pk=None):
#         queryset = Board.objects.all().order_by('created_at').order_by('title')
#         board = get_object_or_404(queryset, pk=pk)
#         serializer = BoardSerializer(board)
#         return Response(serializer.data)


# 댓글 ViewSet
class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]
