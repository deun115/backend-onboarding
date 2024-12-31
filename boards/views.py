from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.exceptions import PermissionDenied
from rest_framework.filters import SearchFilter
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from boards.models import Category, Board, Comment
from boards.permissions import IsOwnerOrReadOnly, IsOwner
from boards.serializers import CategorySerializer, BoardSerializer, CommentSerializer


# 카테고리 관련 ViewSet
# TODO: 카테고리의 공개/비공개 상태에 따라 permission 다르게 지정
class CategoryAPIView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsOwnerOrReadOnly]


# 게시글 ViewSet
# TODO: 자신이 작성한 게시글만 수정/삭제하기
# TODO: 카테고리의 공개/비공개 상태를 따르되, 개별 게시글 설정으로 덮어쓰기 기능
# TODO: 카테고리 이동
# TODO: 카테고리 삭제 시 해당 게시글은 '미분류' 카테고리로 이동
# TODO: 카테고리별로 게시글 조회 (하위 카테고리의 게시글도 표시)
class BoardAPIView(viewsets.ModelViewSet):
    queryset = Board.objects.all().order_by('-created_at').order_by('title')
    serializer_class = BoardSerializer
    authentication_classes = [JWTAuthentication]
    # permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination

    # def create(self, request, *args, **kwargs):
    #
    #     return super().create(request, *args, **kwargs)
    def perform_create(self, serializer):
        serializer.save(user_id=self.request.user)


# 게시글 검색 ViewSet
# TODO: 제목 및 내용 검색 기능
class BoardSearchViewSet(viewsets.ViewSet):
    queryset = Board.objects.all().order_by('-created_at')
    # permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [SearchFilter]
    search_fields = ['title', 'content']

    def list(self, request):
        serializer = BoardSerializer(self.queryset, many=True)
        return serializer.data


# 댓글 ViewSet
class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsOwnerOrReadOnly]
