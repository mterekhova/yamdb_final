from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import GenericViewSet

from reviews.models import Category, Genre, Review, Title
from .filters import TitleFilter
from .permissions import AdminOrReadOnly, OwnerOrReadOnly
from .serializers import (CategorySerializer, CommentSerializer,
                          GenreSerializer, ReviewSerializer,
                          TitleCreateSerializer, TitleSerializer)


class CreateListDestroyViewSet(
    CreateModelMixin, ListModelMixin,
        GenericViewSet, DestroyModelMixin):
    """
    CreateListDestroyViewSet не предоставляет никакой особенной
    функциональность предназначен исключительно для наследования
    общей фукцуиональности от объединения нескольких mixin-ов
    """
    pass


class GenreViewSet(CreateListDestroyViewSet):
    """Получить список всех жанров."""

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOrReadOnly)
    lookup_field = 'slug'
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)


class TitleViewSet(viewsets.ModelViewSet):
    """Получить список всех произведений."""

    queryset = Title.objects.annotate(rating=Avg('reviews__score')).all()
    serializer_class = TitleSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOrReadOnly)

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH',):
            return TitleCreateSerializer
        return TitleSerializer


class CategoryViewSet(CreateListDestroyViewSet):
    """Получить список всех категорий."""

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAuthenticatedOrReadOnly, AdminOrReadOnly)
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)
    search_fields = ('name',)
    lookup_field = 'slug'


class ReviewViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Возвращает отзыв на выбранное произведение.

    list:
    Возвращает список отзывов всех отзывов на выбранное произведение.

    create:
    Создает отзыв.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerOrReadOnly]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        reviews = title.reviews.all()
        return reviews

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    """
    retrieve:
    Возвращает комментарий на выбранный отзыв.

    list:
    Возвращает список всех комментариев на выбранный отзывов.

    create:
    Создает комментарий.
    """
    permission_classes = [IsAuthenticatedOrReadOnly, OwnerOrReadOnly]
    serializer_class = CommentSerializer

    def get_queryset(self):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        comments = review.comments.all()
        return comments

    def perform_create(self, serializer):
        review = get_object_or_404(Review, id=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
