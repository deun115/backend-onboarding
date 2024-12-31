from rest_framework_simplejwt.tokens import AccessToken

from accounts.models import Users


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        access_token_value = request.COOKIES.get('access_token')
        if access_token_value:
            try:
                access_token = AccessToken(access_token_value)
                user_id = access_token.payload.get('user_id')

                user = Users.objects.filter(id=user_id).first()
                if user:
                    request.user = user
                else:
                    request.user = None

            except Exception as e:
                request.user = None
                raise Exception(f"Token decoding failed: {str(e)}")

        response = self.get_response(request)
        response.headers['Authorization'] = f"Bearer {access_token_value}"
        return response
