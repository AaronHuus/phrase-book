from flask import Blueprint, jsonify
from werkzeug.exceptions import NotFound

from phrase_book.objects.book import Book

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/', methods=['GET'])
def books():
    return jsonify([])


@books_blueprint.route('/<book_id>', methods=['GET'])
def get_book(book_id: str):
    book = get_book_by_id(book_id)
    if not book:
        raise NotFound(f'Book with id: {book_id} was not found')
    return jsonify(book)


def get_book_by_id(book_id: str):
    return Book()
