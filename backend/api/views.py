from django.db.models import Exists, OuterRef, Sum
from django.http import FileResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend

from rest_framework import permissions, viewsets, status
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.response import Response

from djoser.views import UserViewSet

from users.models import Subscribe

from recipes.models import (
    Tag,
    Ingredient,
    Recipes,
    ShoppingCart,
    Favorites,
    IngredientInRecipe
)
from recipes import pdf_shopping_cart

from api.permissions import IsAuthorOrAdminOrReadOnly
from api.filters import RecipeFilter
from api.serializers import (
    TagSerializer,
    IngredientSerializer,
    RecipeListRetrieveSerializer,
    RecipeCreateSerializer,
    FavoriteSerializer,
    RecipeMinifiedSerializer,
    ShoppingCartSerializer,
    SubscribeSerializer,
    CustomUserSubscribeSerializer,
)


class CustomUserViewSet(UserViewSet):
    @action(detail=False, methods=['get'],
            permission_classes=(permissions.IsAuthenticated,))
    def subscriptions(self, request):
        subscribtions = self.queryset.filter(
            subscription__user=self.request.user
        )
        page = self.paginate_queryset(subscribtions)
        serializer = CustomUserSubscribeSerializer(
            page, many=True, context={'request': request}
        )
        return self.get_paginated_response(serializer.data)

    @action(detail=True, methods=['post'],
            permission_classes=(permissions.IsAuthenticated,))
    def subscribe(self, request, id=None):
        author = get_object_or_404(self.get_queryset(), id=id)
        serializer = SubscribeSerializer(
            context={
                'request': request,
                'author': author
            },
            data=request.data
        )
        serializer.is_valid(raise_exception=True)
        serializer.save(
            user=self.request.user,
            author=author
        )
        response = CustomUserSubscribeSerializer(
            author, context={'request': request}
        )
        return Response(
            response.data, status=status.HTTP_201_CREATED)

    @subscribe.mapping.delete
    def unsubscribe(self, request, id=None):
        author = get_object_or_404(self.get_queryset(), id=id)
        get_object_or_404(
            Subscribe, author=author, user=self.request.user
        ).delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (permissions.AllowAny,)
    pagination_class = None


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (permissions.AllowAny,)
    filter_backends = (SearchFilter,)
    search_fields = ('^name',)
    pagination_class = None


class RecipeViewSet(viewsets.ModelViewSet):
    permission_classes = (IsAuthorOrAdminOrReadOnly,)
    http_method_names = ['get', 'post', 'patch', 'delete']
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_queryset(self):
        if self.request.user.is_anonymous:
            return Recipes.objects.all()

        is_favorited = Favorites.objects.filter(
            recipe=OuterRef('pk'),
            user=self.request.user,
        )
        is_in_shopping_cart = ShoppingCart.objects.filter(
            recipe=OuterRef('pk'),
            user=self.request.user,
        )

        return Recipes.objects.annotate(
            is_favorited=Exists(is_favorited)).annotate(
            is_in_shopping_cart=Exists(is_in_shopping_cart)
        )

    def get_serializer_class(self):
        if self.action in ['create', 'partial_update']:
            return RecipeCreateSerializer
        return RecipeListRetrieveSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @staticmethod
    def add_to(request, serializer, pk):
        data = {
            'user': request.user.id,
            'recipe': pk
        }
        recipe = get_object_or_404(Recipes, id=pk)
        serializer = serializer(data=data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user, recipe=recipe)
        response = RecipeMinifiedSerializer(
            Recipes.objects.get(id=pk), context={'request': request}
        )
        return Response(response.data, status=status.HTTP_201_CREATED)

    @staticmethod
    def remove_from(request, model, pk):
        recipe = get_object_or_404(Recipes, id=pk)
        obj = model.objects.filter(user=request.user, recipe=recipe)
        if not obj:
            return Response(
                'Невозможно удалить рецепт из списка',
                status=status.HTTP_400_BAD_REQUEST
            )
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post'])
    def favorite(self, request, pk):
        return self.add_to(request, FavoriteSerializer, pk)

    @favorite.mapping.delete
    def remove_from_favorite(self, request, pk):
        return self.remove_from(request, Favorites, pk)

    @action(detail=True, methods=['post'],)
    def shopping_cart(self, request, pk):
        return self.add_to(request, ShoppingCartSerializer, pk)

    @shopping_cart.mapping.delete
    def remove_from_shopping_cart(self, request, pk):
        return self.remove_from(request, ShoppingCart, pk)

    @action(detail=False,  methods=['get'],
            permission_classes=(permissions.IsAuthenticated,))
    def download_shopping_cart(self, request):
        recipes = Recipes.objects.filter(
            shopping_cart__user=self.request.user)
        to_purchase = IngredientInRecipe.objects.filter(
            recipe__in=recipes).values(
            'ingredient__name', 'ingredient__measurement_unit').annotate(
            sum=Sum('amount')
        )
        pdf = pdf_shopping_cart.generate(to_purchase)
        return FileResponse(
            pdf,
            as_attachment=True,
            filename='shopping_cart.pdf')
