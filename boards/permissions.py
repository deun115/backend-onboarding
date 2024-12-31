import pprint

from rest_framework import permissions
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from rest_framework_simplejwt.tokens import AccessToken


class IsOwner(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user:
            if obj.id == request.user.id:
                return True
            raise PermissionDenied()
        raise NotAuthenticated()


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    게시글 작성자만 수정/삭제 권한이 있으며,
    읽기 요청은 모두 허용됩니다.
    """
    def has_object_permission(self, request, view, obj):
        print(request.META.get('HTTP_AUTHORIZATION'))

        # 읽기 권한은 모두 허용
        if request.method in permissions.SAFE_METHODS:
            return True

        # 작성자만 수정/삭제 가능
        return obj.user_id == request.user
