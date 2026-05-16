from flask import Flask
from models import db   # import the single db instance
from employees import employees_bp
from tasks import tasks_bp

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///company.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize db with app
db.init_app(app)

# Register blueprints
app.register_blueprint(employees_bp)
app.register_blueprint(tasks_bp)

@app.route("/")
def home():
    return {"message": "Employee Task Management System"}

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  
    app.run(debug=True)

