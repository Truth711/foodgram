import csv

from django.conf import settings
from django.core.management.base import BaseCommand
from recipes.models import Ingredient


class Command(BaseCommand):
    help = 'load ingredients from csv'

    def handle(self, *args, **options):
        data_dir = settings.BASE_DIR
        with open(
            f'{data_dir}/data/ingredients.csv',
            'r',
            encoding="utf-8-sig"
        ) as csv_file:
            csv_reader = csv.reader(csv_file)
            for row in csv_reader:
                name = row[0]
                measurement_unit = row[1]
                ingredient = Ingredient(
                    name=name, measurement_unit=measurement_unit)
                ingredient.save()
        self.stdout.write(self.style.SUCCESS('Done!'))
