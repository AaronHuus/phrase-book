from unittest import TestCase

from phrase_book.models.book import Book


class TestBooks(TestCase):

    def test_book_creation(self):
        book: Book = Book('Book Display Name')
        self.assertEqual(book.phrases, [])
        self.assertIsNotNone(book.id)
