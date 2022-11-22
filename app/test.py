from flask import Flask
from app.models.summary import Summary
from app.models.db import db

from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://fdadmin:NCSAfarmdoc##@fd-postgres-dev:5432/pdl"
# db = SQLAlchemy(app)
# migrate = Migrate(app, db)
db.init_app(app)

@app.route('/summary', methods=['GET'])
def handle_summary():
    cars = Summary.query.all()
    results = [
        {
            "title": car.title,
            "state": car.state,
            "amount": car.amount
        } for car in cars]

    return {"count": len(results), "cars": results}

# class Summary(db.Model):
#     __tablename__ = 'summary'
#
#     summary_code = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String())
#     state = db.Column(db.String())
#     amount = db.Column(db.Integer())
#
#     def __init__(self, title, state, amount):
#         self.name = title
#         self.model = state
#         self.doors = amount
#
#     def __repr__(self):
#         return f"<Car {self.name}>"

if __name__ == '__main__':
    app.run(debug=True)