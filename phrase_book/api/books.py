import json

from flask import Blueprint, jsonify, request
from werkzeug.exceptions import NotFound

from phrase_book import db
from phrase_book.models.book import Book
from phrase_book.settings import DISPLAY_NAME

books_blueprint = Blueprint('books', __name__)


# Create a Book
@books_blueprint.route('/', methods=['POST'])
def create_books():
    body = json.loads(request.data)
    book = Book(body[DISPLAY_NAME])
    db.session.add(book)
    db.session.commit()
    return jsonify(book), 201


# Get All Books
@books_blueprint.route('/', methods=['GET'])
def books():
    all_books = Book.query.all()
    return jsonify(all_books)


# Get one Book
@books_blueprint.route('/<book_id>', methods=['GET'])
def get_book(book_id: str):
    book = Book.query.get(book_id)
    if not book:
        raise NotFound(f'Book with id: {book_id} was not found')
    return jsonify(book)


# Update a Book
@books_blueprint.route('/<book_id>', methods=['PUT'])
def update_a_book(book_id: str):
    body = json.loads(request.data)
    db.session.query(Book).filter(Book.id == book_id).update(body)
    db.session.commit()
    return jsonify(Book.query.get(book_id))


# Delete a Book
@books_blueprint.route('/<book_id>', methods=['DELETE'])
def delete_a_book(book_id: str):
    book = Book.query.get(book_id)
    if not book:
        raise NotFound(f'Book with id: {book_id} was not found')
    db.session.delete(book)
    db.session.commit()
    return jsonify({'status': 'ok'})
