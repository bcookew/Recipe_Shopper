from flask_app.config.mysqlconnection import MySQLConnection

####################  Shop Item - Dual use Model - shopping list items / recipe ingredients ####################
####################  Check section breaks for which methods apply to which tables   ####################

class Item:
    db = "recipe_shopper_schema" # Schema name here

    def __init__(self, data): # layout instance attributes according to table column header
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.department = None

#----------------------------------
#-------------------------------------  Add item to DB
#----------------------------------

    @classmethod
    def add_item(cls, data):
        query =  """INSERT IGNORE INTO
                    shop_items (name, created_at, departments_id)
                    VALUES
                    (%(name)s, now(), %(departments_id)s);
                    """
        return MySQLConnection(cls.db).query_db(query, data)

#----------------------------------
#-------------------------------------  Add ingredient relationship
#----------------------------------

    @classmethod
    def add_ingredient(cls, data):
        query =  """INSERT INTO
                    recipes_ingredients
                    (recipes_id, shop_items_id, qty, measure, created_at)
                    VALUES
                    (%(recipes_id)s, %(shop_items_id)s, %(qty)s, %(measure)s, NOW());
                    """
        MySQLConnection(cls.db).query_db(query,data)        

#----------------------------------
#-------------------------------------  Get item by name
#----------------------------------

    @classmethod
    def get_item_by_name(cls, data):
        query =  """SELECT *
                    FROM shop_items
                    WHERE
                    name = %(name)s;
                    """
        returned_data = MySQLConnection(cls.db).query_db(query,data)
        return cls(returned_data[0])
        

#----------------------------------
#-------------------------------------  Get ingredients by recipe id
#----------------------------------

    @classmethod
    def get_ingredients_by_recipe(cls, data):
        query =  """SELECT shop_items.name, qty, measure
                    FROM recipes
                    JOIN recipes_ingredients
                    ON recipes.id = recipes_ingredients.recipes_id
                    JOIN shop_items
                    ON shop_items.id = recipes_ingredients.shop_items_id
                    WHERE
                    recipes.id = %(id)s;
                    """
        returned_data = MySQLConnection(cls.db).query_db(query,data)
        ingredients={}
        for i in range(len(returned_data)):
            ingredients['ing_'+str(i)] = returned_data[i]
        return ingredients
        
