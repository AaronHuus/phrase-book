from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound

from phrase_book.api.books import get_book_by_id
from phrase_book.objects.book import Book

phrases_blueprint = Blueprint('phrases', __name__)


@phrases_blueprint.route('/phrases', methods=['GET'])
def phrases(book_id):
    book: Book = get_book_by_id(book_id)
    return jsonify(book.phrases)


@phrases_blueprint.route('/phrases/<phrase_id>', methods=['GET'])
def get_phrase(book_id, phrase_id):
    book: Book = get_book_by_id(book_id)
    filtered_phrases = [p for p in book.phrases if p.id == phrase_id]
    if not filtered_phrases:
        raise NotFound(f'Phrase with id: {phrase_id} of book with id: {book_id} was not found')
    return jsonify(filtered_phrases[0])
