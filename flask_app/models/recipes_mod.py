from flask_app.config.mysqlconnection import MySQLConnection
import json
####################  Recipe Model  ####################

class Recipe:
    db = "recipe_shopper_schema" # Schema name here

    def __init__(self, data): # layout instance attributes according to table column header
        self.id = data['id']
        self.name = data['name']
        self.cook_time = data['cook_time']
        self.comments = data['comments']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.categories = []
        self.steps = []
        self.ingredients = []

#----------------------------------
#-------------------------------------  Save new recipe
#----------------------------------

    @classmethod
    def add_recipe(cls, data):
        query =  """INSERT INTO
                    recipes 
                    (users_id, name, cook_time, serves, comments, created_at)
                    VALUES
                    (%(users_id)s, %(name)s, %(cook_time)s, %(serves)s, %(comments)s, now());
                    """
        return MySQLConnection(cls.db).query_db(query,data)

#----------------------------------
#-------------------------------------  Get all
#----------------------------------

    @classmethod
    def get_all(cls):
        query =  """SELECT * FROM recipes"""
        returned_data = MySQLConnection(cls.db).query_db(query)
        instances = [cls(row) for row in returned_data]
        return instances

#----------------------------------
#-------------------------------------  Get all json
#----------------------------------

    @classmethod
    def get_all_json(cls):
        query =  """SELECT id, name, cook_time FROM recipes"""
        returned_data = MySQLConnection(cls.db).query_db(query)
        instances = {}
        for i in range(len(returned_data)):
            instances[str(i)] = returned_data[i]
        js = json.dumps(instances)
        return js

#----------------------------------
#-------------------------------------  Get recipe with Ings,Steps JSON
#----------------------------------

    @classmethod
    def get_recipe_id_json(cls, data):
        query =  """SELECT recipes.name, cook_time, serves, comments
                    FROM recipes
                    WHERE
                    recipes.id = %(id)s"""
        returned_data = MySQLConnection(cls.db).query_db(query, data)
        recipe = {data['id']:returned_data[0]}
        return recipe

#----------------------------------
#-------------------------------------  Delete Recipe
#----------------------------------

    @classmethod
    def delete_recipe(cls, data):
        query =  """DELETE
                    FROM recipes
                    WHERE
                    id = %(id)s"""
        MySQLConnection(cls.db).query_db(query,data)
        