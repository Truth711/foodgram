import io

import reportlab
from django.conf import settings
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

reportlab.rl_config.TTFSearchPath.append(
    str(settings.BASE_DIR) + '/recipes/fonts'
)
pdfmetrics.registerFont(TTFont('FreeSans', 'FreeSans.ttf'))


def parse_data(ingredients_to_purchase):
    ingredients = {}
    for i in ingredients_to_purchase:
        ingredients[i.ingredient] = ingredients.get(i.ingredient, 0) + i.amount

    parsed_data = []
    for key, value in ingredients.items():
        pdf_string = [
            key.name,
            key.measurement_unit,
            value,
        ]
        parsed_data.append(pdf_string)
    return parsed_data


def generate(ingredients_to_purchase):
    buff = io.BytesIO()
    file = canvas.Canvas(buff, pagesize=A4)

    file.setFont('FreeSans', 17, leading=None)
    file.drawString(200, 811, 'Список покупок:')
    file.line(0, 780, 1000, 780)
    parsed_data = parse_data(ingredients_to_purchase)
    x = 100
    y = 600

    for string in parsed_data:
        file.setFont('FreeSans', 15, leading=None)
        file.drawString(
            x,
            y,
            f'- {string[0]} ({string[1]}) - {str(string[2])}'
        )
        y += 15

    file.showPage()
    file.save()
    buff.seek(0)
    return buff
