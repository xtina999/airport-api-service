from rest_framework import generics
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


# використовуєм generics щоб створити незалежні класи:
# створення юзера
# обновлення юзера
# щоб дві різні вьюшки

class CreateUserView(generics.CreateAPIView):
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
    serializer_class = AuthTokenSerializer

class ManagerUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    # определяет сис-му аутентификации
    authentication_classes = (TokenAuthentication, )

    # щоб до цієї кінцевої сторінки мали тільки ті
    # хто прописані в permission_classes
    permission_classes = (IsAuthenticated, )

    # щоб інформація була від користувача який залогінився
    def get_object(self):
        return self.request.user

