import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CLOUD_SQL_URI')
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    schoolId = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=False, nullable=False)
    slack = db.Column(db.String(30), unique=True, nullable=False)
    #achievedKPIs = koppeltabel naar kpis behaald
    #inProgressKPIs = koppeltabel naarh uidige kpis
    #entities = koppeltabel naar entities met eigen magnitude en sentiment averaged van docs en het aantal docs waarin het voorkwam
    #skills = koppeltabel