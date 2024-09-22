from flask import Flask
from config import Config
from models import db, bcrypt
from routes import api, jwt

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
bcrypt.init_app(app)
jwt.init_app(app)

# Register the blueprint
app.register_blueprint(api, url_prefix='/api')

# Create the database tables
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)