from django_filters import ChoiceFilter, FilterSet, ModelMultipleChoiceFilter
from recipes.models import Recipes, Tag

CHOICES = (
    (1, True),
    (0, False),
)


class RecipeFilter(FilterSet):
    is_favorited = ChoiceFilter(field_name='is_favorited', choices=CHOICES)
    is_in_shopping_cart = ChoiceFilter(
        field_name='is_in_shopping_cart', choices=CHOICES
    )
    tags = ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
    )

    class Meta:
        model = Recipes
        fields = ('is_favorited', 'is_in_shopping_cart', 'author', 'tags',)
