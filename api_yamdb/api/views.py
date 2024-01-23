from django.contrib.auth.tokens import default_token_generator
from django.db.models import Avg
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from rest_framework import filters, mixins, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

import api.permissions
import api.serializers
from reviews.models import Category, Genres, Review, Title
from users.models import User

from .filters import FilterTitle
from .utils import send_confirmation_code
from .permissions import IsSuperUserOrIsAdminOnly
from .serializers import (UserCreateSerializer, UserSerializer,
                          UserRecieveTokenSerializer)


class CreateListDestroy(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    """Mixin for create, destroy, get and delete models."""


class UserCreateViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user, _ = User.objects.get_or_create(**serializer.validated_data)
        confiramion_code = default_token_generator.make_token(user)
        send_confirmation_code(
            email=user.email,
            confirmation_code=confiramion_code
        )
        return Response(serializer.data, status=status.HTTP_200_OK)


class UserReceiveTokenViewSet(viewsets.GenericViewSet):
    queryset = User.objects.all()
    serializer_class = api.serializers.UserRecieveTokenSerializer
    permission_classes = (permissions.AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = UserRecieveTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data.get('username')
        confirmation_code = serializer.validated_data.get('confirmation_code')
        user = get_object_or_404(User, username=username)

        if not default_token_generator.check_token(user, confirmation_code):
            return Response('Код подтверждения невалиден',
                            status=status.HTTP_400_BAD_REQUEST)
        return Response(str(AccessToken.for_user(user)),
                        status=status.HTTP_200_OK)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,
                          IsSuperUserOrIsAdminOnly)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('=username',)
    lookup_field = 'username'
    http_method_names = ('get', 'post', 'patch', 'delete')

    @action(
        detail=False,
        methods=['get', 'patch'],
        permission_classes=(permissions.IsAuthenticated,
                            IsSuperUserOrIsAdminOnly,)
    )
    def get_user_by_username(self, request, username):
        user = get_object_or_404(User, username=username)
        if request.method == 'PATCH':
            serializer = UserSerializer(user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(
        detail=False,
        methods=['get', 'patch'],
        url_path='me',
        url_name='me',
        permission_classes=(permissions.IsAuthenticated,)
    )
    def get_me_data(self, request):
        if request.method == 'PATCH':
            serializer = UserSerializer(
                request.user, data=request.data,
                partial=True, context={'request': request}
            )
            serializer.is_valid(raise_exception=True)
            serializer.save(role=request.user.role)
            return Response(serializer.data, status=status.HTTP_200_OK)
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(CreateListDestroy):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          api.permissions.AdminOrReadOnly]
    serializer_class = api.serializers.CategorySerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class GenresViewSet(CreateListDestroy):
    queryset = Genres.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          api.permissions.AdminOrReadOnly]
    serializer_class = api.serializers.GenresSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ('name', 'slug')
    lookup_field = 'slug'


class TitlesViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          api.permissions.AdminOrReadOnly]
    serializer_class = api.serializers.TitleGetSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    filterset_class = FilterTitle
    search_fields = ('name', 'year', 'genre__slug', 'category__slug')

    def get_rating(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.aggregate(Avg('score'))['score__avg']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return api.serializers.TitleGetSerializer
        return api.serializers.TitlePostSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        api.permissions.IsSuperUserIsAdminIsModeratorIsAuthor)
    serializer_class = api.serializers.ReviewSerializer

    def get_title(self):
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, id=title_id)

    def get_queryset(self):
        title = self.get_title()
        return title.reviews.all()

    def perform_create(self, serializer):
        title = self.get_title()
        serializer.save(title=title,
                        author=get_object_or_404(User, id=self.request.user.id)
                        )


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = api.serializers.CommentsSerializer
    permission_classes = (
        permissions.IsAuthenticatedOrReadOnly,
        api.permissions.IsSuperUserIsAdminIsModeratorIsAuthor)

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        serializer.save(review=review, author=self.request.user)
