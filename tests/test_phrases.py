from unittest import TestCase
from uuid import uuid4

import app
from phrase_book.models.phrase import Phrase


class TestPhrases(TestCase):

    def setUp(self):
        app.testing = True

    def test_phrase_creation(self):
        phrase: Phrase = Phrase('Good Morning', str(uuid4()))
        self.assertIsNotNone(phrase.book_id)
        self.assertIsNotNone(phrase.id)
