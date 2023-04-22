from http import HTTPStatus

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import (LimitOffsetPagination,
                                       PageNumberPagination)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from reviews.models import Category, Genre, Title, User

from .filter import TitleFilter
from .mixins import ListCreateDeleteViewSet
from .permissions import IsAdmin, IsAdminOrReadOnly
from .serializers import (AdminSerializer, CategorySerializer, GenreSerializer,
                          RegistrationSerializer, TitleReadSerializer,
                          TitleWriteSerializer, TokenConfirmationSerializer,
                          UserSerializer)


class UserCreation(APIView):
    """Вьюсет создания юзера и отправки сообщения на почту"""
    @staticmethod
    def send_participation_code(user_data):
        message = EmailMessage(
            subject=user_data['subject'],
            body=user_data['message'],
            from_email=settings.EMAIL_HOST_USER,
            to=[user_data['to_email']],
        )
        message.send()

    @staticmethod
    def token_generator(signed_user):
        return default_token_generator.make_token(signed_user)

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        signed_user, created = User.objects.get_or_create(
            username=data.get('username'),
            email=data.get('email')
        )
        signed_user.confirmation_code = self.token_generator(signed_user)
        user_data = {
            'subject': f'Код подтверждения для {signed_user.username}',
            'message': signed_user.confirmation_code,
            'to_email': signed_user.email
        }
        self.send_participation_code(user_data)
        return Response(serializer.data, status=HTTPStatus.OK)


class JWTTokenConfirmation(APIView):
    """Создание JWT токена через код пользователя"""
    def post(self, request):
        serializer = TokenConfirmationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_data = serializer.validated_data
        current_user = get_object_or_404(
            User, username=user_data.get('username'),
        )
        if user_data['confirmation_code'] == current_user.confirmation_code:
            refreshed_token = RefreshToken.for_user(current_user)
            return Response({
                'JWT-Код': str(refreshed_token.access_token),
            }, status=HTTPStatus.CREATED)
        return Response(
            'Неверный код-подтверждение!',
            status=HTTPStatus.BAD_REQUEST
        )


class UserViewSet(viewsets.ModelViewSet):
    """Вьюсет Users."""
    queryset = User.objects.all()
    serializer_class = AdminSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('username',)
    lookup_field = 'username'
    http_method_names = ('patch', 'post', 'get', 'delete',)
    permission_classes = (IsAuthenticated, IsAdmin)
    pagination_class = LimitOffsetPagination

    @action(detail=False, url_path='me', methods=['GET', 'PATCH'],
            permission_classes=(IsAuthenticated,))
    def get_or_patch_self_profile(self, request):
        """Пользователь может изменить и получить данные о себе."""
        user = get_object_or_404(User, id=request.user.id)
        if request.method == 'GET':
            serializer = UserSerializer(user, many=False)
            return Response(serializer.data)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=HTTPStatus.OK)
        return Response(serializer.errors, status=HTTPStatus.BAD_REQUEST)


class CategoryViewSet(ListCreateDeleteViewSet):
    queryset = Category.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def delete(self, request, pk, format=None):
        category = self.model.objects.get(category_id=pk, user=request.user)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class GenreViewSet(ListCreateDeleteViewSet):
    queryset = Genre.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'

    def delete(self, request, pk, format=None):
        genre = self.model.objects.get(genre_id=pk, user=request.user)
        genre.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = (IsAdminOrReadOnly,)
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ['POST', 'PATCH']:
            return TitleWriteSerializer
        return TitleReadSerializer
