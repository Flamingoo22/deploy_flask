from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models.user_model import User
from flask import flash, session

class Recipe():
    def __init__(self, db_data):
        self.id = db_data['id']
        self.name = db_data['name']
        self.description = db_data['description']
        self.below30 = db_data['below30']
        self.instruction = db_data['instruction']
        self.cooked_date = db_data['cooked_date']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        
    @classmethod
    def upload(cls, data):
        query = '''
                INSERT INTO recipes (name, description, below30, instruction, cooked_date)
                VALUES (%(name)s, %(description)s, %(below30)s, %(instruction)s, %(cooked_date)s);
                '''
        return connectToMySQL('recipe').query_db(query, data)

    @classmethod
    def edit(cls, data):
        query = '''
                UPDATE recipes
                SET recipes.name = %(name)s, recipes.description = %(description)s, recipes.below30=%(below30)s, recipes.instruction=%(instruction)s, recipes.cooked_date=%(cooked_date)s
                WHERE recipes.id = %(id)s;
                '''
        return connectToMySQL('recipe').query_db(query, data)
    @classmethod
    def combine(cls, data):
        query = '''
                INSERT INTO share_recipe (user_id, recipe_id)
                VALUES (%(user_id)s, %(recipe_id)s)
                '''
        return connectToMySQL('recipe').query_db(query, data)
    
    
    
    @classmethod
    def delete(cls, data):
        query = '''
                DELETE
                FROM recipes
                WHERE recipes.id = %(id)s;
                '''
        return connectToMySQL('recipe').query_db(query, data)
    
    @classmethod
    def together(cls, data):
        query = '''
                SELECT * 
                FROM users
                WHERE users.id NOT IN(
                SELECT *
                FROM recipes
                LEFT JOIN share_recipes
                ON recipes.id = share_recipes.recipe_id
                LEFT JOIN users
                ON share_recipes.user_id = users.id
                WHERE recipes.id = %(id)s
                );
                '''
        results = connectToMySQL('recipes').query_db(query, data)
        if not results:
            return False
        users_has_not_participate = []
        for user in results:
            users_has_not_participate.append(User(user))
        return users_has_not_participate
        
    
    @classmethod
    def get_one(cls, data):
        query = '''
                SELECT *
                FROM recipes
                LEFT JOIN share_recipe
                ON recipes.id = share_recipe.recipe_id
                LEFT JOIN users
                ON share_recipe.user_id = users.id
                WHERE recipes.id = %(id)s
                '''
        results = connectToMySQL('recipe').query_db(query, data)
        if results:
            for recipe in results:
                recipe_instance = cls(recipe)
                recipe_data = {
                    **recipe,
                    "id":recipe['users.id'],
                    'created_at':recipe['users.created_at'],
                    'updated_at':recipe['users.updated_at']
                }
                user_instance = User(recipe_data)
                recipe_instance.owner = user_instance
            return recipe_instance
        else:
            return False
        
    @classmethod
    def get_all_recipesonly(cls):
        query = '''
                SELECT *
                FROM recipes
                LEFT JOIN share_recipe
                ON recipes.id = share_recipe.recipe_id
                LEFT JOIN users
                ON share_recipe.user_id = users.id
                '''
        results = connectToMySQL('recipe').query_db(query)
        all_recipes = []
        for row_db in results:
            all_recipes.append(cls(row_db))
        return all_recipes
    
    @classmethod
    def get_all(cls):
        query = '''
                SELECT *
                FROM recipes
                LEFT JOIN share_recipe
                ON recipes.id = share_recipe.recipe_id
                LEFT JOIN users
                ON share_recipe.user_id = users.id
                '''
        results = connectToMySQL('recipe').query_db(query)
        if results:
            recipes = []
            for recipe in results:
                recipe_instance = cls(recipe)
                recipe_data = {
                    **recipe,
                    "id":recipe['users.id'],
                    'created_at':recipe['users.created_at'],
                    'updated_at':recipe['users.updated_at']
                }
                user_instance = User(recipe_data)
                recipe_instance.owner = user_instance
                recipes.append(recipe_instance)
            return recipes
        else:
            return False
        
    @staticmethod
    def validate_upload(data):
        is_valid = True
        if len(data['name']) <=3:
            flash('Name is required', 'err_recipes_name')
            is_valid = False
        if len(data['description']) <=3:
            flash('Description Cannot be Empty','err_recipes_description')
            is_valid = False
        if 'below30' not in data:
            flash('Please Specify cooking time is over/under 30 minutes','err_recipes_below30')
            is_valid = False
        if len(data['instruction']) <=3:
            flash('Instrution Cannot be Empty','err_recipes_instruction')
            is_valid = False
        if len(data['cooked_date']) <=0:
            flash('cooked_time is required','err_recipes_cooked_date')
            is_valid = False
        return is_valid