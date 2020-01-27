import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CLOUD_SQL_URI')
db = SQLAlchemy(app)

class Skill(db.Model):
    skillId = db.Column(db.String(80), unique=True, nullable=False, primary_key=True)
   # relevantKPIs = koppeltabel
   # relevantEntities = koppeltabel
