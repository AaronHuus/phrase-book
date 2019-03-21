import json

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

from phrase_book import db
from phrase_book.models.book import Book
from phrase_book.settings import DISPLAY_NAME

books_blueprint = Blueprint('books', __name__)


@books_blueprint.route('/', methods=['POST'])
def create_books():
    body = json.loads(request.data)
    book = Book(body[DISPLAY_NAME])
    db.session.add(book)
    db.session.commit()
    return jsonify(book), 201


@books_blueprint.route('/', methods=['GET'])
def books():
    all_books = Book.query.all()
    return jsonify(all_books)


@books_blueprint.route('/<book_id>', methods=['GET'])
def get_book(book_id: str):
    book = get_book_by_id(book_id)
    if not book:
        raise NotFound(f'Book with id: {book_id} was not found')
    return jsonify(book)


def get_book_by_id(book_id: str):
    return Book()
