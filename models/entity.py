import sqlalchemy
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass

from sqlalchemy.dialects.postgresql import UUID

db = SQLAlchemy(app)

@dataclass()
class Entity(db.Model):
    entityId: str
    entityKeyword: str
    courseId: str
    submissionId: str
    averageSentiment: float
    averageMagnitude: float

    entityId = db.Column(UUID(as_uuid=True), unique=True, nullable=False, primary_key=True, server_default=sqlalchemy.text("uuid_generate_v4()"))
    entityKeyword = db.Column(db.String(80), unique=False, nullable=False)
    courseId = db.Column(db.String(160), unique=False, nullable=True)
    submissionId = db.Column(db.String(160), unique=False, nullable=True)
    averageSentiment = db.Column(db.Float(), unique=False, nullable=False)
    averageMagnitude = db.Column(db.Float(), unique=False, nullable=False)

db.create_all()