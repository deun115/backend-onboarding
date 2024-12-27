from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.exceptions import PermissionDenied
from rest_framework.renderers import TemplateHTMLRenderer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import Users
from boards.models import Category
from boards.serializers import CategorySerializer


# JWT 쿠키에서 유저 인스턴스 가져오기
def get_user_instance(request):
    try:
        access_token = request.COOKIES.get('access_token')

        # JWT 디코딩
        decoded = AccessToken(access_token)
        user_id = decoded['uuid']
        user_nickname = decoded['nickname']

        if not access_token:
            raise ValueError("Access token not found in cookies.")

        return user_id, user_nickname

    except (KeyError, ValueError, ObjectDoesNotExist) as e:
        # 오류 발생 시 적절한 예외 처리
        raise PermissionDenied("유효하지 않은 사용자입니다.") from e


# 카테고리 리스트 조회 뷰
class CategoryListAPIView(generics.ListCreateAPIView):
    queryset = Category.objects.all().order_by('-depth1')
    serializer_class = CategorySerializer
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['depth1', 'depth2', 'depth3']
    renderer_classes = [TemplateHTMLRenderer]
    template_name = 'category_list.html'

    def get(self, request, *args, **kwargs):
        # Queryset을 가져와서 컨텍스트에 추가
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        print(serializer.data)
        context = {'categories': serializer.data}
        return Response(context, template_name=self.template_name)


# 카테고리 생성 뷰
class CategoryCreateAPIView(generics.GenericAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def post(self, request):
        uuid, nickname = get_user_instance(request)
        print(type(uuid))
        category_data = {
            "user_id": str(uuid),
            "is_opened": request.data.get('is_opened', False),
            "depth1": request.data.get('depth1'),
            "depth2": request.data.get('depth2'),
            "depth3": request.data.get('depth3')
        }
        serializer = CategorySerializer(data=category_data)
        print(serializer)

        if serializer.is_valid():
            category = serializer.save()

        return Response(
            {
                "data": category_data,
                "nickname": nickname
            },
            template_name="category_create.html",
        )
