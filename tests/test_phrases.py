from unittest import TestCase
from uuid import uuid4

from phrase_book.objects.phrase import Phrase


class TestPhrases(TestCase):

    def test_phrase_creation(self):
        phrase: Phrase = Phrase('Good Morning', str(uuid4()))
        self.assertIsNotNone(phrase.book_id)
        self.assertIsNotNone(phrase.id)
