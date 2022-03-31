from flask_app import app
from flask_app.controllers import user_con, recipe_con


if __name__ == "__main__":
    app.run(debug=True)