# Smoothie Web Application
Smoothie is a web application that allows users to create, view, and rate custom smoothies while providing detailed nutritional information using the API from https://www.nal.usda.gov/.

## Distinctiveness and Complexity:
As the name suggests, Smoothie is an app for putting together your own smoothies or asking for information about certain ingredients.

The data is processed and converted according to weights. The user is given a complete nutritional value table with various data on energy vitamins etc. based on their input.

### Complexity: The main functions of the app are
```
1. Search of ingredients.
2. Create your own smoothies and add ingredients by weight.
3. View all the fruit used in a smoothie with weight, energy and various vitamin data. Always calculated according to the corresponding input quantity.
4. Smoothies can be viewed and rated by all users under Custom Smoothies. The rating is calculated from the entries of all users.
5. A delete button is only displayed for the creator of the respective smoothie
```

## What’s contained in each file you created
### View.py:
```
index view: Render the main page when the user logs in. A field is shown here in which the user can search for various ingredients via the API and display the corresponding information.

login/register view: Takes care of login register

create_smoothie view: Function to create smoothies and store them in the database

view_smoothie view: In this function, the various smoothies are retrieved and can be edited. So ingredients can be added or deleted. In addition, the calculation of the nutrition information is managed

list_smoothies view: All smoothies are listed here. If the user is the creator, he can delete the entry. In addition, the smoothie can be rated by all users and an average of all ratings is created.
```

### Nutrition_tags
```
nutrition_tags.py: My custom template tags with functions and filters to help fetch and manipulate data.
```

### Models.py
This file contains the database models for the Smoothie web application. It defines the following models:

```
Smoothie: Represents a smoothie created by a user. It has a foreign key relationship with the User model and a name field to store the smoothie's name.

SmoothieIngredient: Represents an ingredient added to a smoothie. It has a foreign key relationship with the Smoothie model and contains the following fields: fdc_id for the ingredient's ID from the API, description for the ingredient's name, quantity for the number of units added to the smoothie, and grams for the weight of the ingredient in grams.

Rating: Represents a user's rating of a smoothie. It has foreign key relationships with both the Smoothie and User models. It also has a rating field that stores the rating value as a positive integer, with choices ranging from 1 to 5 stars.

```

### Folder: Templates
```
Contains various HTML files that are responsible for displaying the views and that extend layout.html
```

## How to run your application.
```
1. Clone the repository
2. Install the required packages using pip install -r requirements.txt.
3. Run the following commands to set up the database:
    python3 manage.py migrate
    python3 manage.py makemigrations

4. Start the app from the terminal using: python3 manage.py runserver.