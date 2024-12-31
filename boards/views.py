from rest_framework import viewsets
from rest_framework import filters
from rest_framework.filters import SearchFilter
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
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
# TODO: 카테고리의 공개/비공개 상태를 따르기
# TODO: 카테고리 삭제 시 해당 게시글은 '미분류' 카테고리로 이동
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
class BoardSearchViewSet(ListModelMixin, viewsets.GenericViewSet):
    queryset = Board.objects.all().order_by('-created_at')
    # permission_classes = [IsOwnerOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    serializer_class = BoardSerializer


# 댓글 ViewSet
class CommentAPIView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [IsOwnerOrReadOnly]


# TODO: 카테고리별로 게시글 조회 (하위 카테고리의 게시글도 표시)
class CategoryBoardListView(ListModelMixin, GenericViewSet):
    queryset = Board.objects.select_related('category_id').order_by('-created_at')
    pagination_class = PageNumberPagination
    filter_backends = [filters.SearchFilter]

    # Category 모델의 필드를 참조
    search_fields = ['category_id.depth1', 'category_id.depth2', 'category_id.depth3']
    serializer_class = BoardSerializer
