from django.urls import path
from boards.views import CategoryAPIView, CommentAPIView, BoardAPIView, BoardSearchViewSet

board_list_api = BoardAPIView.as_view(
    {
        "get": "list",
        "post": "create",
    }
)

board_detail_api = BoardAPIView.as_view(
    {
        "get": "retrieve",
        "put": "update",
        "delete": "destroy",
    }
)

board_search_api = BoardSearchViewSet.as_view(
    {
        "get": "list"
    }
)

category_list_api = CategoryAPIView.as_view(
    {
        "get": "list",
        "post": "create",
        "delete": "destroy",
    }
)

comment_api = CommentAPIView.as_view(
    {
        "get": "list",
        "post": "create",
        "delete": "destroy",
    }
)

urlpatterns = [
    path('', board_list_api, name='board_list_api'),
    path('<int:pk>/', board_detail_api),
    path('search/', board_search_api),
    path('category/', category_list_api),
    path('comment/', comment_api),
]
