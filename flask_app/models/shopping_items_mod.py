from flask_app.config.mysqlconnection import MySQLConnection

####################  Shop Item - Dual use Model - shopping list items / recipe ingredients ####################
####################  Check section breaks for which methods apply to which tables   ####################

class Shopping_Item:
    db = "recipe_shopper_schema" # Schema name here

    def __init__(self, data): # layout instance attributes according to table column header
        self.id = data['id']
        self.name = data['name']
        self.qty = data['qty']
        self.measure = data['measure']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.department = None

#----------------------------------
#-------------------------------------  Get shopping list by week
#----------------------------------

    @classmethod
    def shopping_list_by_week(cls, data):
        query =  """SELECT *
                    FROM shop_items
                    JOIN departments
                    ON shop_items.departments_id = departments.id
                    JOIN shopping_lists_items
                    ON  shopping_lists_items.shop_items_id = shop_items.id
                    JOIN weekly_plans
                    ON weekly_plans.id = shopping_lists_items.weekly_plans_id
                    WHERE
                    weekly_plans.week_starting = %(week_starting)s
                    """
        returned_data = MySQLConnection(cls.db).query_db(query,data)
        for row in returned_data:
            data = {

            }
        
        return instances