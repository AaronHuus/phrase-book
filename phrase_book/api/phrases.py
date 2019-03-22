import json

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

from phrase_book import db
from phrase_book.models.phrase import Phrase
from phrase_book.settings import SOURCE_PHRASE

phrases_blueprint = Blueprint('phrases', __name__)


# Create a Phrase
@phrases_blueprint.route('/', methods=['POST'])
def create_phrases(book_id: str):
    body = json.loads(request.data)
    phrase = Phrase(body[SOURCE_PHRASE], book_id)
    db.session.add(phrase)
    db.session.commit()
    return jsonify(phrase), 201


# Get All Phrase
@phrases_blueprint.route('/', methods=['GET'])
def phrases(book_id: str):
    all_phrases = Phrase.query.filter_by(book_id=book_id).all()
    return jsonify(all_phrases)


# Get one Phrase
@phrases_blueprint.route('/<phrase_id>', methods=['GET'])
def get_phrase(book_id: str, phrase_id: str):
    phrase = Phrase.query.get(phrase_id)
    if not phrase:
        raise NotFound(f'Phrase with id: {phrase_id} of book with id: {phrase_id} was not found')
    return jsonify(phrase)


# Update a Phrase
@phrases_blueprint.route('/<phrase_id>', methods=['PUT'])
def update_a_phrase(book_id: str, phrase_id: str):
    body = json.loads(request.data)
    phrase = Phrase.query.get(phrase_id)
    if not phrase:
        raise NotFound(f'Phrase with id: {phrase_id} of book with id: {phrase_id} was not found')
    db.session.query(Phrase).filter(Phrase.id == phrase_id).update(body)
    db.session.commit()
    return jsonify(Phrase.query.get(phrase_id))


# Delete a Phrase
@phrases_blueprint.route('/<phrase_id>', methods=['DELETE'])
def delete_a_phrase(book_id: str, phrase_id: str):
    phrase = Phrase.query.get(phrase_id)
    if not phrase:
        raise NotFound(f'Phrase with id: {phrase_id} of book with id: {phrase_id} was not found')
    db.session.delete(phrase)
    db.session.commit()
    return jsonify({'status': 'ok'})
