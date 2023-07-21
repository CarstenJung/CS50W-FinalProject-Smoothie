from django import template

register = template.Library()


@register.filter
def get_nutrient_value_by_name(food_nutrients, nutrient_name):
    for nutrient in food_nutrients:
        if nutrient['nutrientName'] == nutrient_name:
            return f"{nutrient['value']} {nutrient['unitName']}"
    return "N/A"


@register.filter
def get_nutrient_value_by_id(food_nutrients, nutrient_id):
    for nutrient in food_nutrients:
        if nutrient['nutrientId'] == nutrient_id:
            return f"{nutrient['value']} {nutrient['unitName']}"
    return "N/A"


@register.filter
def get_total_nutrient_value_by_id(total_nutrients, nutrient_id):
    nutrient_data = total_nutrients.get(int(nutrient_id))
    if nutrient_data:
        return f"{nutrient_data['amount']:.2f}"
    return "N/A"


@register.filter
def average_rating(smoothie):
    if not smoothie:
        return "N/A"
    ratings = smoothie.ratings.all()
    if len(ratings) == 0:
        return "N/A"
    else:
        total_rating = sum([r.rating for r in ratings])
        return round(total_rating / len(ratings), 2)


@register.filter
def calculate_nutrient_value(value, weight):
    try:
        numeric_value = float(value)
        numeric_weight = float(weight)
        return round(numeric_value * (numeric_weight / 100), 2)
    except (TypeError, ValueError):
        return 0


@register.filter
def multiply(value, arg):
    return value * arg
