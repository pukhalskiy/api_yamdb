from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet,
                    CommentsViewSet, GenresViewSet, ReviewViewSet,
                    TitlesViewSet, UserCreateViewSet,
                    UserReceiveTokenViewSet,
                    UserViewSet)


router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'categories', CategoryViewSet, basename="categories")
router.register(r'genres', GenresViewSet, basename="genres")
router.register(
    'titles/(?P<title_id>\\d+)/reviews/(?P<review_id>\\d+)/comments',
    CommentsViewSet,
    basename="comments")
router.register('titles', TitlesViewSet, basename="titles")
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename="reviews")
router.register(r'^titles/(?P<title_id>\d+)/', TitlesViewSet,
                basename='title')
urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/auth/signup/', UserCreateViewSet.as_view({'post': 'create'}),
         name='signup'),
    path('v1/auth/token/', UserReceiveTokenViewSet.as_view({'post': 'create'}),
         name='token')
]
