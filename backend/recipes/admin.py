from django.contrib import admin
from .models import (Tag, Ingredient, Recipes,
                     Favorites, IngredientInRecipe, ShoppingCart)


class RecipeAdmin(admin.ModelAdmin):
    list_select_related = ('author',)
    list_display = ('name', 'author', 'times_added_to_favorites')
    list_display_links = ('name', )
    list_filter = ('name', 'author', 'tags',)
    empty_value_display = '-пусто-'

    @admin.display(description='Число добавлений этого рецепта в избранное')
    def times_added_to_favorites(self, obj):
        return obj.favorites_recipe.count()


class IngredientAdmin(admin.ModelAdmin):
    list_display = ('name', 'measurement_unit',)
    list_display_links = ('name',)
    list_filter = ('name',)
    empty_value_display = '-пусто-'


admin.site.register(Tag)
admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(Recipes, RecipeAdmin)
admin.site.register(Favorites)
admin.site.register(IngredientInRecipe)
admin.site.register(ShoppingCart)
