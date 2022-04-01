from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models import recipes_mod
import json

####################  Category Model  ####################

class Category:
    db = "recipe_shopper_schema" # Schema name here

    def __init__(self, data): # layout instance attributes according to table column header
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = {}

#----------------------------------
#-------------------------------------  Add recipe/category relationship
#----------------------------------

    @classmethod
    def add_rel(cls, data):
        for rel in data:
            query = """INSERT INTO
                    categories_recipes (categories_id, recipes_id, created_at)
                    VALUES
                    (%(categories_id)s, %(recipes_id)s, now());
                    """
            MySQLConnection(cls.db).query_db(query,rel)
        

#----------------------------------
#-------------------------------------  Get all category names
#----------------------------------

    @classmethod
    def get_category_names(cls):
        query =  """SELECT *
                    FROM categories"""
        returned_data = MySQLConnection(cls.db).query_db(query)
        instances = []
        for row in returned_data:
            data = {
                "id" : row["id"],
                "name" : row["name"].capitalize(),
                "created_at" : row["created_at"],
                "updated_at" : row["updated_at"]
            }
            instances.append(cls(data))
        return instances

#----------------------------------
#-------------------------------------  Get a category with all recipes
#----------------------------------

    @classmethod
    def get_category_with_recipes_json(cls, data):
        query =  """SELECT *
                    FROM categories
                    JOIN categories_recipes
                    ON categories_recipes.categories_id = categories.id
                    JOIN recipes 
                    ON categories_recipes.recipes_id = recipes.id
                    WHERE categories.id = %(id)s;
                    """
        returned_data = MySQLConnection(cls.db).query_db(query,data)
        if not returned_data:
            return False
        recipes = {}
        for i in range(len(returned_data)):
            recipe_data = {
                "id" : returned_data[i]['recipes.id'],
                "name" : returned_data[i]['recipes.name'],
                "cook_time" : returned_data[i]['cook_time']
            }
            recipes[str(i)] = recipe_data
        return json.dumps(recipes)