from unittest import TestCase

from phrase_book.objects.book import Book


class TestBooks(TestCase):

    def test_book_creation(self):
        book: Book = Book()
        self.assertEqual(book.phrases, [])
        self.assertIsNotNone(book.id)

