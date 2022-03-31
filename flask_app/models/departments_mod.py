from flask_app.config.mysqlconnection import MySQLConnection
from flask_app.models import recipes_mod

####################  Category Model  ####################

class Department:
    db = "recipe_shopper_schema" # Schema name here

    def __init__(self, data): # layout instance attributes according to table column header
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#----------------------------------
#-------------------------------------  Get all category names
#----------------------------------

    @classmethod
    def get_departments_names(cls):
        query =  """SELECT *
                    FROM departments"""
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
    def get_category_with_recipes(cls, data):
        query =  """SELECT *
                    FROM categories
                    JOIN categories_recipes
                    ON categories_recipes.categories_id = categories.id
                    JOIN recipes 
                    ON categories_recipes.recipes_id = recipes.id;
                    WHERE categories.id = %(id)s
                    """
        returned_data = MySQLConnection(cls.db).query_db(query,data)
        instance = cls(returned_data[0])
        for row in returned_data:
            recipe_data = {
                "id" : row['recipes.id'],
                "name" : row['recipes.name'],
                "cook_time" : row['cook_time'],
                "comments" : row['comments'],
                "created_at" : row['recipes.created_at'],
                "updated_at" : row['recipes.updated_at']
            }
            instance.recipes[row['recipes.id']] = recipes_mod.Recipe(recipe_data) 
        return instance