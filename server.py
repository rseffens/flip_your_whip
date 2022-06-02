from flask_app import app
from flask_app.controllers import user_controllers
# from flask_app.controllers import car_controllers


if __name__=="__main__":   # Ensure this file is being run directly and not from a different module    
    app.run(debug=True)    # Run the app in debug mode.