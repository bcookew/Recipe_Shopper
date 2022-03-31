from flask_app.config.mysqlconnection import MySQLConnection
import shopping_items_mod

####################  Weekly Plan Model  ####################

class Weekly_Plan:
    db = "recipe_shopper_schema" # Schema name here

    def __init__(self, data): # layout instance attributes according to table column header
        self.id = data['id']
        self.week_starting = data['week_starting']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []
        self.shopping = []


#----------------------------------
#-------------------------------------  Get shopping list
#----------------------------------

    def get_shopping(self, data):
        data = {'week_starting':self.week_starting}
        self.shopping = shopping_items_mod.Shopping_Item.shopping_list_by_week(data)
        return self