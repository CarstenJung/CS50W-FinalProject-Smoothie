from django.http import JsonResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from smoothie.models import Smoothie, SmoothieIngredient, Rating
from forms import SmoothieForm
from forms import SearchForm
import requests

# Mainpage view function
def index(request, smoothie_id=None):
    # Post request to get ingredients with nutrition information
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
            params = {
                'api_key': 'Get a free one from https://fdc.nal.usda.gov/api-key-signup.html',
                'query': query,
                'pageSize': 10,
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            foods = response.json()['foods']
            context = {'foods': foods}
            if smoothie_id:
                context['smoothie_id'] = smoothie_id
            return render(request, 'index.html', context)
        # Handle Get request for initial page load
    else:
        form = SearchForm()
    context = {'form': form, 'smoothie_id': smoothie_id}
    return render(request, 'index.html', context)


# Register view function
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('register')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Login view function
@login_required
def create_smoothie(request):
    # Post request to create a new smoothie
    if request.method == 'POST':
        form = SmoothieForm(request.POST)
        if form.is_valid():
            # Save the new smoothie and associate it with the current user
            smoothie = form.save(commit=False)
            smoothie.user = request.user
            smoothie.save()
            return redirect('view_smoothie', smoothie_id=smoothie.id)
        # Handle Get request for initial page load
    else:
        form = SmoothieForm()
    return render(request, 'create_smoothie.html', {'form': form})


# View smoothie view function
@login_required
def view_smoothie(request, smoothie_id):
    # Get smoothie from database
    smoothie = Smoothie.objects.get(id=smoothie_id)
    # Set default values for grams (API response is per 100g)
    grams = 100

    # Search form submission, adding or deleting ingredients
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            query = form.cleaned_data['query']
            url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
            params = {
                'api_key': 'elhyRfYJ42dSR6zWHJXgOeU9zudQ7wfawa1hYFP8',
                'query': query,
                'pageSize': 1,
            }
            response = requests.get(url, params=params)
            response.raise_for_status()
            foods = response.json()['foods']
            context = {
                'foods': foods,
                'smoothie': smoothie,
            }
            # Return the search results to the view smoothie page
            return render(request, 'view_smoothie.html', context)
        # Handle adding or deleting ingredients
        elif 'fdc_id' in request.POST and 'description' in request.POST and 'quantity' in request.POST and 'grams' in request.POST:
            fdc_id = request.POST['fdc_id']
            description = request.POST['description']
            quantity = int(request.POST['quantity'])
            grams = float(request.POST['grams']) / 100
            SmoothieIngredient.objects.create(
                smoothie=smoothie, fdc_id=fdc_id, description=description, quantity=quantity, grams=grams)
            # Redirect to the view smoothie page to show the new ingredient
            return redirect('view_smoothie', smoothie_id=smoothie.id)
        # Handle deleting ingredients
        elif 'delete_ingredient_id' in request.POST:
            ingredient_id = request.POST['delete_ingredient_id']
            SmoothieIngredient.objects.filter(id=ingredient_id).delete()
            return redirect('view_smoothie', smoothie_id=smoothie.id)
    else:
        form = SearchForm()

    # Retrieve all ingredients for the current smoothie
    ingredients = SmoothieIngredient.objects.filter(smoothie=smoothie)
    total_nutrients = {}

    # Calculate the total nutrients for the smoothie
    for ingredient in ingredients:
        url = f'https://api.nal.usda.gov/fdc/v1/food/{ingredient.fdc_id}'
        params = {'api_key': 'elhyRfYJ42dSR6zWHJXgOeU9zudQ7wfawa1hYFP8'}
        response = requests.get(url, params=params)
        response.raise_for_status()
        food_data = response.json()

        # Nutrient data for each ingredient
        for nutrient in food_data['foodNutrients']:
            nutrient_id = nutrient['nutrient']['id']
            nutrient_name = nutrient['nutrient']['name']
            nutrient_amount = nutrient['amount'] * \
                float(ingredient.quantity) * ingredient.grams
            nutrient_unit = nutrient['nutrient']['unitName']

            # Add or update the nutrient in the total nutrients dictionary
            if nutrient_id not in total_nutrients:
                total_nutrients[nutrient_id] = {
                    'name': nutrient_name,
                    'amount': nutrient_amount,
                    'unit': nutrient_unit,
                }
            else:
                total_nutrients[nutrient_id]['amount'] += nutrient_amount

    context = {
        'smoothie': smoothie,
        'ingredients': ingredients,
        'form': form,
        'total_nutrients': total_nutrients,
        'grams': grams,
    }
    return render(request, 'view_smoothie.html', context)


# List smoothies view function
@login_required
def list_smoothies(request):
    # Get all smoothies
    if request.method == 'POST':
        # Handle deleting smoothies
        if 'delete_smoothie_id' in request.POST:
            smoothie_id = request.POST['delete_smoothie_id']
            Smoothie.objects.filter(user=request.user, id=smoothie_id).delete()
        # Rating smoothies
        elif 'rate_smoothie_id' in request.POST:
            smoothie_id = request.POST['rate_smoothie_id']
            rating_value = int(request.POST['rating'])

            smoothie = Smoothie.objects.get(id=smoothie_id)
            user = request.user

            # Check if the user has already rated this smoothie
            user_rating = Rating.objects.filter(
                smoothie=smoothie, user=user).first()
            if user_rating:
                # Update the existing rating
                user_rating.rating = rating_value
                user_rating.save()
            else:
                # Create a new rating for the smoothie
                rating = Rating(smoothie=smoothie, user=user,
                                rating=rating_value)
                rating.save()

            # Redirect to the same page to refresh the ratings
            return redirect('list_smoothies')

    # Retrieve all smoothies from the database
    smoothies = Smoothie.objects.all()
    return render(request, 'list_smoothies.html', {'smoothies': smoothies})
