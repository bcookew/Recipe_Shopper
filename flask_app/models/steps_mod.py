from flask_app.config.mysqlconnection import MySQLConnection

####################  Steps Model  ####################

class Step:
    db = "recipe_shopper_schema" # Schema name here

    def __init__(self, data): # layout instance attributes according to table column header
        self.id = data['id']
        self.step = data['step']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

#----------------------------------
#-------------------------------------  Add Steps associated with a recipe
#----------------------------------

    @classmethod
    def add_steps(cls, data):
        for step in data:
            query =  """INSERT INTO
                    steps
                    (step_num, details, created_at, recipes_id)
                    VALUES
                    (%(step_num)s, %(details)s, NOW(), %(recipes_id)s);
                    """
            MySQLConnection(cls.db).query_db(query,step)

#----------------------------------
#-------------------------------------  get_steps_for_recipe
#----------------------------------

    @classmethod
    def get_steps(cls, data):
        query =  """SELECT step_num, details
                    FROM steps
                    WHERE
                    recipes_id = %(id)s"""
        returned_data = MySQLConnection(cls.db).query_db(query,data)
        steps = {}
        for i in range(len(returned_data)):
            steps["step "+str(i)] = returned_data[i]
        return steps