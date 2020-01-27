import os
from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types
from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from google.protobuf.json_format import MessageToJson, MessageToDict

from flask import current_app as app
client = language.LanguageServiceClient()

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('CLOUD_SQL_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)

from models.entity import Entity


def sentiments(request):
    request_json = request.get_json()
    if request_json and 'data' in request_json:
        return jsonify(MessageToDict(get_entity_sentiment(request_json['data']))['entities']), 202
       # return request_json['data']
    else:
        return f'Error, please include some data to translate', 400

def testSQL(request):
    entity = Entity.query.first()
    return jsonify(entity), 200

def sentimentsPersist(request):
    request_json = request.get_json()
    if request_json and 'data' in request_json:
        entityResponse = get_entity_sentiment(request_json['data'])
        entities = entityResponse.entities
        for entity in entities:
            print(entity.sentiment.score)
            newEntity = Entity(entityKeyword=entity.name,
                   averageSentiment=entity.sentiment.score,
                   averageMagnitude=entity.sentiment.magnitude,
                   courseId=request.headers['courseId'],
                   submissionId=request.headers['submissionId'])
            db.session.add(newEntity)
        db.session.commit()

        return jsonify(MessageToDict(entityResponse)['entities']), 201
       # return request_json['data']
    else:
        return f'Error, please include some data to translate', 400

def getPersistedSentimentsByCourse(request):
    entities = Entity.query.filter(Entity.courseId == request.headers['courseId']).all()
    return jsonify(entities), 200

def entities(request):
    request_json = request.get_json()
    if request_json and 'data' in request_json:
        return jsonify(MessageToDict(get_entities(request_json['data']))['entities']), 202
       # return request_json['data']
    else:
        return f'Error, please include some data to translate', 400

def get_sentiment(text):
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_sentiment(document)
    return response

def get_entity_sentiment(text):
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_entity_sentiment(document)
    for entity in response.entities:
        print(u"Representative name for the entity: {}".format(entity.name))
        print(u"Entity type: {}".format(enums.Entity.Type(entity.type).name))
        print(u"Salience score: {}".format(entity.salience))
        sentiment = entity.sentiment
        print(u"Entity sentiment score: {}".format(sentiment.score))
        print(u"Entity sentiment magnitude: {}".format(sentiment.magnitude))

        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{} = {}".format(metadata_name, metadata_value))
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))
            print(
                u"Mention type: {}".format(enums.EntityMention.Type(mention.type).name)
            )
    return response

def get_entities(text):
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)
    response = client.analyze_entities(document)
    return response
