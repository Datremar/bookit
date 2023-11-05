from flask import Flask
from routes.healthcheck import health_blueprint
from routes.auth import auth_blueprint
from routes.notifications import notif_blueprint
from routes.timesheets import blueprint as timesheets_blueprint

app = Flask(__name__)  # flask app object
app.config.from_object('config')  # Configuring from Python Files

# Registering the blueprint
app.register_blueprint(auth_blueprint, url_prefix='/auth')
app.register_blueprint(health_blueprint, url_prefix='/healthcheck')
app.register_blueprint(notif_blueprint, url_prefix='/notifications')
app.register_blueprint(timesheets_blueprint, url_prefix='/timesheets')

if __name__ == '__main__':  # Running the app
    app.run(host='127.0.0.1', port=5000, debug=True)
