from flask import render_template, request, redirect, session, flash, jsonify
from flask_app import app
from flask_app.models import categories_mod, recipes_mod, shop_items_mod, departments_mod, steps_mod
from flask_app.config.validator import Logged_in
import json
#----------------------------------
# ------------------------------------  Recipe Book
#----------------------------------

@app.route('/recipes')
def recipe_book():
    if Logged_in.checker():
        categories = categories_mod.Category.get_category_names()
        departments = departments_mod.Department.get_departments_names()
        recipes = recipes_mod.Recipe.get_all()
        return render_template('recipe_book.html', departments = departments, categories = categories, recipes = recipes)
    else:
        return redirect('/')

#----------------------------------
#-------------------------------------  Get recipe by ID with Ing,Steps
#----------------------------------

@app.route('/get_recipe_by_id', methods=['POST'])
def get_recipe_by_id():
    recipe = recipes_mod.Recipe.get_recipe_id_json(request.form)
    steps = steps_mod.Step.get_steps(request.form)
    print(steps)
    ingredients = shop_items_mod.Item.get_ingredients_by_recipe(request.form)
    return jsonify({'recipe':recipe,'steps':steps,'ingredients':ingredients})

#----------------------------------
#-------------------------------------  Get recipes by category
#----------------------------------

@app.route('/get_all_recipes', methods=['POST'])
def get_recipes():
    category = recipes_mod.Recipe.get_all_json()
    print(category)
    return category

#----------------------------------
#-------------------------------------  Get recipes by category
#----------------------------------

@app.route('/get_recipes_by_category', methods=['POST'])
def recipes_by_category():
    data = {
        "id" : int(request.form['id'])
    }
    category = categories_mod.Category.get_category_with_recipes_json(data)
    return category
    

#----------------------------------
#-------------------------------------  Delete Recipe
#----------------------------------

@app.route('/delete', methods=['POST'])
def delete():
    recipes_mod.Recipe.delete_recipe(request.form)
    return 'Deleted'


#----------------------------------
#-------------------------------------  Save new recipe
#----------------------------------

@app.route('/add_recipe', methods=["POST"])
def save_recipe():
    recipe = request.form
    print(recipe)
    ####################  parse recipes info  ####################
    recipe_data = {
        "name" : recipe["name"],
        "cook_time" : recipe["cook_time"],
        "serves" : recipe["serves"],
        "comments" : recipe['comments'],
        "users_id" : session["user_id"]
    }
    recipe_id = recipes_mod.Recipe.add_recipe(recipe_data)
    print(recipe_id)
    ####################  Parse categories to list  ####################
    categories = []
    counter = 1
    while(f"cat_{str(counter)}" in recipe):
        categories.append({
            "categories_id": recipe[f'cat_{str(counter)}'],
            "recipes_id" : recipe_id
        })
        counter += 1
    categories_mod.Category.add_rel(categories)
    ####################  parse steps to list  ####################
    step_data = []
    counter = 0
    while(f"step_{str(counter)}" in recipe):
        if recipe[f"step_{str(counter)}"] != "":
            step_data.append({
                "step_num": counter,
                "details": recipe[f'step_{str(counter)}'],
                "recipes_id" : recipe_id
            })
        counter += 1
    steps_mod.Step.add_steps(step_data)
    ####################  parse ingredients to list  ####################
    counter = 1
    while(f"ing_{str(counter)}" in recipe):
        item_data = {
            "name": recipe[f'ing_{str(counter)}'],
            "departments_id": recipe[f'ing_{str(counter)}_department']
        }
        shop_items_mod.Item.add_item(item_data)
        item_id = shop_items_mod.Item.get_item_by_name(item_data)
        ingredient_data = {
            "qty": int(recipe[f'ing_{str(counter)}_qty']),
            "measure": recipe[f'ing_{str(counter)}_measure'],
            "recipes_id": recipe_id,
            "shop_items_id": item_id.id
        }
        shop_items_mod.Item.add_ingredient(ingredient_data)
        counter += 1

    return "Data Recieved"


