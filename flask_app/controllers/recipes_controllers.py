from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models.recipe_model import Recipe


@app.route('/recipes')
def recipes():
    if 'uuid' not in session:
        return redirect('/')
    recipes = Recipe.get_all()
    print(recipes)
    return render_template('recipes.html', recipes = recipes)
    
@app.route('/recipes/new')
def recipes_new():
    if 'uuid' not in session:
        return redirect('/')
    return render_template('recipes_new.html')

@app.route('/recipes/<int:recipe_id>')
def recipes_info(recipe_id):
    if 'uuid' not in session:
        return redirect('/')
    recipe = Recipe.get_one({'id':{recipe_id}})
    # print(recipe)
    return render_template('recipes_info.html', recipe = recipe)


@app.route('/recipes/edit/<int:recipe_id>')
def edit_page(recipe_id):
    if 'uuid' not in session:
        return redirect('/')
    recipe = Recipe.get_one({'id':{recipe_id}})
    return render_template('recipes_edit.html', recipe = recipe)
    

'''
*******************ACTTION ROUTES********************
'''

@app.route('/recipes/create', methods = ['POST'])
def create():
    if 'uuid' not in session:
        return redirect('/')
    if not Recipe.validate_upload(request.form):
        return redirect(f'/recipes/new')
    data  = {
        'name': request.form['name'],
        'description': request.form['description'],
        'below30': request.form['below30'],
        'instruction': request.form['instruction'],
        'cooked_date': request.form['cooked_date']
    }
    recipe_id = Recipe.upload(data) #INSERT METHOD RETURN THE ID OF NEWLY CREATED OBJECT
    user_recipe = {
        "user_id" : session['uuid'],
        'recipe_id':recipe_id
    }
    Recipe.combine(user_recipe)
    return redirect('/recipes')

@app.route('/recipes/edit', methods=['POST'])
def edit():
    if 'uuid' not in session:
        return redirect('/')
    if not Recipe.validate_upload(request.form):
        return redirect(f'/recipes/edit/{request.form["id"]}')
    data = {
        'id':request.form['id'],
        'name': request.form['name'],
        'description': request.form['description'],
        'below30': request.form['below30'],
        'instruction': request.form['instruction'],
        'cooked_date': request.form['cooked_date']
    }
    Recipe.edit(data)
    return redirect('/recipes')

@app.route('/recipes/delete/<int:recipe_id>')
def delete(recipe_id):
    if 'uuid' not in session:
        return redirect('/')
    Recipe.delete({'id':recipe_id})
    return redirect('/recipes')


