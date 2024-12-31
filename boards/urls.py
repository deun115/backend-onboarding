from django.urls import path
from boards.views import CategoryAPIView, CommentAPIView, BoardAPIView

board_api = BoardAPIView.as_view(
    {
        "get": "list",
        "post": "create",
        "delete": "destroy",
        "put": "update",
    }
)

# board_search_api = BoardAPIView.as_view(
#     {
#         "get": "retrieve"
#     }
# )

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
    path('', board_api),
    # path('search/<>', board_search_api),
    path('category/', category_list_api),
    path('comment/', comment_api),
]
