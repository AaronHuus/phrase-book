from unittest import TestCase

import app
from phrase_book.models.book import Book


class TestBooks(TestCase):

    def setUp(self):
        app.testing = True

    def test_book_creation(self):
        book: Book = Book('Book Display Name')
        self.assertEqual(book.phrases, [])
        self.assertIsNotNone(book.id)
